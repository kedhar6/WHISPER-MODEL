# Whisper Audio Transcription Project

A web application for transcribing audio and video files using OpenAI's Whisper model.

## Features

- Audio/Video transcription using OpenAI's Whisper model
- Modern web interface with drag & drop functionality
- Multiple export formats (TXT, CSV, JSON)
- Timestamp generation for segments and words
- Content analysis and statistics

## Project Structure

```
whisper_project/
├── app.py                  # Flask backend server
├── WHISPER_AUDIO_TRANSCRIPTION.py  # Core transcription logic
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── styles.css         # Frontend styles
│   └── script.js          # Frontend JavaScript
└── uploads/              # Directory for temporary file uploads
```

## Setup Instructions

1. Install FFmpeg
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```
   python app.py
   ```
4. Access the application at http://localhost:5000

## Dependencies

- Flask
- OpenAI Whisper
- numpy
- scipy
- soundfile
- torch
- tqdm

## Usage

1. Drag and drop audio/video files into the web interface
2. Select desired output format
3. Click "Transcribe" to start the process
4. Download the transcribed output in selected format
