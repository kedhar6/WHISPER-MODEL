document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const uploadButton = document.getElementById('uploadButton');
    const fileInput = document.getElementById('fileInput');
    const transcriptionSection = document.getElementById('transcriptionSection');
    const transcriptionContent = document.getElementById('transcriptionContent');

    // Drag and drop functionality
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#007bff';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = '#ccc';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#ccc';
        
        const file = e.dataTransfer.files[0];
        if (file) {
            handleFile(file);
        }
    });

    // File input handling
    uploadButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    async function handleFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/transcribe', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                displayTranscription(result);
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during transcription');
        }
    }

    function displayTranscription(data) {
        transcriptionSection.style.display = 'block';
        transcriptionContent.innerHTML = '';

        // Display overall transcription
        const transcriptionDiv = document.createElement('div');
        transcriptionDiv.className = 'transcription-segment';
        transcriptionDiv.innerHTML = `
            <h3>Full Transcription</h3>
            <p>${data.transcription}</p>
        `;
        transcriptionContent.appendChild(transcriptionDiv);

        // Display segments with timestamps
        data.segments.forEach(segment => {
            const segmentDiv = document.createElement('div');
            segmentDiv.className = 'transcription-segment';
            segmentDiv.innerHTML = `
                <h3>Segment</h3>
                <p class="timestamp">Start: ${segment.start.toFixed(2)}s - End: ${segment.end.toFixed(2)}s</p>
                <p>${segment.text}</p>
            `;
            transcriptionContent.appendChild(segmentDiv);
        });
    }

    async function exportTranscription(format) {
        const transcriptionData = {
            transcription: transcriptionContent.innerText
        };

        try {
            const response = await fetch('/api/export', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    transcription: transcriptionData,
                    format: format
                })
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `transcription.${format.toLowerCase()}`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            }
        } catch (error) {
            console.error('Error exporting:', error);
            alert('Error exporting transcription');
        }
    }
});
