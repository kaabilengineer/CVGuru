from flask import Flask, request, render_template, flash, redirect, send_file, url_for,session, Response, render_template_string
from subjective import SubjectiveTest
import nltk
import pdfkit
import os
app = Flask(__name__)

pdf_file = request.files['pdf_file']
job_title = request.form.get('job_title')  # Retrieve job title from the form

if pdf_file.filename == '':
    print("No selected file")
import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyBcv7SmYX416WBX5nkm3h5fuiM4zUhpiL4")

# Create the model
generation_config = {
"temperature": 1,
"top_p": 0.95,
"top_k": 40,
"max_output_tokens": 8192,
"response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
model_name="gemini-1.5-pro",
generation_config=generation_config,
)

chat_session = model.start_chat(
history=[
]
)

    pdf = PdfReader(pdf_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()

    
    basequery = 'below is the text extracted from the resume, without explaining generate 20 questions that can be asked during the interview for the role of' + job_title + ' on this resume :'

    query = basequery + text
    response = chat_session.send_message(query)
