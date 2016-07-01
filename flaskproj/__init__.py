from __future__ import unicode_literals
from flask import Flask,render_template, request,send_file
import threading
import getMusic,os.path



app = Flask(__name__)
filename = ''
path =''
download_link = ''
flag = 0   

@app.route('/')
def index(): 
    return render_template('index.html')
    
# @app.route('/')
# def index():
#     return render_template('test.html')

@app.route('/loading', methods=['POST'])
def loading():
    global download_link,flag,path

    download_link = request.form.get('textField','all')
    checkYtube = "https://www.youtube.com" # check youtube url
    if (download_link.startswith(checkYtube)): 
      

        print('dddd')
        flag=1      
        return render_template('loading.html')
        
     
    else :
        flag=0
        return render_template('errorlink.html')
        
   

 
@app.route('/download')
def download():
    global path
    if(flag):      
        getMusic.getMusic(download_link) 
        path = getMusic.filename  
        return render_template('download.html',link = '/savefile')
    else :
        return render_template('errorlink.html')

@app.route('/savefile')
def file_downloads():
	    
    print(path)
    return send_file(path, as_attachment=True)




if __name__=="__main__":
    app.run(host='127.0.0.1',port=8888)
