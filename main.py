import json
import os
import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from email_sender import send_email
from s3_helper import read_session_files, upload_transcription
from transcribe import transcribe_rev_ai

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)


@app.route('/process-recording', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
def process_recording():
    session_id = str(uuid.uuid4())
    temp_rec_file_name = f'{session_id}.wav'
    try:
        recording_file = request.files['recording_file']
        email = request.form['email']
        print(f'Got a new request for email {email}. Assigned {session_id} as the session id')
        recording_file.save(temp_rec_file_name)
        trans_results = transcribe_rev_ai(temp_rec_file_name)
        s3_dir_name = f'{email}_{session_id}'
        upload_transcription(s3_dir_name, trans_results, temp_rec_file_name)
    except Exception as ex:
        os.remove(temp_rec_file_name)
        print(f'Error while processing request [{ex}]')
        return "General error. We're about to fire someone.", 500

    os.remove(temp_rec_file_name)
    send_email(email, session_id)
    print(f'Finished processing request for {email}')
    return 'OK'


@app.route('/get-recording-sessions', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_data():
    sessions = read_session_files()
    return json.dumps(sessions)


@app.route('/get-session-data', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_data_for_session():
    session_id = request.args.get('session_id')
    session = read_session_files(session_id)
    if session_id not in session:
        return f"Session id {session_id} doesn't exist", 400
    return json.dumps(session[session_id])


@app.route('/get-user-data', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_user_data():
    email = request.args.get('email')
    result = []
    for session_id, data in read_session_files(email).items():
        data['session_id'] = session_id
        result.append(data)

    return jsonify(result)


@app.route('/test-app', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def test_app_endpoint():
    return "you shouldn't be here"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
