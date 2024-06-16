import random

rules = {
    "alpha": ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y"],
    "digit": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "word" : ["tempWord"],
    "ip"   : ["<digit><digit><digit>.<digit><digit><digit>.<digit><digit><digit>.<digit><digit><digit>"],
    "slash": ['/', '${HOME:0:1}'],
    "filler": ["<word>", "<ip>", "<filepath>"],
    "filepath": ["file.txt", "<slash>etc<slash>passwd"],
    "space": [" ", "${IFS}"],
    "flag":  ["-<alpha>", "--<word>", "-<alpha>=<word>", "-<alpha>=<filepath>"],
    "cmd_word": ["id", "whoami", "sleep<space>1", "<slash>usr<slash>bin<slash>whoami", "<slash>usr<slash>bin<slash>id", "cat<space><filepath>", "ls<space><flag><space><word>", "sleep<space>0"],
    "redirection": [';', '&&', '||', '|'],
    "root": ["<cmd_word>", "<redirection><space><cmd_word>", "<filler><redirection><space><cmd_word>", "<redirection><cmd_word>", "<filler><space><redirection><cmd_word>"]
}

def addRandomTicks(payload):
    words = payload.split(' ')
    editWord_i = random.randint(0, len(words) - 1)
    word = list(words[editWord_i])
    insertPoints = sorted([random.randint(0, len(words[editWord_i])), random.randint(0, len(words[editWord_i]))])

    tick = random.choice(['\"', '\'', '`'])
    word.insert(insertPoints[1], tick)
    word.insert(insertPoints[0], tick)
    words[editWord_i] = ''.join(word)
    return ' '.join(words)

def generate_example(rules, start_symbol, depth=0):
    if depth > 50:
        return None
    
    if start_symbol not in rules.keys():
        print(start_symbol)
        return start_symbol

    production = random.choice(rules[start_symbol])
    tokens = production.split("<")
    
    example = ''
    for token in tokens:
        if '>' in token:
            i = token.index('>')
            tok = token[:i]
            rest = token[i+1:]
            temp = generate_example(rules, tok, depth+1)
            if not temp: return None
            example += temp + rest
        else:
            example += token
    return example


if __name__ == "__main__":
    samples = 300000
    file = open("DataGen/payloads/generated_dataset.txt", "w")
    i = 0
    addTickp = 0.1
    while i < samples:
        gen = generate_example(rules, "root")
        if random.random() < addTickp: gen = addRandomTicks(gen)
        if gen:
            i += 1
            file.write(gen + "\n")
    file.close()