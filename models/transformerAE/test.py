from transformers import RobertaTokenizerFast, RobertaForMaskedLM
import torch
import os

# Define paths
output_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(output_dir, 'latest/')
model_dir = os.path.join(output_dir, 'cmdEncoder/')
tokenizer_dir = os.path.join(output_dir, 'cmdTokenizer/')

# Load the tokenizer and model
tokenizer = RobertaTokenizerFast.from_pretrained(tokenizer_dir)
model = RobertaForMaskedLM.from_pretrained(model_dir)

# Prepare input text with a mask token
input_text = "mv file.txt  /path1/path2/file.txt   <<- tempWord  "
inputs = tokenizer(input_text, return_tensors='pt')

# Perform inference
with torch.no_grad():
    outputs = model(**inputs, output_hidden_states=True)
    predictions = outputs.logits

# Get the predicted token ID
# mask_token_index = (inputs.input_ids == tokenizer.mask_token_id).nonzero(as_tuple=True)[1]
predicted_token_ids = predictions.argmax(dim=-1).squeeze()

# Decode the predicted token ID to get the predicted word
predicted_token = tokenizer.decode(predicted_token_ids)

print(f"Input: {input_text}")
print(f"Output: {predicted_token}")
print(f"Encoding: {outputs.hidden_states[-1][0, 0, :].size()}")