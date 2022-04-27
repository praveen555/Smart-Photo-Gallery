import time

from flask import render_template
from flask import request

from app import folder, webapp
# from app.aws_transcribe import aws_transcribe

webapp.config['UPLOAD_FOLDER'] = folder


@webapp.route('/search_by_voice', methods=['GET'])
def search_voice():
    return render_template('search_voice.html')


@webapp.route('/voice', methods=['POST', 'GET'])
def display_voice():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')
        time.sleep(2)
        print("After sleeping")
        status = 1
        # run the aws transcribe service and return the printed text
        # subprocess.call("aws_transcribe.py", shell=True)
        # aws_transcribe()

        return render_template('transcribe.html', status=status)
    else:
        status = -1
        return render_template("transcribe.html", status=status)
