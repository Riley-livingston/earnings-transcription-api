import asyncio
import websockets
import json
import os
from pydub import AudioSegment
import io

CHUNK_SIZE = 30000  # 30 seconds
OVERLAP = 5000  # 5 seconds overlap

async def send_audio():
    uri = "ws://localhost:8000/ws/transcribe"
    audio_file_path = 'lpth_q_4_2024_09_19_earnings_summary.mp3'  # Your audio file path

    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file not found at {audio_file_path}")
        return

    try:
        # Load audio file
        audio = AudioSegment.from_mp3(audio_file_path)
        
        # Convert to mono and set sample rate to 16kHz
        audio = audio.set_frame_rate(16000).set_channels(1)

        print(f"Audio file loaded: {len(audio)/1000:.2f} seconds")

        async with websockets.connect(uri) as websocket:
            # Send audio file metadata
            metadata = {
                "filename": os.path.basename(audio_file_path),
                "duration": len(audio) / 1000,
                "sample_rate": audio.frame_rate,
                "channels": audio.channels
            }
            await websocket.send(json.dumps(metadata))

            for start_ms in range(0, len(audio), CHUNK_SIZE - OVERLAP):
                end_ms = start_ms + CHUNK_SIZE
                chunk = audio[start_ms:end_ms]
                
                # Convert chunk to wav format
                buffer = io.BytesIO()
                chunk.export(buffer, format="wav")
                wav_data = buffer.getvalue()

                # Send chunk size first
                await websocket.send(len(wav_data).to_bytes(4, byteorder='big'))
                
                # Then send the chunk data
                await websocket.send(wav_data)
                print(f"Sent chunk from {start_ms/1000:.2f}s to {end_ms/1000:.2f}s, size: {len(wav_data)} bytes")
                
                # Wait for and print the transcription
                response = await websocket.recv()
                transcript = json.loads(response)
                
                if transcript['transcript']:
                    last_segment = transcript['transcript'][-1]
                    print(f"Transcription: {last_segment['text']}")
                else:
                    print("No transcription received for this chunk.")
                
                # Short delay to prevent overwhelming the server
                await asyncio.sleep(0.1)

        print("Audio file processing completed.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(send_audio())