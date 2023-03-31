import torch
import torch.nn.functional as F
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from tqdm import trange

device = torch.device("cuda")

def generate(
    model,
    tokenizer,
    prompt='<|endoftext|>',
    entry_count=3,
    entry_length=700, #maximum number of words
    top_p=0.8,
    temperature=1.0,
):
    model.eval()
    generated_num = 0
    generated_list = []

    filter_value = -float("Inf")

    with torch.no_grad():

        for entry_idx in trange(entry_count):

            entry_finished = False
            generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0).to(device)

            for i in range(entry_length):
                outputs = model(generated, labels=generated)
                loss, logits = outputs[:2]
                logits = logits[:, -1, :] / (temperature if temperature > 0 else 1.0)

                sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

                sorted_indices_to_remove = cumulative_probs > top_p
                sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[
                    ..., :-1
                ].clone()
                sorted_indices_to_remove[..., 0] = 0

                indices_to_remove = sorted_indices[sorted_indices_to_remove]
                logits[:, indices_to_remove] = filter_value

                next_token = torch.multinomial(F.softmax(logits, dim=-1), num_samples=1)
                generated = torch.cat((generated, next_token), dim=1)

                if next_token in tokenizer.encode("<|endoftext|>"):
                    entry_finished = True

                if entry_finished:

                    generated_num = generated_num + 1

                    output_list = list(generated.to('cpu').squeeze().numpy())
                    output_text = tokenizer.decode(output_list)
                    generated_list.append(output_text)
                    break
            
            if not entry_finished:
              output_list = list(generated.to('cpu').squeeze().numpy())
              output_text = f"{tokenizer.decode(output_list)}<|endoftext|>" 
              generated_list.append(output_text)
                
    return generated_list

#Function to generate multiple sentences. Test data should be a dataframe
def text_generation(model, tokenizer):
  generated = []
  for i in range(1):
    x = generate(model.to(device), tokenizer, prompt='<garnt>', entry_count=1)
    generated.append(x)
  return generated

#Run the functions to generate the lyrics
model = torch.load('models/gpt2_20ep.pt')
# model = GPT2LMHeadModel.from_pretrained('gpt2')
# model.load_state_dict(torch.load('models/gpt2_15ep.pt'))

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
generated = text_generation(model, tokenizer)
print(generated[0][0])
