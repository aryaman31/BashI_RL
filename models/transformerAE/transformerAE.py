from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForLanguageModeling, LineByLineTextDataset
from transformers import RobertaTokenizerFast, RobertaForMaskedLM
from tokenizers import ByteLevelBPETokenizer
import matplotlib.pyplot as plt
import numpy as np
import torch 
import os

# Define paths and parameters
output_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = os.path.join(output_dir, "transformerFigs/")

cmd_encoder_dir = os.path.join(output_dir, 'cmdEncoder/')
cmd_tokenizer_dir = os.path.join(output_dir,'cmdTokenizer/')

payload_encoder_dir = os.path.join(output_dir, 'payloadEncoder/')
payload_tokenizer_dir = os.path.join(output_dir,'payloadTokenizer/')

dirs = [cmd_encoder_dir, cmd_tokenizer_dir, payload_encoder_dir, payload_tokenizer_dir]

cmd_dataset_path = 'DataGen/bnf/Dataset.txt'
payload_dataset_path = 'DataGen/payloads/generated_dataset.txt'

model_name = 'microsoft/codebert-base'
epochs = 5

def createDir(path):
    try: 
        os.mkdir(path)
    except FileExistsError:
        pass

# Create the dirs 
for d in dirs:
    createDir(d)

def train(dataset_path, tokenizer_dir, encoder_dir, model_disp_name='Cmd Encoder'):
    # Train a custom tokenizer
    save_dir = os.path.join(output_dir, 'customTokenizer/'); createDir(save_dir)
    tokenizer = ByteLevelBPETokenizer()
    tokenizer.train(files=[dataset_path], vocab_size=52000, min_frequency=2, special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>"])
    tokenizer.save_model(save_dir)

    # Initialize the tokenizer
    tokenizer = RobertaTokenizerFast.from_pretrained(save_dir)

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
        disable_tqdm=True
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
    print(f"Finished training {model_disp_name}")

    eval_results = trainer.evaluate()

    # Calculate perplexity
    perplexity = np.exp(eval_results['eval_loss'])
    print(f"Perplexity: {perplexity}")

    # Save the model and tokenizer
    trainer.save_model(encoder_dir)
    tokenizer.save_pretrained(tokenizer_dir)
    return trainer

def saveLossGraph(trainer, figName):
    loss = [node['loss'] for node in trainer.state.log_history if 'loss' in node.keys()]
    plt.plot(loss)
    plt.xlabel("Logging Step")
    plt.ylabel("Loss")
    plt.savefig(figName)

payloadTrainer = train(payload_dataset_path, payload_tokenizer_dir, payload_encoder_dir, model_disp_name='Payload Encoder')
cmdTrainer = train(cmd_dataset_path, cmd_tokenizer_dir, cmd_encoder_dir)

saveLossGraph(payloadTrainer, "payload_bnf_loss.png")
saveLossGraph(cmdTrainer, "cmd_bnf_loss.png")

