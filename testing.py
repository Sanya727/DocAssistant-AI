import quart
from quart import Quart, render_template, request, send_from_directory
from langchain.pipeline import TextPipeline
import os

app = Quart(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'  # Directory to store uploaded PDFs

@app.route('/')
async def index():
    return await render_template('index2.html')

@app.route('/upload', methods=['POST'])
async def upload_file():
    if 'file' not in (await quart.request.files):
        return 'No file part'

    file = (await quart.request.files)['file']
    if file.filename == '':
        return 'No selected file'

    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    await file.save(filename)
    return await render_template('upload_success.html', filename=file.filename)

@app.route('/qa', methods=['GET', 'POST'])
async def qa():
    if quart.request.method == 'POST':
        question = (await quart.request.form)['question']
        pdf_file = (await quart.request.form)['pdf_file']
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file)

        # Use LangChain or another library to process the PDF and answer the question
        pipeline = TextPipeline()
        answer = pipeline.process_pdf(pdf_path, question)

        return await render_template('qa.html', question=question, answer=answer)

    return await render_template('qa.html')

@app.route('/uploads/<filename>')
async def uploaded_file(filename):
    return await send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
