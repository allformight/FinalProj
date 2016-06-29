from __future__ import unicode_literals
from flask import Flask,render_template, request,send_file

import getMusic,os.path


app = Flask(__name__)
filename = ''
path =''

@app.route('/')
def index(): 
    return render_template('index.html')
    
# @app.route('/')
# def index():
#     return render_template('test.html')
 
@app.route('/download', methods=['POST'])
def download():
    global path
    download_link = request.form.get('textField','all')    
    # print(download_link)
    checkYtube = "https://www.youtube.com" # check youtube url
    if (download_link.startswith(checkYtube)):
        # return render_template('pending.html')
        # print(getMusic.filename)
        print(path)
        getMusic.getMusic(download_link)
        # if getMusic.path_flag == 2 : 
        
        path = getMusic.filename
        #path = unicode(path)
        print(path)
        #path = path.encode('latin-1')
        #path = path.encode('utf-8')
       
        return render_template('download.html',link = '/savefile')
        # else :
        #     return render_template('download.html',link = '/savefile')
    else :
        return render_template('errorlink.html')

@app.route('/savefile')
def file_downloads():
	    
    print(path)
    return send_file(path, as_attachment=True)




if __name__=="__main__":
    app.run(host='140.123.103.172',port=8888)
