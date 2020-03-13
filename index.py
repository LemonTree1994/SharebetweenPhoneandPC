# coding=utf-8

from flask import Flask, request, send_from_directory, make_response
import os
import io
import socket


app = Flask(__name__)
abspath = os.path.dirname(__file__)
abspath = os.path.abspath(os.path.join(abspath, '..'))
print()
# abspath = '.'
print(abspath)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('www.baidu.com', 80))
ip = s.getsockname()[0]
print(ip)

@app.route("/")
def index():
    title = f'{abspath}下的文件:<br/>'
    return title+_listfilestohtml(abspath)


def _listfilestohtml(path):
    display = ''
    files = os.listdir(path)
    # print(f'files:{files}')
    for file in files:
        # print(f'file-{file}')
        if file == "share-files":
            continue
        filepath = os.path.join(path, file)
        # print(f'filepath: {filepath}')
        # print(f'type {file}', os.path.isdir(filepath))
        filepathsplit = filepath.split("\\")
        # print(filepathsplit)
        filepathdisplay = filepathsplit[-1]

        # print(filepathdisplay)
        if os.path.isdir(filepath):
            # nextpath = os.path.join(path, file)
            display += '&nbsp;'*4*(len(filepathsplit)-1) + filepathdisplay+'<br/>'
            nextpath = os.path.join(path, file)
            # print(f'nextpath={nextpath}')
            display += _listfilestohtml(nextpath)
        else:
            display += '&nbsp;'*4*(len(filepathsplit)-1) + f'<a href="/d?path={filepath}">'+filepathdisplay+'</a><br/>'
    return display


@app.route("/d", methods=['GET', 'POST'])
def download():
    path = request.values.get('path')
    path = os.path.abspath(path)
    print(path)
    if os.path.isfile(path):
        dirpath = os.path.dirname(path)
        filename = path.replace(dirpath, '')[1:]
        # print(dirpath)
        # return send_from_directory(abspath, path.encode().decode('latin-1'), as_attachment=True)
        response = make_response(send_from_directory(dirpath, filename, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
        return response

    else:
        return 'Not a file.'



if  __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888, threaded=True)

