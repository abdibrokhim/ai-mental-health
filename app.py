# Import from standard library
import os
import logging
import time

# Import from 3rd party libraries
import streamlit as st

# Import modules from the local package
import stable_diffusion, chroma_cohere, eleven_labs, video_gen, helper, clean_up



def generate_shorts():

    st.session_state.text_error = ""

    if st.session_state.cohere_api_key == "" or st.session_state.elevenlabs_api_key == "" or st.session_state.stable_diffusion_api_key == "":
        st.session_state.text_error = "Missed API key."
        return


    st.session_state.text_error = ""

    if st.session_state.file_path == "" or st.session_state.query == "":
        st.session_state.text_error = "Missed a file or query."
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while we process your query..."):
            print('st.session_state.cohere_api_key:', st.session_state.cohere_api_key)

            prompt = chroma_cohere.generate_prompt(query=st.session_state.query, file_path=st.session_state.file_path, cohere_api_key=st.session_state.cohere_api_key)

            if prompt == "":
                st.session_state.text_error = "Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again."
                logging.info(f"Text Error: {st.session_state.text_error}")
                return
            
            st.session_state.prompt_generate = (prompt)


    st.session_state.text_error = ""

    if len(st.session_state.prompt_generate) == len("I don't know") or st.session_state.prompt_generate == "":
        st.session_state.text_error = "Something went wrong. Please refresh the page and try again."
        st.session_state.prompt_generate = ""
        return
        # generate_shorts()

    
    st.session_state.text_error = ""

    with texts_spinner_placeholder:
        with st.spinner("Please wait while we preprocess response..."):

            clean_text_list = helper.clean_text(st.session_state.prompt_generate)

            print('clean_text_list:', clean_text_list)

            
            clean_text = helper.make_text(clean_text_list)

            print('clean_text:', clean_text)

    
    with image_spinner_placeholder:
        with st.spinner("Please wait while we generating images..."):

            st.session_state.text_error = ""

            if clean_text_list == []:
                st.session_state.text_error = "Something went wrong. Please refresh the page and try again."
                return
            
            img_path = stable_diffusion.imagine(prompt_list=clean_text_list, stable_diffusion_api_key=st.session_state.stable_diffusion_api_key)

            if img_path == "":
                st.session_state.text_error = "Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again."
                logging.info(f"Text Error: {st.session_state.text_error}")
                return
            
            st.session_state.img_path = (img_path)


    with audio_spinner_placeholder:
        with st.spinner("Please wait while we generating audio..."):

            st.session_state.text_error = ""

            st.session_state.audio_path = (eleven_labs.with_premade_voice(prompt=clean_text, voice="Bella", elevenlabs_api_key=st.session_state.elevenlabs_api_key))

            if st.session_state.audio_path == "":
                st.session_state.text_error = "Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again."
                logging.info(f"Text Error: {st.session_state.text_error}")
                return


    with shorts_spinner_placeholder:
        with st.spinner("Please wait a bit more while we generating your shorts..."):
            folder_path = st.session_state.img_path
            audio_path = st.session_state.audio_path
            video_path_name = "static/output/result.mp4"

            video_gen.MP3ToMP4(folder_path, audio_path, video_path_name)

            time.sleep(5)

            st.session_state.video_path = ("static/output/result.mp4")
    

    clean_up.clean_up()




# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)



# Configure Streamlit page and state
st.set_page_config(page_title="Imagine", page_icon="🍩")



# Store the initial value of widgets in session state
if "imagine" not in st.session_state:
    st.session_state.imagine = ""

if "query" not in st.session_state:
    st.session_state.query = ""

if "img_path" not in st.session_state:
    st.session_state.img_path = ""

if "video_path" not in st.session_state:
    st.session_state.video_path = ""

if "audio_path" not in st.session_state:
    st.session_state.audio_path = ""

if "prompt_generate" not in st.session_state:
    st.session_state.prompt_generate = ""

if "file_path" not in st.session_state:
    st.session_state.file_path = ""

if "text_error" not in st.session_state:
    st.session_state.text_error = ""

if "cohere_api_key" not in st.session_state:
    st.session_state.cohere_api_key = ""

if "elevenlabs_api_key" not in st.session_state:
    st.session_state.elevenlabs_api_key = ""

if "stable_diffusion_api_key" not in st.session_state:
    st.session_state.stable_diffusion_api_key = ""

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"



# Force responsive layout for columns also on mobile
st.write(
    """
    <style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# Render Streamlit page
with st.sidebar:
    st.session_state.cohere_api_key = st.text_input('Cohere API Key', )
    st.session_state.elevenlabs_api_key = st.text_input('ElevenLabs API Key', )
    st.session_state.stable_diffusion_api_key = st.text_input('Stable Diffusion API Key', )


# title of the app
st.title("MindSpeak: Visualizing Mental Health Support")


# st.markdown(
#     "This is a demo of YouTube shorts generator."
# )


# file upload
file = st.file_uploader(label="Upload file", type=["pdf",])
if file is not None:
    filename = "static/files/book.pdf"
    with open(filename, "wb") as f:
        f.write(file.getbuffer())
    st.session_state.file_path = "static/files/book.pdf"


# textarea
st.session_state.query = st.text_area(
    label="Query the document",
    placeholder="Tell about Depression, its causes and factors.", height=100)


# button
st.button(
    label="Generate Prompt",
    help="Click to genearate prompt",
    key="generate_prompt",
    type="primary",
    on_click=generate_shorts,
    )


text_spinner_placeholder = st.empty()


if st.session_state.prompt_generate:
    st.markdown("""---""")
    st.text_area(label="Generated Prompt", value=st.session_state.prompt_generate,)


texts_spinner_placeholder = st.empty()
audio_spinner_placeholder = st.empty()
image_spinner_placeholder = st.empty()
shorts_spinner_placeholder = st.empty()


if st.session_state.text_error:
    st.error(st.session_state.text_error)


if st.session_state.video_path:
    st.markdown("""---""")
    st.subheader("YouTube Shorts generated by Stable Diffusion and Eleven Labs")
    video_file = open(st.session_state.video_path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes, format="video/mp4", start_time=0)

