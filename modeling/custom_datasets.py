import torch
from torch.utils.data import Dataset

class GPT2Transcript(Dataset):
    def __init__(self, text, tokenizer, max_length=1024):
        self.input_ids = []
        self.attn_masks = []
        self.labels = []

        self.tokenizer = tokenizer
        self.samples = []
        for i in range(0, len(text), max_length):
            encodings_dict = self.tokenizer(text[i : i + max_length],max_length=max_length, padding='max_length')
            self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
            self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))
        self.count = len(self.samples)

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.attn_masks[idx]

class BloomTranscript(Dataset):
    def __init__(self, text, tokenizer, max_length=2048):
        self.input_ids = []
        self.attn_masks = []
        self.labels = []

        self.tokenizer = tokenizer
        self.samples = []
        for i in range(0, len(text), max_length):
            encodings_dict = self.tokenizer(text[i : i + max_length],max_length=max_length, padding='max_length')
            self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
            self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))
        self.count = len(self.samples)

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.attn_masks[idx]
