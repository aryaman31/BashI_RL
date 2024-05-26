from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForLanguageModeling, LineByLineTextDataset
from transformers import RobertaTokenizerFast, RobertaForMaskedLM
from tokenizers import ByteLevelBPETokenizer
import numpy as np
import evaluate
import torch 
import os

# Define paths and parameters
output_dir = './models/transformerAE/myles/'
customTokenizer_dir = output_dir + "customTokenizer/"
trainer_dir = output_dir + 'transAutoEncoder/'
output_dir = output_dir + 'robertaTokenizer/'


dataset_path = 'DataGen/bnf/Dataset.txt'

model_name = 'microsoft/codebert-base'
epochs = 1

def createDir(path):
    try: 
        os.mkdir(path)
    except FileExistsError:
        pass

# Function to compute metrics
# def compute_metrics(eval_pred):
#     logits, labels = eval_pred
#     predictions = np.argmax(logits, axis=-1)
#     return metric.compute(predictions=predictions, references=labels)

# Create the dirs 
createDir(output_dir)
createDir(customTokenizer_dir)
createDir(trainer_dir)
createDir(output_dir)


# Train a custom tokenizer
tokenizer = ByteLevelBPETokenizer()
tokenizer.train(files=[dataset_path], vocab_size=52000, min_frequency=2, special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>"])
tokenizer.save_model(customTokenizer_dir)

# Initialize the tokenizer
tokenizer = RobertaTokenizerFast.from_pretrained(customTokenizer_dir)

# Load the dataset
tokenized_datasets = LineByLineTextDataset(
    tokenizer=tokenizer,
    file_path=dataset_path,
    block_size=128,
)

# Split the dataset into training and validation sets
train_size = int(0.9 * len(tokenized_datasets))
val_size = len(tokenized_datasets) - train_size
train_set, val_set = torch.utils.data.random_split(tokenized_datasets, [train_size, val_size])

# Initialize the model
model = RobertaForMaskedLM.from_pretrained(model_name)

# Data collator to handle padding and masking
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=True,
    mlm_probability=0.15
)

# Define training arguments
training_args = TrainingArguments(
    output_dir=output_dir, 
    evaluation_strategy="epoch", 
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    num_train_epochs=epochs,
    save_strategy="epoch",
    logging_dir='./logs',  # Directory for storing logs
    logging_steps=10,
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_set,
    eval_dataset=val_set,
    data_collator=data_collator,
)

# Train the model
trainer.train()

eval_results = trainer.evaluate()

# Calculate perplexity
perplexity = np.exp(eval_results['eval_loss'])
print(f"Perplexity: {perplexity}")

# Save the model and tokenizer
trainer.save_model(trainer_dir)
tokenizer.save_pretrained(output_dir)
