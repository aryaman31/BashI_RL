import re 
import random

def parse_bnf(bnf):
    rules = {}
    for line in bnf.split('\n'):
        if '::=' in line:
            non_terminal, production = line.split('::=')
            rules[non_terminal.strip()] = [prod.strip().replace("@", "\n").replace('\'', '') for prod in production.split('|')]
    return rules

def generate_example(rules, start_symbol, depth=0):
    if depth > 10000:
        return None
    
    if start_symbol not in rules:
        print(start_symbol)
        return start_symbol
    
    addSpace = start_symbol not in ['<WORD>', '<ALPHA>', '<NUMBER>', '<DIGIT>', '<FLAGS>']


    production = random.choice(rules[start_symbol])
    # tokens = re.findall(r'(<[^>]+>|[^<> ]+)', production)
    tokens = production.split(" ")
    
    example = ''
    for token in tokens:
        if token.startswith('<') and token.endswith('>') and len(token) > 2:
            temp = generate_example(rules, token, depth+1)
            if not temp: return None
            example += temp + (' ' if addSpace else '')
        else:
            example += token + (' ' if addSpace else '')
    return example


if __name__ == "__main__":
    file_bnf = "dataGen/bnf/bashV2.bnf"
    samples = 300000

    file = open(file_bnf, "r")
    data = file.read()
    file.close() 

    rules = parse_bnf(data)

    file = open("dataGen/bnf/Dataset.txt", "w")
    i = 0
    while i < samples:
        gen = generate_example(rules, "<SIMPLE-COMMAND>")
        if gen:
            i += 1
            file.write(gen + "\n")
    file.close()
