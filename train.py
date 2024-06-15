import subprocess
import os 
import random

PORT=8000

output_dir = os.path.dirname(os.path.realpath(__file__))
webapp_dir = os.path.join(output_dir, "VulnerableApplications/")

ignoreList = ['DynEval_Age', 'impossible', 'dvwa_impossible']
webApps = [f for f in os.scandir(webapp_dir) if f.is_dir() and f.name not in ignoreList]
random.shuffle(webApps)

found = []
failed = []
for app in webApps:
    file_server = open(f"{output_dir}/logs/php/log_{app.name}.txt", "w+")
    file_agent = open(f"{output_dir}/logs/agent/log_{app.name}.txt", "w+")
    try:
        print("======================================================================================")
        print(f"Training against {app.name}!")
        
        webServer_process = subprocess.Popen(["php", "-q", "-S", f"localhost:{PORT}", "-t", app.path], stderr=subprocess.STDOUT, stdout=file_server)
        model_process = subprocess.run(["python3", "bash_rl.py", str(webServer_process.pid), f"http://localhost:{PORT}"], stderr=subprocess.STDOUT, stdout=file_agent)

        file_server.close()
        file_agent.close()
        
        if model_process.returncode != 0:
            print("An error has occured")
            print(model_process.stderr)
            exit() 
        
        with open(f"{output_dir}/logs/agent/log_{app.name}.txt", "r") as file:
            lines = file.readlines()
            if "Found an injection!\n" in lines: 
                found.append(app.name)
                print(f"    Found injection for {app.name}")
                print("    Injection: " + lines[-1])
            else:
                failed.append(app.name)
                print(f"    No injection found for {app.name}")
        print("======================================================================================")
    finally:
        webServer_process.kill()
        file_server.close()
        file_agent.close()
        
print("Found: " + ",".join(found))
print("Failed: " + ",".join(failed))
print(f"Finished training against all webapps in {webapp_dir}")
    



