import torch

from bash_rl import cmdTokenizer, cmdEncoder, payloadEncoder, payloadTokenizer

class State:
    def __init__(self, executed_command: str, previous_payload: str, error_code: str):
        self.executed_command = executed_command
        self.previous_payload = previous_payload 
        self.error_code = error_code
    
    def createCommandTensor(self) -> torch.tensor: 
        inp = cmdTokenizer(self.executed_command, return_tensors='pt')
        out = cmdEncoder(**inp, output_hidden_states=True)
        return out.hidden_states[-1][0, 0, :]

    def createPayloadTensor(self) ->  torch.tensor:
        inp = payloadTokenizer(self.previous_payload, return_tensors='pt')
        out = payloadEncoder(**inp, output_hidden_states=True)
        return out.hidden_states[-1][0, 0, :]
    
    def getStateTensor(self) -> torch.tensor:
        cmd = self.createCommandTensor()
        payload = self.createPayloadTensor()
        err = torch.FloatTensor([self.error_code])
        return torch.cat((cmd, payload, err))
    
    def __str__(self):
        return f'({self.executed_command}, {self.previous_payload}, {self.error_code})'