import google.generativeai as genai
import os
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
import torch
#from google.cloud import aiplatform

with open('./main/env.json') as f:
    config = json.load(f)


def call_api(text):
    genai.configure(api_key=config['provider']['gemini']['key'])

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Is the following SMS message a voice phishing scam? If correct, answer with 0; if incorrect, answer with 1.\n\n{text}")
    print(response.text)

    return response.text


def call_model(text):
    model_path = './main/g-results/checkpoint-18'# + config['model']['id']
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)

    # 로짓 값에서 가장 높은 값의 클래스 ID 선택
    logits = outputs.logits
    predicted_class_id = torch.argmax(logits, dim=-1).item()
    return predicted_class_id



#call_model("Hi~")

#call_api("abcde")