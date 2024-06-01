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
    TERMINATION_LIMIT = 100

    currState = env.reset()
    canExploit = env.findNextTarget()
    while canExploit:
        for i_episode in range(EPISODES_PER_RUN):
            state = env.reset()
            agent.reset()
            for _ in range(TERMINATION_LIMIT):
                action = agent.pickAction(state)
                state = env.step(action) 
                game, reward = agent.updateGame(state)

                if game == GAME.FINISHED: 
                    break
        canExploit = env.findNextTarget()
                    
    # Can save agent model here !    
    agent.save('agent.model')
    
    print("FINISHED")

