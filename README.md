# Earnings Call Transcription System

## Overview

The Earnings Call Transcription System is an open-source project designed to automatically transcribe earnings call audio files. It uses a client-server architecture to process long audio files efficiently, providing real-time transcription updates and saving the final transcript to a structured text file.

### Key Features

- Processes long audio files (e.g., hour-long earnings calls)
- Real-time transcription using Google's Speech Recognition API
- Handles overlapping audio chunks to ensure no data loss
- Saves transcriptions to a structured, easily readable text file
- WebSocket-based communication for real-time updates

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/earnings-call-transcription.git
   cd earnings-call-transcription
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Starting the Server

1. Navigate to the project directory.
2. Run the following command:
   ```
   uvicorn earnings-call-api:app --reload --log-level debug
   ```
3. The server will start running on `http://localhost:8000`.

### Running the Client

1. Ensure your audio file is in a supported format (e.g., MP3).
2. Update the `audio_file_path` in `test_client.py` to point to your audio file.
3. Run the client:
   ```
   python test_client.py
   ```

4. The client will process the audio file and send it to the server for transcription.
5. Transcription progress will be displayed in the console.
6. Once complete, you'll find the transcription file in the same directory as the server script.

## File Structure

- `earnings-call-api.py`: The main server script that handles WebSocket connections and transcription.
- `test_client.py`: The client script that processes and sends audio data to the server.
- `requirements.txt`: List of Python dependencies.
- `README.md`: This file, containing project documentation.

## Contributing

We welcome contributions to the Earnings Call Transcription System! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear, descriptive messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

Please ensure your code adheres to the project's coding standards and include tests for new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses Google's Speech Recognition API through the SpeechRecognition library.
- Thanks to all contributors who have helped to improve this project.

For any questions or issues, please open an issue on the GitHub repository.
