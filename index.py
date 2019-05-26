# coding=utf-8

from flask import Flask, request, send_from_directory, make_response
import os
import io
import socket


app = Flask(__name__)
abspath = os.path.dirname(__file__)
print()
print(abspath)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('www.baidu.com', 80))
ip = s.getsockname()[0]
print(ip)

@app.route("/")
def index():
    title = f'{abspath}下的文件:<br/>'
    return title+_listfilestohtml('.')


def _listfilestohtml(path):
    display = ''
    files = os.listdir(path)
    # print(f'files:{files}')
    for file in files:
        # print(f'file-{file}')
        filepath = path+"/"+file
        # print(f'filepath: {filepath}')
        # print(f'type {file}', os.path.isdir(filepath))
        filepathsplit = filepath.split("/")
        # print(filepathsplit)
        filepathdisplay = filepathsplit[-1]

        # print(filepathdisplay)
        if os.path.isdir(filepath):
            # nextpath = os.path.join(path, file)
            display += '&nbsp;'*4*(len(filepathsplit)-1) + filepathdisplay+'<br/>'
            nextpath = path+"/"+file
            # print(f'nextpath={nextpath}')
            display += _listfilestohtml(nextpath)
        else:
            display += '&nbsp;'*4*(len(filepathsplit)-1) + f'<a href="/d?path={filepath}">'+filepathdisplay+'</a><br/>'
    return display


@app.route("/d", methods=['GET', 'POST'])
def download():
    path = request.values.get('path')
    print(path)
    if os.path.isfile(path):
        # return send_from_directory(abspath, path.encode().decode('latin-1'), as_attachment=True)
        response = make_response(send_from_directory(abspath, path, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(path.split("/")[-1].encode().decode('latin-1'))
        return response

    else:
        return 'Not a file.'



if  __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True, debug=True)

