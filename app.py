from flask import Flask, render_template, request
from Text_Summarization_Information_Extraction import *

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
  data = ""
  if method == "POST":
    pass

  return render_template("index.html", data = data)
    


if __name__ == "__main__":
  app.run(debug = True)
