### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
    response=get_gemini_repsonse(input_prompt,input)
    st.subheader("The Response is")
    st.write(response)    
    else:
        raise FileNotFoundError("No info provided")
    
##initialize our streamlit app

st.set_page_config(page_title="Micronutrients Calculator")

st.header("Micronutrients Calculator")
input=st.text_input("Insert the Ingredient list: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Micronutrients calculation")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate each micronutrient in the final recipe, or calculate it from the ingredient list, recipe provided in input as text.
               first list all the ingredients in below format:
For total amount of "insert dish name" in the pic (mentions grams of dish), the ingredients used are: ingredient 1 (weight in grams), ingredient 2 (weight in grams).....
               Then also provide the details of every micronutrient in below tabular format:

               Micronutrients Name   amount per 100 gm
               1. Micronutrient 1 - amount per 100 gms
               2. Micronutrient 1 - amount per 100 gms
               ----
               ----


"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)


