import torch 

encoder = torch.load("encoder.model")
decoder = torch.load("decoder.model")
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


def cmd_to_tensor(cmd):
    cmd = "SOL " + cmd + " EOL"
    tokens = cmd.split()
    # tokens = list(cmd)
    tensor = torch.tensor([torch.tensor(cmd_to_idx[t]) for t in tokens], device=device)
    return tensor

with open("dataGen/combined_rand_logs.txt") as file:
    data = file.readlines()
    data = list(map(lambda x : x.strip(), data))
    # data = data[:1000]

    token_set = set(" ".join(data).split())
    # token_set = set(list("".join(data)))
    token_set.add("SOL")
    token_set.add("EOL")
    cmd_to_idx = {token:i for i, token in enumerate(token_set)}
    idx_to_cmd = {i:token for token, i in cmd_to_idx.items()}

cmd = "sudo apt-get update"
tensor_cmd = cmd_to_tensor(cmd)
output, hidden = encoder.encode(tensor_cmd, tensor_cmd.size(0))

cmd_start = torch.tensor([[cmd_to_idx["SOL"]]], device=device)
result = decoder.decode(cmd_start, output, hidden, tensor_cmd.size(0))
print(result)

