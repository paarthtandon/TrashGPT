import torch
from datasets import load_dataset
from peft import LoraConfig, PeftModel, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    AutoTokenizer,
    TrainingArguments,
    GenerationConfig
)
from trl import SFTTrainer
from custom_datasets import LLaMA2Transcript

dataset_fn = '../data_prep/_dataset.txt'
checkpoint_dir = '../checkpoints/'
model_name = 'meta-llama/Llama-2-7b-hf'

#Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

print('Loaded Tokenizer')

#Create a new token and add it to the tokenizer
tokenizer.add_special_tokens({"pad_token":"<pad>"})
tokenizer.padding_side = 'left'

dataset_f = open(dataset_fn, 'r', encoding='utf-8')
dataset = LLaMA2Transcript(dataset_f.read(), tokenizer)
dataset_f.close()

print('Loaded Dataset')

compute_dtype = getattr(torch, "float16")
bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=True,
)
model = AutoModelForCausalLM.from_pretrained(
          model_name, quantization_config=bnb_config, device_map={"": 0}
)

#Resize the embeddings
model.resize_token_embeddings(len(tokenizer))
#Configure the pad token in the model
model.config.pad_token_id = tokenizer.pad_token_id
model.config.use_cache = False # Gradient checkpointing is used by default but not compatible with caching

model = prepare_model_for_kbit_training(model)
peft_config = LoraConfig(
        lora_alpha=32,
        lora_dropout=0.1,
        r=8,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules= ["q_proj","v_proj"]
)

print('Loaded Model')

training_arguments = TrainingArguments(
        output_dir="../checkpoints",
        evaluation_strategy="no",
        do_eval=False,
        per_device_train_batch_size=3,
        gradient_accumulation_steps=1,
        log_level="debug",
        optim="paged_adamw_32bit",
        save_steps=500, #change to 500
        logging_steps=10, #change to 100
        learning_rate=1e-4,
        fp16=True,
        max_grad_norm=0.3,
        num_train_epochs=3, # remove "#"
        warmup_ratio=0.03,
        lr_scheduler_type="constant",
)

trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="text",
        max_seq_length=4096,
        tokenizer=tokenizer,
        args=training_arguments,
        data_collator=lambda data: {
            'input_ids': torch.stack([f[0] for f in data]),
            'attention_mask': torch.stack([f[1] for f in data]),
            'labels': torch.stack([f[0] for f in data])
        }
)

trainer.train()
