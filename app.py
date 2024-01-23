from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image_data,user_prompt):
  response=model.generate_content([input,image_data[0],user_prompt])
  return response.text
with st.sidebar:  
  st.image('skull.jpg',caption='Skull decoration')
def input_image_details(uploaded_file):
  if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    image_parts=[{'mime_type':uploaded_file.type,'data':bytes_data}]
    return image_parts

  else:
    raise FileNotFoundError('No file uploaded')

st.header('Harr cheez mein Darr hai') 

input=st.text_input('Input Prompt',key='input')
uploaded_file=st.file_uploader('Image',type=['jpg','jpeg','png'])

if uploaded_file is not None:
  image=Image.open(uploaded_file)
  st.image(image,caption='Uploaded File',use_column_width=True)

sub=st.button('TELL ME THEIR STORY')
input_prompt="""You are a storywriter and an expert in sentiment analysis. We will upload an image and you will have to write a horror story based on the image's content"""

if sub:
  with st.spinner('cooking up the tale...'):
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader('STORYTIME:')
    st.text_area(label="",value=response,height=500)
