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
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Micronutrients Calculator")

st.header("Micronutrients Calculator")
input=st.text_input("You can share any additional info for the dish here: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Calculate the Micronutrients")

input_prompt="""
You are an expert nutritionist where you need to see the food items from the image, figure out the ingredients, exclude ingredients that are optional and are not evidently visible in the pic.
               and calculate the micronutrients, 
               First provide the list of ingredients in following format:
               For amount of dish_name in grams, inredients are: ingredient 1 (amount in grams), ingredient 2 (amount in grams), ...
               Then in a professionally presentable tabular form, provide the details of every micronutrient including the fatty acids and other minutely calculabe micronutrients per 100 gm of the dish
               in the below format

                  Name                Amount per 100 gm
               1. Micronutrient 1 - amount per 100 gm
               2. Micronutrient 1 - amount per 100 gm
               ----
               ----


"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("Here's the Micronutrient information you requested: ")
    st.write(response)

