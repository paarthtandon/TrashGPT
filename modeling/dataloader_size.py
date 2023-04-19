from torch.utils.data import DataLoader
from custom_datasets import GPT2Transcript

dataset_fn = '../annotated_w_names/_dataset.txt'
dataset_f = open(dataset_fn, 'r', encoding='utf-8')
dataset = GPT2Transcript(dataset_f.read(), gpt2_type="gpt2")
dataset_f.close()

dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

print(len(dataloader))
