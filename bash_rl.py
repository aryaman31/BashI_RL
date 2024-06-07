import sys

from Communication.Controller import Controller
from BashExtractor.BashExtractor import BashExtractor
from Environment.Actions.Action import Action
from Environment.Environment import BashI_Environment
from Environment.Agent import Agent

from Environment.Games import GAME

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

    print("...................................................................................")
    print("Initializeing Environment...")
    env = BashI_Environment(controller, bashEx) 
    print("Done")
    print("...................................................................................")

    print("...................................................................................")
    print("Starting Agent...")
    agent = Agent()
    print("Done")
    print("...................................................................................")


    # Check wether pid is correct and exists

    EPISODES_PER_RUN = 50
    TERMINATION_LIMIT = 30

    currState = env.reset()
    canExploit = env.findNextTarget()
    while canExploit:
        for i_episode in range(EPISODES_PER_RUN):
            print("==============================================================================")
            print(f"                           Episode {i_episode}")
            state = env.reset()
            agent.reset()
            print(f"Initial Payload: {state.previous_payload}")
            for i in range(TERMINATION_LIMIT):
                action = agent.pickAction(state)
                state = env.step(action) 
                game, reward = agent.updateGame(state, env.before, env.after)
                agent.train(reward)

                print("------------------------------------------------------------------------------------------------")
                print(f"{i}) Payload: {state.previous_payload}, State: {state}, Game: {game}, Action: {action.actionId}:{action.location}")
                print("------------------------------------------------------------------------------------------------")

                if game == GAME.FINISHED:
                    print("Found an injection!")
                    print(state.previous_payload)
                    agent.save('agent.model')
                    exit()
            print("==============================================================================\n")
        
        canExploit = env.findNextTarget()
                    
    # Can save agent model here !    
    agent.save('agent.model')  
    
    print("FINISHED")

