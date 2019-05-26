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
    title = f'{abspath}下的文件:<br/>'
    return title+_listfilestohtml('.')
    filedict = _listfiles('.')
    return str(filedict)+downloadhtml


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
        filepathdisplay = filepathsplit[-1]

        # print(filepathdisplay)
        if os.path.isdir(filepath):
            # nextpath = os.path.join(path, file)
            display += '&nbsp;'*4*(len(filepathsplit)-1) + filepathdisplay+'<br/>'
            nextpath = path+"/"+file
            # print(f'nextpath={nextpath}')
            display += _listfilestohtml(nextpath)
        else:
            display += '&nbsp;'*4*(len(filepathsplit)-1) + f'<a href=/d?path={filepath}>'+filepathdisplay+'</a><br/>'
    return display


# def _listfiles(path):
#     display = {}
#     files = os.listdir(path)
#     # print(f'files:{files}')
#     for file in files:
#         # print(f'file-{file}')
#         filepath = path+"/"+file
#         # print(f'type {file}', os.path.isdir(filepath))
#         if os.path.isdir(filepath):
#             # nextpath = os.path.join(path, file)
#             nextpath = path+"/"+file
#             # print(f'nextpath={nextpath}')
#             display[file]=_listfiles(nextpath)
#         else:
#             display[file]=1
#     return display
#
# def _parsedicttohtml(dict):
#     pass

@app.route("/d", methods=['GET', 'POST'])
def download():
    path = request.values.get('path')
    if os.path.isfile(path):
        return send_from_directory(abspath, filename=path, as_attachment=True)
    else:
        return 'is not a file'



if  __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True)

