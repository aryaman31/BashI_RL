import requests

class Controller:
    def __init__(self, address):
        self.address = address 
    
    def makeRequest(self, params):
        response = requests.get(self.address, params=params)
        # print("Response received:\n" + response.content)