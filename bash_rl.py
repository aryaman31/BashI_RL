import sys

from Communication.Controller import Controller
from BashExtractor.BashExtractor import BashExtractor
from Environment.Environment import Environment
from Environment.Agent import Agent
    
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
    env = Environment(controller, bashEx) 

    agent = Agent()

    # Check wether pid is correct and exists

    NUM_RUNS = 1000
    EPISODES_PER_RUN = 100

    currState = env.reset()
    for i in range(NUM_RUNS):
        for i_episode in range(EPISODES_PER_RUN):
            state = env.reset()
            done, terminated = False, False 
            while not (done or terminated):
                action = Agent.pickAction(state)
                state = env.step(action) 

    # Can save agent model here !    
    
    print("FINISHED")

