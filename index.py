# coding=utf-8

from flask import Flask, request, send_from_directory
import os
import io
import socket


app = Flask(__name__)
abspath = os.path.dirname(__file__)
print(abspath)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('www.baidu.com', 80))
ip = s.getsockname()[0]
print(ip)

@app.route("/")
def index():
    downloadhtml = '''
    <br/>
    <form action="/d" method='post'>
        <input type='text' name='path'>
        <input type='submit' value='下载'>
    </form>
    '''
    return str(_listfiles('.'))+downloadhtml


def _parsedicttohtml():
    pass


def _listfiles(path):
    display = {}
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
            display[file]=_listfiles(nextpath)
        else:
            display[file]=1
    return display


@app.route("/d", methods=['GET', 'POST'])
def download():
    path = request.values.get('path')
    if os.path.isfile(path):
        return send_from_directory(abspath, filename=path, as_attachment=True)
    else:
        return 'is not a file'



if  __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

