import torch
from transformers import LlamaTokenizer, LlamaForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model 
from custom_datasets import BloomTranscript

dataset_fn = '../data_prep/_dataset.txt'
model_dir = 'models/llama/'

tokenizer = LlamaTokenizer.from_pretrained("decapoda-research/llama-7b-hf", pad_token='<|pad|>')
model = LlamaForCausalLM.from_pretrained("decapoda-research/llama-7b-hf", device_map='auto', load_in_8bit=True)
model.resize_token_embeddings(len(tokenizer))

for param in model.parameters():
  param.requires_grad = False
  if param.ndim == 1:
    param.data = param.data.to(torch.float32)

model.gradient_checkpointing_enable()
model.enable_input_require_grads()

class CastOutputToFloat(torch.nn.Sequential):
  def forward(self, x): return super().forward(x).to(torch.float32)
model.lm_head = CastOutputToFloat(model.lm_head)

def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, config)
print_trainable_parameters(model)

dataset_f = open(dataset_fn, 'r', encoding='utf-8')
dataset = BloomTranscript(dataset_f.read(), tokenizer)
dataset_f.close()

trainer = Trainer(
    model=model, 
    train_dataset=dataset,
    args=TrainingArguments(
        per_device_train_batch_size=1, 
        gradient_accumulation_steps=4,
        num_train_epochs=1,
        warmup_steps=100, 
        fp16=True,
        logging_steps=1, 
        output_dir=model_dir
    ),
    data_collator=lambda data: {
                'input_ids': torch.stack([f[0] for f in data]),
                'attention_mask': torch.stack([f[1] for f in data]),
                'labels': torch.stack([f[0] for f in data])
            }
)
model.config.use_cache = False
trainer.train(model_dir + 'checkpoint-1500')

trainer.save_model(model_dir + 'llama_final.pt')

