import sys
import os

from Communication.Controller import Controller
from BashExtractor.BashExtractor import BashExtractor
from Environment.Action import Action
from Environment.Environment import BashI_Environment
from Environment.Agent import Agent

from Environment.Games import GAME

if __name__ == "__main__":
    '''
        main execution of the tool
    '''

    # Get PID of server 
    if len(sys.argv) != 4:
        print("Usage: python3 bash_rl.py <PID OF SERVER> <Address of server> <learning>")
        sys.exit()
    
    server_pid = sys.argv[1] 
    server_address = sys.argv[2]
    learning = sys.argv[3].lower() == 'true'

    try:
        os.kill(int(server_pid), 0)
    except OSError:
        print("PID is invalid. No process exists with given PID.")
        exit(1)

    controller = Controller(server_address)
    bashEx = BashExtractor(server_pid) 

    print("...................................................................................")
    print("Initializeing Environment...")
    env = BashI_Environment(controller, bashEx) 
    print("Done")
    print("...................................................................................")

    print("...................................................................................")
    print("Starting Agent...")
    agent = Agent(learning=learning)
    print("Done")
    print("...................................................................................")

    EPISODES_PER_RUN = 50
    TERMINATION_LIMIT = 15

    currState = env.reset()
    canExploit = env.findNextTarget()
    while canExploit:
        counter = 0
        for i_episode in range(EPISODES_PER_RUN):
            print("==============================================================================")
            print(f"                           Episode {i_episode}")
            state = env.reset()
            agent.reset()
            print(f"Initial Payload: {state.previous_payload}")
            for i in range(TERMINATION_LIMIT):
                counter += 1
                action = agent.pickAction(state, True)
                state = env.step(action) 
                game, reward = agent.updateGame(state, env.before, env.after)
                agent.train(reward)

                print("------------------------------------------------------------------------------------------------")
                print(f"{i}) Payload: {state.previous_payload}, State: {state}, Game: {game}, Action: {action.actionId}:{action.location}")
                print("------------------------------------------------------------------------------------------------")

                if game == GAME.FINISHED:
                    print("Found an injection!")
                    print(state.previous_payload)
                    print(f"Tries: {counter}" )
                    if learning:
                        agent.save('agent.model')
                    exit(0)
            print("==============================================================================\n")
        
        canExploit = env.findNextTarget()
                    
    # Can save agent model here !    
    if learning:
        agent.save('agent.model')  
    print("No injection found :(")

