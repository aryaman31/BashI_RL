import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict

class Controller:
    def __init__(self, url):
        self.url = url 
        self.requestMethod = ''
        self.requestAction = ''
        self.input = ''
        self.inputs = defaultdict(list)

        response = requests.get(self.url)
        if response.status_code != 200:
            print(f"Server returned error {response.status_code}. Please fix the URL.")
            exit()
        
        print("Looking for potential inputs...")
        total = 0
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        self.forms = list(soup.find_all('form', recursive=True))
        for form in self.forms:
            inps = form.find_all('input')
            for input_field in inps:
                if input_field.get('type') in ['text']:
                    total += 1
                    self.inputs[form].append(input_field.get('name'))
        print(f"Done. Found {total} potential inputs")
        
    def findNewRequestPath(self):
        if len(self.forms) < 1:
            return False 
        
        self.input = self.inputs[self.forms[0]].pop()
        self.requestAction = self.forms[0].get('action')
        self.requestMethod = self.forms[0].get('method', 'get')

        if self.inputs[self.forms[0]] == []:
            self.forms.pop(0)

        return True
        
    def makeRequest(self, payload):
        request_url = urljoin(self.url, self.requestAction)
        params = {self.input : payload}
        
        if self.requestMethod == 'get':
            response = requests.get(request_url, params=params)
        else: 
            response = requests.post(request_url, json=params)
        # print("Response received:\n" + response.content)

if __name__ == '__main__':
    controller = Controller('http://localhost:8000/')
    controller.findNewRequestPath()
    controller.makeRequest('test')

    controller.findNewRequestPath()
    controller.makeRequest('test2')