from torch.utils.data import DataLoader
from datasets import Transcript

dataset_fn = '../annotated_w_names/dataset.txt'
dataset_f = open(dataset_fn, 'r', encoding='utf-8')
dataset = Transcript(dataset_f.read(), gpt2_type="gpt2") 
dataset_f.close()

dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

print(len(dataloader))
