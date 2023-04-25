import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, BloomForCausalLM
from tqdm import trange
import time

device = torch.device("cuda")

tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m")
model = BloomForCausalLM.from_pretrained("bigscience/bloom-560m", device_map="auto", torch_dtype=torch.float16).cuda()
model.load_state_dict(torch.load('models/bloom_560_final/pytorch_model.bin'))

# encode context the generation is conditioned on
input_ids = tokenizer.encode('<title> the waifu wars of 2022 </title>', return_tensors='pt').to(device)

print('Starting generation')
start = time.time()

# activate sampling and deactivate top_k by setting top_k sampling to 0
sample_output = model.generate(
    input_ids, 
    do_sample=True, 
    max_length=2048,
    temperature=0.75
)

print(tokenizer.decode(sample_output[0], skip_special_tokens=True))
print('Time taken:', time.time() - start)
