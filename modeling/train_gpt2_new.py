import torch
from transformers import GPT2Tokenizer, TrainingArguments, Trainer, GPT2LMHeadModel
from custom_datasets import GPT2Transcript

dataset_fn = '../annotated_w_names/_dataset.txt'
model_dir = 'models/gpt_small'

tokenizer = GPT2Tokenizer.from_pretrained('gpt2', pad_token='<|pad|>')
model = GPT2LMHeadModel.from_pretrained('gpt2').cuda()
model.resize_token_embeddings(len(tokenizer))

dataset_f = open(dataset_fn, 'r', encoding='utf-8')
dataset = GPT2Transcript(dataset_f.read(), tokenizer)
dataset_f.close()

torch.cuda.empty_cache()

training_args_small = TrainingArguments(output_dir=model_dir,
                                  num_train_epochs=2,
                                  logging_steps=100,
                                  save_steps=5000,
                                  per_device_train_batch_size=2,
                                  per_device_eval_batch_size=2,
                                  warmup_steps=10,
                                  weight_decay=0.05,
                                  logging_dir=model_dir,
                                  report_to='none')

training_args_med = TrainingArguments(output_dir=model_dir,
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
        args=training_args_small,
        train_dataset=dataset,
        data_collator=lambda data: {
                'input_ids': torch.stack([f[0] for f in data]),
                'attention_mask': torch.stack([f[1] for f in data]),
                'labels': torch.stack([f[0] for f in data])
            }
        )

trainer.train()
trainer.save_model(model_dir + 'gpt2small_final.pt')
