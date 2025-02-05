from flask import Flask, request, render_template, send_file
import re
import os

def join_wrapped_lines(text):
    # Join lines that don't end with period/question/exclamation marks
    sentences = []
    current = []
    
    for line in text.split('\n'):
        if not line.strip():
            if current:
                sentences.append(' '.join(current))
                current = []
            continue
        
        if line.strip()[-1] in '.!?':
            current.append(line.strip())
            sentences.append(' '.join(current))
            current = []
        else:
            current.append(line.strip())
    
    if current:
        sentences.append(' '.join(current))
    
    return '\n'.join(sentences)

def add_sentence_spacing(text):
    # Add space after periods/question marks/exclamation marks if not present
    return re.sub(r'([.!?])([A-Z])', r'\1 \2', text)

def clean_srt_content(srt_content):
    # Remove UTF-8 BOM if present
    srt_content = srt_content.replace('\ufeff', '')
    
    # Remove DOS line endings
    srt_content = srt_content.replace('\r', '')
    
    # Split into lines for processing
    lines = srt_content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip if line is only numbers (subtitle numbers)
        if line.strip().isdigit():
            continue
            
        # Skip timestamp lines
        if re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', line.strip()):
            continue
            
        # Remove HTML/XML tags
        line = re.sub(r'<[^>]*>', '', line)
        
        # Add non-empty lines
        if line.strip():
            cleaned_lines.append(line.strip())
    
    # Join lines and fix spacing
    text = '\n'.join(cleaned_lines)
    text = join_wrapped_lines(text)
    text = add_sentence_spacing(text)
    
    return text

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    cleaned_text = None
    file_link = None
    if request.method == 'POST':
        if 'text_input' in request.form and request.form['text_input'].strip():
            srt_content = request.form['text_input']
            cleaned_text = clean_srt_content(srt_content)
        elif 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file.filename.endswith('.srt'):
                srt_content = uploaded_file.read().decode('utf-8')
                cleaned_text = clean_srt_content(srt_content)
                with open("output.txt", "w", encoding="utf-8") as f:
                    f.write(cleaned_text)
                file_link = '/download'
    return render_template('index.html', cleaned_text=cleaned_text, file_link=file_link)

@app.route('/download')
def download():
    return send_file("output.txt", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
