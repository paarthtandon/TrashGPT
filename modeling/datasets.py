import torch
from torch.utils.data import Dataset
from transformers import GPT2Tokenizer

class Transcript(Dataset):
    def __init__(self, text, gpt2_type='gpt2', max_length=1024):

        self.tokenizer = GPT2Tokenizer.from_pretrained(gpt2_type)
        self.samples = []
        for i in range(0, len(text), max_length):
            self.samples.append(torch.tensor(self.tokenizer.encode(text[i : i + max_length])))
        self.count = len(self.samples)

    def __len__(self):
        return self.count

    def __getitem__(self, i):
        return self.samples[i]
