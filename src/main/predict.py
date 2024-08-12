def predict_fraudulent_text(model, tokenizer, text):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = logits.argmax(dim=-1).item()
    return prediction

# 예측 예제
model = GPT2LMHeadModel.from_pretrained('./gpt_finetuned')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

is_fraudulent = predict_fraudulent_text(model, tokenizer, clean_text)
if is_fraudulent:
    print("보이스 피싱 패턴이 감지되었습니다.")
else:
    print("정상적인 메시지입니다.")
