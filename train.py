import subprocess
import os 

PORT=8000

output_dir = os.path.dirname(os.path.realpath(__file__))
webapp_dir = os.path.join(output_dir, "VulnerableApplications/")

ignoreList = ['DynEval_Age', 'impossible', 'dvwa_impossible']
webApps = [f for f in os.scandir(webapp_dir) if f.is_dir() and f.name not in ignoreList]

found = []
failed = []
for app in webApps:
    file = open(f"{output_dir}/logs/log_{app.name}.txt", "w+")
    try:
        print("======================================================================================")
        print(f"Training against {app.name}!")
        
        webServer_process = subprocess.Popen(["php", "-q", "-S", f"localhost:{PORT}", "-t", app.path], stderr=subprocess.STDOUT, stdout=file)
        model_process = subprocess.run(["python3", "bash_rl.py", str(webServer_process.pid), f"http://localhost:{PORT}"], capture_output=True, text=True)
        
        if model_process.returncode != 0:
            print("An error has occured")
            print(model_process.stderr)
            exit() 
        
        if "Found an injection!" in model_process.stdout: 
            found.append(app.name)
            print(f"    Found injection for {app.name}")
            print("    Injection: " + model_process.stdout.split(["Found an injection!\n"][1]))
        else:
            failed.append(app.name)
            print(f"    No injection found for {app.name}")
        print("======================================================================================")
    finally:
        webServer_process.kill()
        file.close()
        
print("Found: " + ",".join(found))
print("Failed: " + ",".join(failed))
print(f"Finished training against all webapps in {webapp_dir}")
    



