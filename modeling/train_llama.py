import torch
from transformers import LlamaTokenizer, LlamaForCausalLM, TrainingArguments, Trainer
from custom_datasets import BloomTranscript

dataset_fn = '../annotated_w_names/_dataset.txt'
model_dir = 'models/llama'

tokenizer = LlamaTokenizer.from_pretrained("decapoda-research/llama-7b-hf")
model = LlamaForCausalLM.from_pretrained("decapoda-research/llama-7b-hf").cuda()

dataset_f = open(dataset_fn, 'r', encoding='utf-8')
dataset = BloomTranscript(dataset_f.read(), tokenizer)
dataset_f.close()

torch.cuda.empty_cache()

training_args = TrainingArguments(output_dir=model_dir,
                                  num_train_epochs=2,
                                  logging_steps=10,
                                  # save_steps=100,
                                  save_steps=5000,
                                  per_device_train_batch_size=1,
                                  per_device_eval_batch_size=1,
                                  warmup_steps=10,
                                  weight_decay=0.05,
                                  logging_dir=model_dir,
                                  report_to='none',
                                  fp16=True,
                                  gradient_accumulation_steps=4,
                                  gradient_checkpointing=True)

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
trainer.save_model(model_dir + 'llama_final.pt')

