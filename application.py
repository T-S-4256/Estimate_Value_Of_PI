from flask import Flask, send_file,render_template,request
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random
import math
import io
import os

app = Flask(__name__)
try:
    with open(r"D:\PROJECT.H\4TH_SEM_PYTHON_PROJECTS\Monte_Carlo_Simulation\sourceCode.txt", "r") as f:
        SourceCode=f.read()
except Exception as e:
    SourceCode="No Data Found"

@app.route('/')
def homePage():
    return render_template("index.html")

@app.route('/Estimate_Pi',methods=["POST","GET"])
def Estimate_Pi():
    if request.method=="POST":
        total_points=int(request.form.get("total_points"))
        cirPoint = 0
        x2, y2 = 0.5, 0.5
        radius = 0.5
        sqPoint = total_points
        squarePoints = []
        circlePoints = []

        for _ in range(sqPoint):
            x1 = random.random()
            y1 = random.random()
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if distance <= radius:
                cirPoint += 1
                circlePoints.append((x1, y1))
            else:
                squarePoints.append((x1, y1))

        circlePoints = np.array(circlePoints)
        squarePoints = np.array(squarePoints)

        fig, ax = plt.subplots()
        ax.set_aspect("equal")
        circle = patches.Circle((0.5, 0.5), radius, fill=False, edgecolor="blue", linewidth=2)
        ax.add_patch(circle)

        if len(circlePoints) > 0:
            ax.scatter(circlePoints[:, 0], circlePoints[:, 1], color="green", label="Inside", s=10)
        if len(squarePoints) > 0:
            ax.scatter(squarePoints[:, 0], squarePoints[:, 1], color="red", label="Outside", s=10)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        result=(4 * cirPoint) / sqPoint
        plt.title(f"Monte Carlo Estimate of π ≈ {(4 * cirPoint) / sqPoint:.5f}")
        plt.legend()
        plt.grid(True)

        # Save the graph image to static folder
        image_path = os.path.join("static", "graph.png")
        plt.savefig(image_path)
        plt.close()

        return render_template("index.html", pi_value=result, source_code=SourceCode, total_points=total_points)

    return render_template("index.html", total_points=total_points)


@app.route('/download_source')
def download_source():
    path = r"D:\PROJECT.H\4TH_SEM_PYTHON_PROJECTS\Monte_Carlo_Simulation\sourceCode.txt"
    try:
        return send_file(path, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"



if __name__=="__main__":
    app.run(host="0.0.0.0",port=8000)