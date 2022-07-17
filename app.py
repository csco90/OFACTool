from flask import Flask, session
from datetime import datetime

from flask import render_template, abort, request, redirect, flash
import os

from ofac_check import check_names

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'


@app.route("/")
@app.route("/home")
def home():
    """Renders the home page."""
    return render_template(
        "index.html",
        title="Home Page",
        year=datetime.now().year,
    )


AbsPath = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(AbsPath, "static", "inputexcel")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/check/multiple", methods=["GET", "POST"])
def check_multiple():
    if request.method == "POST":

        if request.files:

            if request.files["excelfile"].filename != "":
                excelfile = request.files["excelfile"]
                print(app.config["UPLOAD_FOLDER"])

                excelfile.save(os.path.join(app.config["UPLOAD_FOLDER"], excelfile.filename))

                check_names(os.path.join(app.config["UPLOAD_FOLDER"], excelfile.filename), excelfile.filename)

                return render_template(
                    "check_multiple.html",
                    title="Multiple",
                    year=datetime.now().year,
                    fileuploaded=True,
                    filename = excelfile.filename
                )
            else:
                print("No file was selected")
                return redirect(request.url)

    if request.method == "GET":
        return render_template(
            "check_multiple.html",
            title="Multiple",
            year=datetime.now().year,
            fileuploaded = False
        )


if __name__ == '__main__':
    app.run(debug=True, use_debugger=True, use_reloader=False)
