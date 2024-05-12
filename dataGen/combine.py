import os
import random

folder_path = "/home/aryaman/final_year_project/project/dataGen/bash_logs"
dest_path = "combined_rand_logs.txt"

files = os.listdir(folder_path)

data = []

for file_name in files:
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            file_contents = file.read()
            contents = file_contents.split("\n")
            data.extend(contents)

random.shuffle(data)

with open(dest_path, 'w') as file: 
    data_str = '\n'.join(data)
    file.write(data_str)

