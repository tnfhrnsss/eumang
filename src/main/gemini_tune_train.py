from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
#from google.cloud import aiplatform

import json

with open('env.json') as f:
    config = json.load(f)

# 데이터 로드 (텍스트 파일 경로 수정)
dataset = load_dataset("csv", data_files={"train": "dataset/train_data_output.txt", "test": "dataset/test_data.txt"})

# 토크나이저 설정 (Flan-T5 Base 모델에 맞는 토크나이저 사용)
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small", model_max_length=512, local_files_only=True)
tokenizer.save_pretrained('./g-results/checkpoint-18/')

def tokenize_function(examples):
    # input_ids를 생성
    inputs = tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)
    # labels를 input_ids와 동일하게 설정
    #inputs["labels"] = [0] * len(examples["text"])
    inputs["labels"] = examples["label"]
    return inputs


tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 모델 로딩 (Flan-T5 Base 모델 사용)
model = AutoModelForSequenceClassification.from_pretrained("google/flan-t5-small", num_labels=2)

# 학습 설정
training_args = TrainingArguments(
    output_dir="./g-results",
    evaluation_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
)

# 트레이너 초기화
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# 모델 학습
trainer.train()

trainer.save_model(config['model']['id'])


## aiplatform.Model.upload(
   ## display_name="voice_phishing_model",
   ## artifact_uri="보이스피싱_판별기",
   ## serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/tf2-cpu",
## )


