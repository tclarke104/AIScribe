from app.recording import bp
from flask import request
import os
import uuid
import app.services.recording_service as rs
from flask import current_app
from flask import jsonify
from app.models.recording import Recording

@bp.route('/transcribe', methods=['POST'])
def transcribe_recording():
    path = current_app.config['UPLOAD_FOLDER']
    id = uuid.uuid4()
    recording = request.files['recording'].read()
    save_path = os.path.join(path, f'{id}.wav')
    
    with open(save_path, 'ab') as f:
        f.write(recording)


    text = rs.transcribe(save_path)

    return {'transcription': text}

@bp.route('/note', methods=['POST'])
def generate_note():
    text = request.json['transcription']

    note = rs.get_llm_response(text)

    return {'note': note}