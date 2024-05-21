import torch

class State:
    def __init__(self, executed_command: str, previous_payload: str, error_code: str):
        self.executed_command = executed_command
        self.previous_payload = previous_payload 
        self.error_code = error_code
    
    def createCommandTensor(self) -> torch.tensor: 
        cmd_encoder = torch.load("models/cmdEncoder.model")
        return cmd_encoder.encode((self.executed_command))

    def createPayloadTensor(self) ->  torch.tensor:
        payload_encoder = torch.load("models/payloadEncoder.model")
        return payload_encoder.encode(self.previous_payload)
    
    def getState(self):
        cmd = self.createCommandTensor()
        payload = self.createPayloadTensor()
        err = torch.FloatTensor([self.error_code])
        return torch.cat((cmd, payload, err))