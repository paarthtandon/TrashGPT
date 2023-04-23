import pandas as pd
import torch
from torch.utils.data import Dataset, random_split
from transformers import GPT2Tokenizer, TrainingArguments, Trainer, GPT2LMHeadModel
from custom_datasets import GPT2Transcript

dataset_fn = '../annotated_w_names/_dataset.txt'
model_dir = 'models/gpt_med'

tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium', pad_token='<|pad|>')
model = GPT2LMHeadModel.from_pretrained('gpt2-medium').cuda()
model.resize_token_embeddings(len(tokenizer))

dataset_f = open(dataset_fn, 'r', encoding='utf-8')
dataset = GPT2Transcript(dataset_f.read(), tokenizer)
dataset_f.close()

torch.cuda.empty_cache()

training_args = TrainingArguments(output_dir=model_dir,
                                  num_train_epochs=2,
                                  logging_steps=100,
                                  save_steps=5000,
                                  per_device_train_batch_size=1,
                                  per_device_eval_batch_size=1,
                                  warmup_steps=10,
                                  weight_decay=0.05,
                                  logging_dir=model_dir,
                                  report_to='none')

trainer = Trainer(model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=lambda data: {
                'input_ids': torch.stack([f[0] for f in data]),
                'attention_mask': torch.stack([f[1] for f in data]),
                'labels': torch.stack([f[0] for f in data])
            }
        )

trainer.train()

