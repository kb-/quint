from distutils import text_file
from turtle import right
import streamlit as st
import base64
import time
import random

from time import sleep
from pytube import YouTube
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from IPython.display import YouTubeVideo
import os
#Importing from our own repository
from processing import concatenate_lines
from punctuation_api import punctuate
from chunk_api import chunk
from summary_api import summarize
from timestamp import timestamping
from youtube import video_name
from getting_best_api import get_best






#layout="wide"
st.set_page_config(page_title='Quint')
# st.set_option('deprecation.showPyplotGlobalUse', False)

st.session_state['flag'] = False



# component= "<h1 style= 'color: red' > Inject Header HTML  </h1>"
# st.markdown(component, unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.05,0.9,0.05])

with col1:
    st.write(' ')

with col2:
    st.image("logo.jpg")

with col3:
    st.write(' ')


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


main_html = '''
    <style>
    .stApp {
    background-image: url("data:image/jpg;base64,%s");
    background-size: cover;
    }

    .st-cs {
        background-color: green;
        background-image: linear-gradient(to right, #dd3764, #99ff99);
    }

    .css-1cpxqw2 {
        color:green;
        width:8em;
        height:2.5em;
        padding-bottom: 0 rem;
        padding-top: 100 rem;
        align: buttom;

    .ccss-ocqkz7 e1tzin5v4 {

        padding-bottom: 0 rem;
        padding-top: 0 rem;
        align: buttom;
    }
    </style>
    '''
st.markdown(main_html, unsafe_allow_html=True)


def main_page():
    st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

    st.markdown("# Quintessentia 🎈")



if 'status' not in st.session_state:
    st.session_state['status'] = 'submitted'


def refresh_state():
	st.session_state['status'] = 'submitted'


col1, col2 = st.columns([0.8,0.2])


with col1:
    link = st.text_input('', 'https://www.youtube.com/watch?v=v2ML_uKSskI', on_change=refresh_state)


with col2:
    st.text('')
    st.text('')
    summary = st.button('QUINT')






video_id = link.split("=")[1]
YouTubeVideo(video_id)

text_file = f"{video_id}.txt"

# First we check if we already have summary for some specifict podcast
if (summary) & (text_file not in os.listdir("results/")):


    # Get the transcipt: list of dictionaries
    YouTubeTranscriptApi.get_transcript(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Now we need to get the text out and punctuate it
    concatenated_text = concatenate_lines(transcript)  ## Function that creates txt file from list of texts
    print('Starting punctuating')
    punctuated_text = punctuate(concatenated_text) ## Punctuate concatenated text

    # Now we need to chunk text into main parts
    chunked_text = chunk(punctuated_text) ## Returns list of chunks
    print(f'Chunked into {len(chunked_text)} chunks.')

    # Get the timestamp of each chunk
    timestamps = timestamping(chunked_text,transcript)

    ###### SUMMARIZATION PART #########
    # Create a list of ready summaries
    summary_list = [summarize(each) for each in chunked_text]

    #Take out escape characters and punct which messes with API
    summary_list = list(map(lambda chunk : chunk.replace('\\','').replace('\"','') , summary_list))

    # Create headlines from the summaries
    headlines =[summarize(each, length=20) for each in summary_list]
    # Add headlines to the summaries + get best with higlights
    summary_list =[f"<b>{headlines[i]}</b>" + '\n\n' + get_best(each) for i,each in enumerate(summary_list)]
    # # Create Html tags for best words and sents
    # summary_list = [ for each in summary_list]
    #Add timestamps to summaries
    summary_list = [timestamps[i] + ' ' + each for i,each in enumerate(summary_list)]




    # Create an concatenated summary from summary_list

    # Join the resulting summary list into one text
    title = video_name(video_id)
    summary = '\n\n'.join(summary_list)

    summary = f"<h2>{title}</h2> \n\n\n {summary}"



    # Return the result to streamlit
    st.markdown(summary, unsafe_allow_html=True)
    #YouTubeVideo(video_id)


    #### SAVE TEXT FILE TO PROCESS LATER ####
    with open(f'results/{video_id}.txt', 'w') as f:
        f.write(summary)
        f.close()
    st.video(link)

# If we already have the summary of some video - return it
elif summary:

    my_bar = st.progress(0)


    for percent_complete in range(100):
        time.sleep(random.uniform(0, 0.4))
        my_bar.progress(percent_complete + 1)

    summary = ''
    with open(f"results/{text_file}", 'r') as f:
        for line in f.readlines():
            summary+=line
    st.markdown(summary, unsafe_allow_html=True)
    st.video(link)








st.markdown("""<b>Created by Francesco Puglia with inspiration of Indinan Guy</b>""", unsafe_allow_html=True)
