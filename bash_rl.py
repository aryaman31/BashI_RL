import sys
from transformers import RobertaTokenizerFast, RobertaForMaskedLM

from Communication.Controller import Controller
from BashExtractor.BashExtractor import BashExtractor
from Environment.Actions.Action import Action
from Environment.Environment import BashI_Environment
from Environment.Agent import Agent

from Environment.Games import GAME
    
if __name__ != "__main__":
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
    env = BashI_Environment(controller, bashEx) 

    cmdTokenizer = RobertaTokenizerFast.from_pretrained("models/transformerAE/cmdTokenizer/")
    cmdEncoder = RobertaForMaskedLM.from_pretrained("models/transformerAE/cmdEncoder/")

    payloadTokenizer = RobertaTokenizerFast.from_pretrained("models/transformerAE/payloadTokenizer/")
    payloadEncoder = RobertaForMaskedLM.from_pretrained("models/transformerAE/payloadEncoder/")

    agent = Agent()

    # Check wether pid is correct and exists

    NUM_RUNS = 1000
    EPISODES_PER_RUN = 100

    currState = env.reset()
    found = controller.findNewRequestPath()
    while found:

        for i in range(NUM_RUNS):
            for i_episode in range(EPISODES_PER_RUN):
                state = env.reset()
                done, terminated = False, False 
                i = 0
                while not (done or terminated):
                    action = agent.pickAction(state)
                    state = env.step(action) 
                    # Add a termination condition here
                    done = agent.game == GAME.FINISHED
                    i += 1 
                    

    # Can save agent model here !    
    agent.save('agent.model')
    
    print("FINISHED")

