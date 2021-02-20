import http
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS, cross_origin

from s3_helper import upload_transcription
from transcribe import transcribe_rev_ai

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)


def run_app():
    app.run(host='0.0.0.0', port=8080)


@app.route('/process-recording', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
def extract_doc_api():
    try:
        recording_file = request.files['recording_file']
        email = request.form['email_address']
        print(f'Got a new request for email {email}')
        trans_results = transcribe_rev_ai(recording_file)
        upload_transcription(f'{email}_{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', trans_results)
    except Exception as ex:
        return http.HTTPStatus.INTERNAL_SERVER_ERROR

    return 'OK'


if __name__ == "__main__":
    run_app()
