import os
import logging
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import List
import speech_recognition as sr
import numpy as np
import io
import time
import wave
import json
from difflib import SequenceMatcher

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize speech recognizer
recognizer = sr.Recognizer()

class TranscriptSegment(BaseModel):
    speaker: str
    text: str
    timestamp: float

class EarningsCall(BaseModel):
    company: str
    date: str
    transcript: List[TranscriptSegment]

def merge_transcripts(prev_text, new_text):
    """Merge two transcript segments, resolving overlaps."""
    matcher = SequenceMatcher(None, prev_text, new_text)
    merged = ""
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'equal' or op == 'replace':
            merged += new_text[j1:j2]
        elif op == 'insert':
            merged += new_text[j1:j2]
        elif op == 'delete':
            continue
    return merged

def write_transcription(transcript_file, segment):
    """Write a transcript segment to the file."""
    with open(transcript_file, 'a') as f:
        f.write(f"[{segment.timestamp:.2f}] {segment.speaker}: {segment.text}\n")

@app.websocket("/ws/transcribe")
async def transcribe_call(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")
    call = EarningsCall(company="", date="", transcript=[])
    
    chunk_count = 0
    transcript_file = f"transcript_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    last_transcription = ""
    
    # Receive metadata
    metadata_json = await websocket.receive_text()
    metadata = json.loads(metadata_json)
    logger.info(f"Received metadata: {metadata}")
    
    # Write header to transcript file
    with open(transcript_file, 'w') as f:
        f.write(f"Earnings Call Transcription\n")
        f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Audio File: {metadata['filename']}\n")
        f.write(f"Duration: {metadata['duration']:.2f} seconds\n\n")
    
    try:
        while True:
            # Receive chunk size first
            size_data = await websocket.receive_bytes()
            chunk_size = int.from_bytes(size_data, byteorder='big')
            
            # Then receive the chunk data
            audio_data = await websocket.receive_bytes()
            chunk_count += 1
            logger.info(f"Received audio chunk #{chunk_count} of size {len(audio_data)} bytes")
            
            # Process audio data
            with io.BytesIO(audio_data) as wav_io:
                with sr.AudioFile(wav_io) as source:
                    audio = recognizer.record(source)
            
            try:
                logger.debug("Attempting speech recognition...")
                text = recognizer.recognize_google(audio, show_all=False)
                logger.debug(f"Raw recognition result: {text}")
                
                if not text:
                    raise sr.UnknownValueError("No recognition result returned")
                
                # Merge with previous transcription to handle overlaps
                merged_text = merge_transcripts(last_transcription, text)
                last_transcription = text  # Store for next iteration
                
                # Add transcribed text to the call transcript
                segment = TranscriptSegment(speaker="Speaker", text=merged_text, timestamp=get_current_timestamp())
                call.transcript.append(segment)
                
                # Write transcription to file
                write_transcription(transcript_file, segment)
                
                # Send the updated transcript back to the client
                await websocket.send_json(call.dict())
                logger.info(f"Sent transcription: {merged_text}")
                
            except sr.UnknownValueError:
                logger.warning("Speech Recognition could not understand audio")
            except sr.RequestError as e:
                logger.error(f"Could not request results from Speech Recognition service; {e}")
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {str(e)}")
        logger.exception("Full traceback:")
    finally:
        logger.info("WebSocket connection closed")
        logger.info(f"Transcription saved to {transcript_file}")

def get_current_timestamp() -> float:
    return time.time()

@app.post("/calls")
async def create_call(call: EarningsCall):
    logger.info(f"Received request to create call for company: {call.company}")
    # Save the call data to a database
    return {"message": "Call saved successfully"}

@app.get("/calls/{company}")
async def get_call(company: str):
    logger.info(f"Received request to get call for company: {company}")
    # Retrieve call data from the database
    return {"message": "Call data retrieved"}