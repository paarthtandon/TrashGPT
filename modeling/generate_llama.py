import torch
from transformers import LlamaTokenizer, LlamaForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model 
from peft import PeftModel, PeftConfig
from custom_datasets import BloomTranscript
import time

device = torch.device("cuda")

tokenizer = LlamaTokenizer.from_pretrained("decapoda-research/llama-7b-hf", pad_token='<|pad|>')
model = LlamaForCausalLM.from_pretrained("decapoda-research/llama-7b-hf", device_map='auto', load_in_8bit=True)
model.resize_token_embeddings(len(tokenizer))

for param in model.parameters():
  param.requires_grad = False  # freeze the model - train adapters later
  if param.ndim == 1:
    # cast the small parameters (e.g. layernorm) to fp32 for stability
    param.data = param.data.to(torch.float32)

model.gradient_checkpointing_enable()  # reduce number of stored activations
model.enable_input_require_grads()

class CastOutputToFloat(torch.nn.Sequential):
  def forward(self, x): return super().forward(x).to(torch.float32)
model.lm_head = CastOutputToFloat(model.lm_head)


config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, config)
model.load_state_dict(torch.load('models/llama_final/pytorch_model.bin'))

# encode context the generation is conditioned on
input_ids = tokenizer.encode('<title>', return_tensors='pt').to(device)

print('Starting generation')
start = time.time()

with torch.cuda.amp.autocast():
    # activate sampling and deactivate top_k by setting top_k sampling to 0
    sample_output = model.generate(
        input_ids=input_ids, 
        do_sample=True, 
        max_length=2048,
        temperature=0.7,
        repetition_penalty=1.1
    )

print(tokenizer.decode(sample_output[0], skip_special_tokens=True))
print('Time taken:', time.time() - start)
