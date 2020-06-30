# coding=utf-8


import os
import socket
import sys
import functools
import time
from flask import Flask, request, send_from_directory, make_response

app = Flask(__name__)
abspath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv)>=2:
    inputpath = sys.argv[1]
    if os.path.isdir(inputpath):
        abspath = os.path.abspath(inputpath)

print(abspath)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('www.baidu.com', 80))
ip = s.getsockname()[0]
print(ip)



def timeit(fn):
    print(f"allow timeit on {fn.__name__}")
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print(f" {fn.__name__} run time: {end-start} ms")
        return result
    return wrapper


@app.route("/")
@timeit
def index():
    title = f'{abspath}下的文件:<br/>'
    return title+_listfilestohtml(abspath)


@functools.lru_cache(maxsize=128)
def _listfilestohtml(path):
    display = []
    files = os.listdir(path)
    # print(f'files:{files}')
    for file in files:
        # print(f'file-{file}')
        if file.startswith("."):
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
            display.append('&nbsp;'*4*(len(filepathsplit)-1) + filepathdisplay+'<br/>')
            nextpath = os.path.join(path, file)
            # print(f'nextpath={nextpath}')
            display.append( _listfilestohtml(nextpath))
        else:
            display .append('&nbsp;'*4*(len(filepathsplit)-1) + f'<a href="/download?path={filepath}">'+filepathdisplay+'</a><br/>')
    return "".join(display)


@app.route("/download", methods=['GET', 'POST'])
def download():
    path = request.values.get('path')
    path = os.path.abspath(path)
    print(path)
    if not path.startswith(abspath):
        return "Invalid path."
    if os.path.isfile(path):
        dirpath = os.path.dirname(path)
        filename = path.replace(dirpath, '')[1:]
        # print(dirpath)
        # return send_from_directory(abspath, path.encode().decode('latin-1'), as_attachment=True)
        response = make_response(send_from_directory(dirpath, filename, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
        return response

    else:
        return 'File name error or not a file.'


if  __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True)

