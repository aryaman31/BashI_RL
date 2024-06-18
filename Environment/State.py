import torch

from transformers import RobertaTokenizerFast, RobertaForMaskedLM

class State:
    model = 'latest'
    cmdTokenizer = RobertaTokenizerFast.from_pretrained(f"models/transformerAE/{model}/cmdTokenizer/")
    cmdEncoder = RobertaForMaskedLM.from_pretrained(f"models/transformerAE/{model}/cmdEncoder/")

    payloadTokenizer = RobertaTokenizerFast.from_pretrained(f"models/transformerAE/{model}/payloadTokenizer/")
    payloadEncoder = RobertaForMaskedLM.from_pretrained(f"models/transformerAE/{model}/payloadEncoder/")
    def __init__(self, executed_command: str, previous_payload: str, error_code: str):
        self.executed_command = executed_command
        self.previous_payload = previous_payload 
        self.error_code = int(error_code)
    
    def createCommandTensor(self) -> torch.tensor: 
        inp = State.cmdTokenizer(self.executed_command, return_tensors='pt')
        out = State.cmdEncoder(**inp, output_hidden_states=True)
        return out.hidden_states[-1][0, 0, :]

    def createPayloadTensor(self) ->  torch.tensor:
        inp = State.payloadTokenizer(self.previous_payload, return_tensors='pt')
        out = State.payloadEncoder(**inp, output_hidden_states=True)
        return out.hidden_states[-1][0, 0, :]
    
    def getStateTensor(self) -> torch.tensor:
        cmd = self.createCommandTensor()
        payload = self.createPayloadTensor()
        err = torch.FloatTensor([self.error_code])
        return torch.cat((cmd, payload, err))
    
    def size() -> int: 
        return 768 + 768 + 1
    
    def __str__(self):
        return f'({self.executed_command}, {self.previous_payload}, {self.error_code})'