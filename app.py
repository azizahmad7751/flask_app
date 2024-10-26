from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io
import base64

app = Flask(__name__)

def riemann_sum(f, x_range, y_range, method='midpoint', num_subdivisions=10):
    x_min, x_max = x_range
    y_min, y_max = y_range
    dx = (x_max - x_min) / num_subdivisions
    dy = (y_max - y_min) / num_subdivisions
    total_sum = 0.0

    # Sample grid points
    x_vals = np.linspace(x_min, x_max, num_subdivisions)
    y_vals = np.linspace(y_min, y_max, num_subdivisions)

    # Approximation methods
    for i in range(num_subdivisions):
        for j in range(num_subdivisions):
            if method == 'midpoint':
                x = x_vals[i] + dx / 2
                y = y_vals[j] + dy / 2
            # Other methods can be implemented here

            total_sum += f(x, y) * dx * dy

    return total_sum

def generate_3d_plot(f, x_range, y_range):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.linspace(x_range[0], x_range[1], 30)
    y = np.linspace(y_range[0], y_range[1], 30)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    ax.plot_surface(X, Y, Z, cmap="viridis")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url

@app.route("/", methods=["GET", "POST"])
def index():
    result, plot_url = None, None
    if request.method == "POST":
        f_input = request.form.get("function")
        x_min, x_max = float(request.form.get("x_min")), float(request.form.get("x_max"))
        y_min, y_max = float(request.form.get("y_min")), float(request.form.get("y_max"))
        method = request.form.get("method")
        num_subdivisions = int(request.form.get("subdivisions"))

        # Define function dynamically
        f = lambda x, y: eval(f_input)

        # Calculate the Riemann Sum
        result = riemann_sum(f, (x_min, x_max), (y_min, y_max), method, num_subdivisions)
        plot_url = generate_3d_plot(f, (x_min, x_max), (y_min, y_max))

    return render_template("index.html", result=result, plot_url=plot_url)

if __name__ == "__main__":
    app.run(debug=True)
