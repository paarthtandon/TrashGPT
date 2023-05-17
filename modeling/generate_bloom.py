import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, BloomForCausalLM
from tqdm import trange
import time

device = torch.device("cuda")

tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m")
model = BloomForCausalLM.from_pretrained("bigscience/bloom-560m").cuda()
model.load_state_dict(torch.load('models/bloom_560_final/pytorch_model.bin'))

text = "<title> the differences between japanese and american people </title>\n"
input_ids = tokenizer.encode(text, return_tensors='pt').to(device)

print('Starting generation')
start = time.time()

sample_output = model.generate(
    input_ids=input_ids, 
    do_sample=True, 
    max_length=2048,
    temperature=0.7,
    repetition_penalty=1.0
)

print(tokenizer.decode(sample_output[0], skip_special_tokens=True))
print('Time taken:', time.time() - start)
