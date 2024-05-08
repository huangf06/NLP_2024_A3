import os
from flask import Flask, render_template, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

model = GPT2LMHeadModel.from_pretrained('distilgpt2')
tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    emotion = request.form['emotion']
    style = request.form['style']
    modified_prompt = f"{emotion} {style} {prompt}"

    inputs = tokenizer.encode(modified_prompt, return_tensors='pt')
    outputs = model.generate(
        inputs,
        max_length=256,
        num_return_sequences=1,
        no_repeat_ngram_size=3,
        temperature=0.8,
        top_k=50,
        top_p=0.92,
        eos_token_id=tokenizer.eos_token_id
    )

    poem = tokenizer.decode(outputs[0], skip_special_tokens=True)

    lines = poem.strip().split('\n')
    if lines:
        last_line = lines[-1]
        if '.' not in last_line and ',' not in last_line:
            lines = lines[:-1]
    poem = '\n'.join(lines)

    return jsonify({'poem': poem})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
