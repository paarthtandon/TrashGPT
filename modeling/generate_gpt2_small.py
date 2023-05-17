import torch
import torch.nn.functional as F
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from tqdm import trange
import time

device = torch.device("cuda")

tokenizer = GPT2Tokenizer.from_pretrained('gpt2', pad_token='<|pad|>')
model = GPT2LMHeadModel.from_pretrained('gpt2')
model.resize_token_embeddings(len(tokenizer))
model.load_state_dict(torch.load('models/gpt2_small_final/pytorch_model.bin'), strict=False)
model.to(device)

text = "<title> the differences between japanese and american people </title>\n"
input_ids = tokenizer.encode(text, return_tensors='pt').to(device)

print('Starting generation')
start = time.time()

sample_output = model.generate(
    input_ids=input_ids, 
    do_sample=True, 
    max_length=1024,
    temperature=0.7,
    repetition_penalty=1.05
)

print(tokenizer.decode(sample_output[0], skip_special_tokens=True))
print('Time taken:', time.time() - start)
