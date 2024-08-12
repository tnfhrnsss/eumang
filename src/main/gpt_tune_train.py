from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import load_dataset

import json

with open('env.json') as f:
    config = json.load(f)

dataset = load_dataset("text", data_files={"train": "dataset/train_data_output.txt", "test": "dataset/test_data.txt"})

# 2. 토크나이저 및 모델 불러오기
tokenizer = GPT2Tokenizer.from_pretrained('gpt2', model_max_length=1024)
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model = GPT2LMHeadModel.from_pretrained('gpt2')


# 3. 데이터셋 전처리
def tokenize_function(examples):
    # input_ids를 생성
    inputs = tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)
    # labels를 input_ids와 동일하게 설정
    inputs["labels"] = inputs["input_ids"].copy()
    return inputs


tokenized_datasets = dataset.map(tokenize_function, batched=True)


# 4. 학습 설정
training_args = TrainingArguments(
    output_dir="results",
    evaluation_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
)

# 5. 트레이너 초기화
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# 6. 모델 학습
trainer.train()

# 7. 모델 저장
trainer.save_model(config['model']['id'])
