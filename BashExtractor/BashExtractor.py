import subprocess
import time
import re

class BashExtractor:
    def __init__(self, server_pid):
        self.server_pid = server_pid 
        self.process = None

    def start(self, delay=0.1):
        self.process = subprocess.Popen(["strace", "-f", "-p", self.server_pid, "-e", "trace=execve", "--output=BashExtractor/temp.txt", "--quiet=attach"])
        time.sleep(delay)
        
    
    def stop(self):
        if self.process:
            self.process.kill()
            with open("BashExtractor/temp.txt", "r") as f:
                return self.__extractCommands(f.readlines())
        return []

    def __extractCommands(self, buffer):
        '''
            Should Ideally return all the different commands, with their exit codes 
            For now, just returns the executed bash command only
        '''
        lines = [l.split(" ", 1) for l in buffer]
        pid = lines[0][0]
        cmd = ["", ""]
        for line in lines: 
            if line[0] == pid: 
                matches = re.findall(r'execve\(".*?", \[(.*?)\],', line[1])
                if len(matches) > 0:
                    temp = matches[0].replace("\"", "").split(", ")
                    cmd[0] = temp[-1]
                elif 'exited' in line[1]: 
                    cmd[1] = line[1].split(" ")[-2]
        return cmd

        # pattern = r'execve\(".*?", \[(.*?)\],'
        # matches = re.findall(pattern, "".join(buffer))
        # out = []
        # for m in matches:
        #     temp = m.replace("\"", "").split(", ")
        #     if temp[0] == 'sh':
        #         out.append(temp[-1])
        # return out

    