from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
from quint.transcribtion import google_api as tga
from quint.transcribtion import highlights
from quint.chunk.get_topics import get_topics
import os
output_filepath = os.getenv('OUTPUP_PATH')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    return {'greeting': 'Hello'}


@app.post("/transcript")
def upload(file: UploadFile = File(...)):
    audio_file_name= file.filename
    if audio_file_name not in os.listdir("."):
        print('We got a new file')

        try:
            contents = file.file.read()
            with open(file.filename, 'wb') as f:
                # Get audio file namec

                audio_file_name = audio_file_name.split('.')[0] + '.wav'
                # if audio_file_name not in os.listdir("."):
                # Save audio file locally
                f.write(contents)
                # # Get audio file transcribtion
                transcript = tga.google_transcribe(audio_file_name)
                # Get colored highlights
                transcript = highlights.get_colored_transcript(transcript)
                # Create name for transcript
                transcript_filename = audio_file_name.split('.')[0] + '.txt'
                # Save transript file locally
                tga.write_transcripts(transcript_filename,transcript)

                # else:
                #     return 'We already have this audio!'

                # Return transcript to the api query
                return  transcript


        except Exception as error:
            return {"message": error}

        finally:
            file.file.close()
    else:
        transcript_filename = audio_file_name.split('.')[0] + '.txt'
        path_of_text = output_filepath + transcript_filename
        transcript = highlights.get_colored_transcript(path_of_text)
        transcript_filename = audio_file_name.split('.')[0] + '_colored'+'.txt'
        tga.write_transcripts(transcript_filename,transcript)
        return transcript



# Get topics of an audio
@app.post("/topics")
def upload(file: UploadFile = File(...)):


    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            # Get audio file namec
            audio_file_name= file.filename
            audio_file_name = audio_file_name.split('.')[0] + '.wav'
            print(os.listdir("."))
            if audio_file_name not in os.listdir("."):
                # Save audio file locally
                f.write(contents)
                # Get audio file transcribtion
                transcript = tga.google_transcribe(audio_file_name)
                # Create name for transcript
                transcript_filename = audio_file_name.split('.')[0] + '.txt'
                # Save transript file locally
                tga.write_transcripts(transcript_filename,transcript)
                # Get topics
                path_of_text = output_filepath + transcript_filename
                print(path_of_text)
                topics = get_topics(path_of_text)
            else:
                transcript_filename = audio_file_name.split('.')[0] + '.txt'
                # Get topics
                path_of_text = output_filepath + transcript_filename
                print(path_of_text)
                topics = get_topics(path_of_text)

            # Return transcript to the api query
            return  topics


    except Exception as error:
        return {"message": error}

    finally:
        file.file.close()
