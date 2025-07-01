import whisper
import os
from typing import Dict, List
import json

class WhisperTranscriber:
    def __init__(self, model_size: str = "base"):
        """
        Initialize the Whisper transcriber with specified model size.
        
        Args:
            model_size: Whisper model size ("tiny", "base", "small", "medium", "large")
        """
        self.model = whisper.load_model(model_size)
        self.model_size = model_size

    def transcribe_audio(self, audio_path: str) -> Dict:
        """
        Transcribe audio file and generate detailed transcription data.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dict containing transcription data with timestamps and analysis
        """
        try:
            # Load and transcribe audio
            result = self.model.transcribe(audio_path)
            
            # Extract segments with timestamps
            segments = result["segments"]
            
            # Format results
            formatted_result = {
                "model": self.model_size,
                "transcription": result["text"],
                "segments": [],
                "analysis": self._analyze_content(result["text"])
            }
            
            # Process each segment
            for segment in segments:
                formatted_result["segments"].append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"],
                    "words": self._process_words(segment["words"]) if "words" in segment else []
                })
            
            return formatted_result
            
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")

    def _process_words(self, words: List[Dict]) -> List[Dict]:
        """
        Process individual words with timestamps.
        """
        processed_words = []
        for word in words:
            processed_words.append({
                "word": word["word"],
                "start": word["start"],
                "end": word["end"],
                "confidence": word.get("confidence", 1.0)
            })
        return processed_words

    def _analyze_content(self, text: str) -> Dict:
        """
        Analyze the transcription content and provide contextual information.
        
        Returns:
            Dict containing content analysis
        """
        # Basic analysis - can be extended based on requirements
        analysis = {
            "word_count": len(text.split()),
            "sentence_count": len(text.split('.')),
            "confidence": "High" if self.model_size in ["medium", "large"] else "Medium"
        }
        return analysis

    def export_transcription(self, transcription_data: Dict, format: str, output_path: str) -> None:
        """
        Export transcription data in specified format.
        
        Args:
            transcription_data: Dictionary containing transcription data
            format: Export format ("txt", "json", "csv")
            output_path: Path to save the exported file
        """
        if format == "txt":
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(transcription_data["transcription"])
        elif format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(transcription_data, f, indent=2, ensure_ascii=False)
        elif format == "csv":
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Segment Start", "Segment End", "Text"])
                for segment in transcription_data["segments"]:
                    writer.writerow([segment["start"], segment["end"], segment["text"]])
        else:
            raise ValueError(f"Unsupported format: {format}")
