from flask import Flask, request, render_template, flash, redirect, send_file, url_for,session, Response, render_template_string, jsonify
from subjective import SubjectiveTest
import nltk
import pdfkit
import os
import pdfplumber

app = Flask(__name__)

app.secret_key= 'aica2'

# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# # Download all NLTK data
# nltk.download('all')
import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyBcv7SmYX416WBX5nkm3h5fuiM4zUhpiL4")

from PyPDF2 import PdfFileReader, PdfReader
from flask import Flask, request

from pdfminer.high_level import extract_text



# Model configuration
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

@app.route('/')
def index():
	return render_template('front.html')

@app.route('/predict')
def index1():
     return render_template('predict.html')
     
@app.route('/test_generate', methods=['POST'])
def test_generate():
    if 'pdf_file' not in request.files:
        return "No file part in the request."

    file = request.files['pdf_file']
    job_title = request.form.get('job_title', '')

    if file.filename == '':
        return "No file selected."

    # Extract text from the PDF file
    text_content = ""
    if file and file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text_content += page.extract_text() + "\n"

    # Prepare query for Google Generative AI
    basequery = (
        "Below is the text extracted from the resume. Without explaining, generate "
        f"20 questions that can be asked during the interview for the role of {job_title} based on this resume:"
    )
    query = basequery + text_content

    # Start chat session and send query
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(query)

    # Extract response as questions list
    questions = response.text.split("\n") if response.text else ["No questions generated."]

    # Render questions to HTML template
    return render_template('predict.html', cresults=questions)
        

@app.route("/generate")
def gen():
     return render_template('generate.html')

def generate_unique_filename(base_path, base_name, extension):
    """
    Generate a unique filename by adding an index if the file already exists.
    """
    counter = 1
    file_path = f"{base_path}{base_name}{extension}"
    while os.path.exists(file_path):
        file_path = f"{base_path}{base_name}_{counter}{extension}"
        counter += 1
    return file_path


@app.route("/aienhancement", methods=['GET', 'POST'])
def ai_enhancement():
    if request.method == 'POST':
        # Retrieve personal information
        name = request.form['name']
        email = request.form['email']
        linkedin = request.form.get('linkedin', '')
        contact = request.form['contact']

        # Retrieve experience data
        experiences = []
        companies = request.form.getlist('experience_company[]')
        roles = request.form.getlist('experience_role[]')
        keypoints1 = request.form.getlist('experience_keypoint1[]')
        keypoints2 = request.form.getlist('experience_keypoint2[]')
        keypoints3 = request.form.getlist('experience_keypoint3[]')
        
        for i in range(len(companies)):
            keypoints = [kp for kp in [keypoints1[i], keypoints2[i], keypoints3[i]] if kp]
            experiences.append({
                'company': companies[i],
                'role': roles[i],
                'keypoints': keypoints
            })

        # Retrieve projects data
        projects = []
        project_names = request.form.getlist('project_name[]')
        project_keypoints1 = request.form.getlist('project_keypoint1[]')
        project_keypoints2 = request.form.getlist('project_keypoint2[]')
        project_keypoints3 = request.form.getlist('project_keypoint3[]')

        for i in range(len(project_names)):
            keypoints = [kp for kp in [project_keypoints1[i], project_keypoints2[i], project_keypoints3[i]] if kp]
            projects.append({
                'name': project_names[i],
                'keypoints': keypoints
            })

        # Retrieve education data
        education = []
        colleges = request.form.getlist('education_college[]')
        degrees = request.form.getlist('education_degree[]')
        percentages = request.form.getlist('education_percentage[]')

        for i in range(len(colleges)):
            education.append({
                'college': colleges[i],
                'degree': degrees[i],
                'percentage': percentages[i]
            })

        # Retrieve certifications data
        certifications = request.form.getlist('certification_name[]')

        # Generate HTML content
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
            color: #333;
            line-height: 1.6;
        }}
        .container {{
            width: 80%;
            margin: 0 auto;
        }}
        h1, h2, h3 {{
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        p {{
            margin: 5px 0;
        }}
        hr {{
            border: 0;
            height: 1px;
            background: #ccc;
            margin: 20px 0;
        }}
        ul {{
            list-style-type: disc;
            margin-left: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{name}</h1>
        <p>Email: {email}</p>
        <p>Contact: {contact}</p>
        {f'<p>LinkedIn: {linkedin}</p>' if linkedin else ''}
        <hr>

        <h2>Experience</h2>
        {''.join([f"<h3>{exp['company']} - {exp['role']}</h3><ul>{''.join([f'<li>{kp}</li>' for kp in exp['keypoints']])}</ul>" for exp in experiences])}
        <hr>

        <h2>Projects</h2>
        {''.join([f"<h3>{proj['name']}</h3><ul>{''.join([f'<li>{kp}</li>' for kp in proj['keypoints']])}</ul>" for proj in projects])}
        <hr>

        <h2>Education</h2>
        {''.join([f"<h3>{edu['college']}</h3><p>{edu['degree']}, {edu['percentage']}%</p>" for edu in education])}
        <hr>

        <h2>Certifications</h2>
        <ul>
            {''.join([f"<li>{cert}</li>" for cert in certifications])}
        </ul>
    </div>
</body>
</html>
"""
        basequery = (
        "Below is the html fromat of a the resume. Without explaining, generate "
        f"10 suggestions on the keypoints based on this resume:"
        )
        query = basequery + html_content

        # Start chat session and send query
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(query)

        suggestions = response.text.split("\n") if response.text else [""]

    # Render questions to HTML template
    
        return render_template('suggestions.html', suggestions=suggestions)
    
    return render_template('suggestions.html', suggestions=[])
    


@app.route("/generatepdf", methods=['POST'])
def generate():
    if request.method == "POST":
        # Retrieve personal information
        name = request.form['name']
        email = request.form['email']
        linkedin = request.form.get('linkedin', '')
        contact = request.form['contact']

        # Retrieve experience data
        experiences = []
        companies = request.form.getlist('experience_company[]')
        roles = request.form.getlist('experience_role[]')
        keypoints1 = request.form.getlist('experience_keypoint1[]')
        keypoints2 = request.form.getlist('experience_keypoint2[]')
        keypoints3 = request.form.getlist('experience_keypoint3[]')
        
        for i in range(len(companies)):
            keypoints = [kp for kp in [keypoints1[i], keypoints2[i], keypoints3[i]] if kp]
            experiences.append({
                'company': companies[i],
                'role': roles[i],
                'keypoints': keypoints
            })

        # Retrieve projects data
        projects = []
        project_names = request.form.getlist('project_name[]')
        project_keypoints1 = request.form.getlist('project_keypoint1[]')
        project_keypoints2 = request.form.getlist('project_keypoint2[]')
        project_keypoints3 = request.form.getlist('project_keypoint3[]')

        for i in range(len(project_names)):
            keypoints = [kp for kp in [project_keypoints1[i], project_keypoints2[i], project_keypoints3[i]] if kp]
            projects.append({
                'name': project_names[i],
                'keypoints': keypoints
            })

        # Retrieve education data
        education = []
        colleges = request.form.getlist('education_college[]')
        degrees = request.form.getlist('education_degree[]')
        percentages = request.form.getlist('education_percentage[]')

        for i in range(len(colleges)):
            education.append({
                'college': colleges[i],
                'degree': degrees[i],
                'percentage': percentages[i]
            })

        # Retrieve certifications data
        certifications = request.form.getlist('certification_name[]')

        # Generate HTML content
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
            color: #333;
            line-height: 1.6;
        }}
        .container {{
            width: 80%;
            margin: 0 auto;
        }}
        h1, h2, h3 {{
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        p {{
            margin: 5px 0;
        }}
        hr {{
            border: 0;
            height: 1px;
            background: #ccc;
            margin: 20px 0;
        }}
        ul {{
            list-style-type: disc;
            margin-left: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{name}</h1>
        <p>Email: {email}</p>
        <p>Contact: {contact}</p>
        {f'<p>LinkedIn: {linkedin}</p>' if linkedin else ''}
        <hr>

        <h2>Experience</h2>
        {''.join([f"<h3>{exp['company']} - {exp['role']}</h3><ul>{''.join([f'<li>{kp}</li>' for kp in exp['keypoints']])}</ul>" for exp in experiences])}
        <hr>

        <h2>Projects</h2>
        {''.join([f"<h3>{proj['name']}</h3><ul>{''.join([f'<li>{kp}</li>' for kp in proj['keypoints']])}</ul>" for proj in projects])}
        <hr>

        <h2>Education</h2>
        {''.join([f"<h3>{edu['college']}</h3><p>{edu['degree']}, {edu['percentage']}%</p>" for edu in education])}
        <hr>

        <h2>Certifications</h2>
        <ul>
            {''.join([f"<li>{cert}</li>" for cert in certifications])}
        </ul>
    </div>
</body>
</html>
"""

        # Generate PDF from HTML content
        base_path = 'generatedresume/'
        base_name = name.split()[0] + '_resume'
        pdf_path = generate_unique_filename(base_path, base_name, '.pdf')

        pdfkit.from_string(html_content, pdf_path)

        # Return the generated PDF path
        return render_template('downloadpdf.html', pdf_path=pdf_path)

    return render_template('cantdownload.html')


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
	app.run(debug=True)







    