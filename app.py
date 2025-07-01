from flask import Flask, request, jsonify, send_file, render_template, url_for
import os
from werkzeug.utils import secure_filename
from WHISPER_AUDIO_TRANSCRIPTION import WhisperTranscriber

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'm4a', 'mp4', 'mov'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Whisper transcriber
transcriber = WhisperTranscriber(model_size="base")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Transcribe the audio file
            result = transcriber.transcribe_audio(filepath)
            
            # Clean up the uploaded file
            os.remove(filepath)
            
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/export', methods=['POST'])
def export():
    data = request.json
    format = data.get('format', 'txt')
    
    if not data.get('transcription'):
        return jsonify({'error': 'No transcription data provided'}), 400
    
    try:
        # Generate temporary filename
        temp_filename = f"transcription_{os.getpid()}.{format.lower()}"
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        
        # Export the transcription
        transcriber.export_transcription(data['transcription'], format, temp_path)
        
        # Send file and clean up
        return send_file(temp_path, as_attachment=True, download_name=f"transcription.{format.lower()}")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
