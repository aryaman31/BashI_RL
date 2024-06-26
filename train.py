import subprocess
import os 
import random
import time
import matplotlib.pyplot as plt

EPOCHS=100

output_dir = os.path.dirname(os.path.realpath(__file__))
webapp_dir = os.path.join(output_dir, "VulnerableApplications/")

ignoreList = ['DynEval_Age', 'dvwa_impossible', 'passthru', 'tight_filter', 'impossible', 'bwapp_ci']
webApps = [f for f in os.scandir(webapp_dir) if f.is_dir() and f.name not in ignoreList]

ts = str(time.time())
try: 
    os.mkdir(f"{output_dir}/logs/{ts}")
    os.mkdir(f"{output_dir}/logs/{ts}/php")
    os.mkdir(f"{output_dir}/logs/{ts}/agent")
except FileExistsError:
    pass

found = []
failed = []
counts = []
for epoch in range(2, EPOCHS):
    PORT=random.randint(10000, 60000)
    app = random.choice(webApps)
    file_server = open(f"{output_dir}/logs/{ts}/php/{epoch}_log_{app.name}.txt", "w+")
    file_agent = open(f"{output_dir}/logs/{ts}/agent/{epoch}_log_{app.name}.txt", "w+")
    try:
        print("======================================================================================")
        print(f"Training against {app.name}! Epoch: {epoch}")
        
        webServer_process = subprocess.Popen(["php", "-q", "-S", f"localhost:{PORT}", "-t", app.path], stderr=subprocess.STDOUT, stdout=file_server)
        model_process = subprocess.run(["python3", "bash_rl.py", str(webServer_process.pid), f"http://localhost:{PORT}", "true"], capture_output=True, text=True)

        file_agent.write(model_process.stdout)
        file_agent.write(model_process.stderr)

        file_server.close()
        file_agent.close()
        
        if model_process.returncode != 0:
            print(f"An error has occured in epoch {epoch}")
            print(model_process.returncode)
            print(model_process.stderr)
            print(model_process.stdout)
            webServer_process.kill()
            continue
        
        with open(f"{output_dir}/logs/{ts}/agent/{epoch}_log_{app.name}.txt", "r") as file:
            lines = file.readlines()
            if "Found an injection!\n" in lines: 
                # found.append(app.name)
                print(f"    Found injection for {app.name}")
                print("    Injection: " + lines[-3])
                counts.append(lines[-2].split(' ')[-1].strip())
            else:
                # failed.append(app.name)
                print(f"    No injection found for {app.name}")
                counts.append("-1")
        print("======================================================================================")
    finally:
        webServer_process.kill()
        file_server.close()
        file_agent.close()

# print("Found: " + ",".join(found))
# print("Failed: " + ",".join(failed))
print(f"Finished training against all webapps in {webapp_dir}")

with open(f"{output_dir}/logs/{ts}/counter.txt", "w+") as f:
    f.write(",".join(counts))

plt.plot(counts)
plt.xlabel('Epoch')
plt.ylabel('Counts')
plt.savefig('agent_counts.png')
    
    



