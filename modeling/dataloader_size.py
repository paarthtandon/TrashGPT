from torch.utils.data import DataLoader
from custom_datasets import GPT2Transcript
from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium', pad_token='<|pad|>')

dataset_fn = '../annotated_w_names/_dataset.txt'
dataset_f = open(dataset_fn, 'r', encoding='utf-8')
dataset = GPT2Transcript(dataset_f.read(), tokenizer)
dataset_f.close()

dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

print(len(dataloader))
