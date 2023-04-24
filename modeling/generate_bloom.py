import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, BloomForCausalLM
from tqdm import trange

device = torch.device("cuda")

tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m")
model = BloomForCausalLM.from_pretrained("bigscience/bloom-560m").cuda()
# model.load_state_dict(torch.load('models/gpt_med/checkpoint-35000/pytorch_model.bin'))

# encode context the generation is conditioned on
input_ids = tokenizer.encode('<title> global warming </title>', return_tensors='pt').to(device)

# activate sampling and deactivate top_k by setting top_k sampling to 0
sample_output = model.generate(
    input_ids, 
    do_sample=True, 
    max_length=2048, 
    # top_k=50, 
    top_p=0.75
)

print(tokenizer.decode(sample_output[0], skip_special_tokens=True))
