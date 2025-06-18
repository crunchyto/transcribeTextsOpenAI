#!/usr/bin/env python3
import argparse
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Transcribe MP3 audio file to Spanish text using OpenAI')
    parser.add_argument('mp3_file', help='Path to the MP3 audio file to transcribe')
    
    args = parser.parse_args()
    mp3_file_path = args.mp3_file
    
    # Validate file exists
    if not os.path.exists(mp3_file_path):
        print(f"Error: File '{mp3_file_path}' does not exist.")
        sys.exit(1)
    
    # Validate file has .mp3 extension
    if not mp3_file_path.lower().endswith('.mp3'):
        print(f"Error: File '{mp3_file_path}' is not an MP3 file.")
        sys.exit(1)
    
    print(f"Processing audio file: {mp3_file_path}")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)
    
    try:
        # Open and transcribe the audio file
        with open(mp3_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="es"
            )
        
        transcription_text = transcript.text
        print("Transcription completed successfully.")
        
        # Generate output filename
        output_file_path = os.path.splitext(mp3_file_path)[0] + '.txt'
        
        # Write transcription to file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(transcription_text)
        
        print(f"Transcription saved to: {output_file_path}")
        
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        sys.exit(1)



if __name__ == "__main__":
    main()
