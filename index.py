# coding=utf-8

from flask import Flask
import os
import io


app = Flask(__name__)


@app.route("/")
def index():
    abspath = os.path.dirname(__file__)
    print(abspath)
    return str(_listfiles(abspath))

def _listfiles(path):
    display = []
    files = os.listdir(path)
    # print(f'files:{files}')
    for file in files:
        # print(f'file-{file}')
        filepath = path+"/"+file
        # print(f'type {file}', os.path.isdir(filepath))
        if os.path.isdir(filepath):
            # nextpath = os.path.join(path, file)
            nextpath = path+"/"+file
            # print(f'nextpath={nextpath}')
            display .append(_listfiles(nextpath))
        else:
            display.append(filepath)
    return display

if  __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

