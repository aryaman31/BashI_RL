import subprocess
import os 
import random
import time
import matplotlib.pyplot as plt
import sys

if len(sys.argv) != 2:
    print("Usage: python3 test.py <app number>")
    sys.exit()
    
app_num = int(sys.argv[1])

EPOCHS=100

output_dir = os.path.dirname(os.path.realpath(__file__))
webapp_dir = os.path.join(output_dir, "VulnerableApplications/")

ignoreList = ['DynEval_Age', 'dvwa_impossible', 'passthru', 'tight_filter', 'impossible', 'bwapp_ci']
webApps = [f for f in os.scandir(webapp_dir) if f.is_dir() and f.name not in ignoreList]

PORT=random.randint(10000, 60000)

app = webApps[app_num]
print(f'TESTING: {app.name}')

webServer_process = subprocess.Popen(["php", "-q", "-S", f"localhost:{PORT}", "-t", app.path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
model_process = subprocess.run(["python3", "bash_rl.py", str(webServer_process.pid), f"http://localhost:{PORT}", "false"])#, capture_output=True, text=True)

# print(model_process.returncode)
# print(model_process.stderr)
# print(model_process.stdout)


# if "Found an injection!\n" in model_process.stdout: 
#     # found.append(app.name)
#     print(f"    Found injection")
#     print("    Injection: " + model_process.stdout[-3])
# else:
#     # failed.append(app.name)
#     print(f"    No injection found")

webServer_process.kill()


    
    



