import requests

class Controller:
    def __init__(self, host):
        self.host = host 
        self.requestPath = ''

    def findNewRequestPath(self):
        # Return true if new reqpath found, else false 
        print("Controller.findNewRequestPath IS NOT IMPLEMENTED")
        return True
    
    def makeRequest(self, params):
        # If game is find command, find a new input
        
        response = requests.get(self.address, params=params)
        # print("Response received:\n" + response.content)