from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer, TrainingArguments
import pandas as pd
import json
import torch

# Load the dataset
def load_dataset(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Prepare dataset for training
class InterviewDataset(torch.utils.data.Dataset):
    def __init__(self, data, tokenizer, max_input_length=128, max_output_length=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_input_length = max_input_length
        self.max_output_length = max_output_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        input_text = item['input']
        output_text = item['output']

        inputs = self.tokenizer(
            input_text,
            max_length=self.max_input_length,
            truncation=True,
            padding='max_length',
            return_tensors="pt",
        )
        outputs = self.tokenizer(
            output_text,
            max_length=self.max_output_length,
            truncation=True,
            padding='max_length',
            return_tensors="pt",
        )

        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze(),
            'labels': outputs['input_ids'].squeeze(),
        }

# Load tokenizer and model
model_name = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

# Load the dataset
dataset_file = "interview_dataset.json"
raw_data = load_dataset(dataset_file)

# Prepare the dataset
train_dataset = InterviewDataset(raw_data, tokenizer)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./pegasus_finetuned",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=4,
    num_train_epochs=3,
    save_steps=500,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=100,
    load_best_model_at_end=True,
)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./pegasus_finetuned")
tokenizer.save_pretrained("./pegasus_finetuned")
