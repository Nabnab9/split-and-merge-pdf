import os
import importlib
import split_and_merge
from flask import Flask, flash, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename

importlib.import_module("split_and_merge")

UPLOAD_FOLDER = 'Source/'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        date = request.form['date']
        nb = request.form['nb']
        # check if the post request has the file part
        if 'files' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files')
        if files and len(files) > 0:
            for file in files:
                if file.filename == '':
                    return redirect(request.url)
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            split_and_merge_class = split_and_merge.SplitAndMergePdf(date, int(nb))
            split_and_merge_class.run()
            path = "Document_Final.pdf"
            return send_file(path)
        else:
            return redirect(request.url)
    else:
        return render_template("split.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
