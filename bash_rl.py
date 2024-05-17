import sys

from communication.Controller import Controller
from BashExtractor import BashExtractor
from Environment.state import State
    
if __name__ == "__main__":
    '''
        main execution of the tool
    '''

    # Get PID of server 
    if len(sys.argv) != 3:
        print("Usage: python3 bash_rl.py <PID OF SERVER> <Address of server>")
        sys.exit()
    
    server_pid = sys.argv[1] 
    server_address = sys.argv[2]

    controller = Controller(server_address)
    bashEx = BashExtractor(server_pid)    

    # Check wether pid is correct and exists

    payload = "8.8.8.8; whoami"
    for i in range(1): 
        bashEx.start()

        # controller sends command to server with unique token
        controller.makeRequest({"ip_address": payload})

        # bash extractor returns all the new bash commands its seen
        out = bashEx.stop()
        print(out)

        # controller looks for bash command with unique token
        cmd, err = out[-1]
        state = State(cmd, payload, err)

        # sends this to agent

        # agent returns a bash modification 

        # update next command according action
    
    print("FINISHED")

