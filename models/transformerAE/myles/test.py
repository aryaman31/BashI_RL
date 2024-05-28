from transformers import RobertaTokenizerFast, RobertaForMaskedLM
import torch

# Define paths
output_dir = './models/transformerAE/myles/'
model_dir = output_dir + 'transAutoEncoder/'
tokenizer_dir = output_dir + 'robertaTokenizer/'

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