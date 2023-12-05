from custom_datasets import LLaMA2Transcript
from transformers import LlamaForCausalLM, LlamaTokenizer

dataset_fn = '../data_prep/_dataset.txt'
checkpoint_dir = '../checkpoints/'

tokenizer = LlamaTokenizer.from_pretrained("/output/path")
model = LlamaForCausalLM.from_pretrained("/output/path")