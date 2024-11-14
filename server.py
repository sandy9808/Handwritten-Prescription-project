#!/usr/bin/env python3

import torch
import os
from PIL import Image
from flask import Flask, request, jsonify, render_template
from transformers import AutoModel, AutoTokenizer, BitsAndBytesConfig
from huggingface_hub import login
from waitress import serve

model, tokenizer = None, None
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Corrected __name__ usage
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/predictImage', methods=['POST'])
def predict_image():
    """Receives an image file via POST request, processes it with the model, and returns the extracted data."""
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    if file and file.filename != '':
        img = Image.open(file)
        
        # Prepare the prompt/message for the model
        msgs = [{'role': 'user', 'content': [img, "The image is a handwritten medical prescription. Please extract important information including patient details, diagnosis, medicine names and quantity as a detailed report from it."]}]
        
        # Run inference
        res = model.chat(image=img, msgs=msgs, tokenizer=tokenizer)
        output = {"result": res}
        
        return jsonify(output)
    else:
        return jsonify({"error": "Invalid image file"}), 400

@app.route("/")
def index_page():
    """Renders the 'index.html' page for manual image file uploads."""
    return render_template("index.html")

# Corrected __name__ usage and added waitress serve
if __name__ == '__main__':
    # Load model and tokenizer
    device = torch.device('cuda:7') if torch.cuda.is_available() else torch.device('cpu')
    print(f'Running on device: {device}')

    login("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")
    model = AutoModel.from_pretrained(
        'openbmb/MiniCPM-V-2_6', 
        trust_remote_code=True,
        attn_implementation='sdpa',
        device_map=device, 
        quantization_config=quant_config)
        
    tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V-2_6', trust_remote_code=True)

    # Start flask application on waitress WSGI server
    serve(app, host='0.0.0.0', port=5000)
