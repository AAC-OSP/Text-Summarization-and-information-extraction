from flask import Flask, render_template, request
from Text_Summarization_Information_Extraction import *
import os

app = Flask(__name__)

#Controller
@app.route("/", methods = ["GET", "POST"])
def index():
  data = ""
  if method == "POST":
    if 'file' in request.files:
      file = request.files['file']
      file_type = os.path.split(file)[1]
      text = ''
      if file_type == 'pdf':
        text = extract_text_pdf(file)
      elif file_type == 'txt':
        with open(file, 'r') as f:
          text = f.read()
      result = summarize_text(text)
      data = result
    else:
      text = request.get('text')
      result = summarize_text(text)
      data = result

  return render_template("index.html", data = data)
    


if __name__ == "__main__":
  app.run(debug = True)
