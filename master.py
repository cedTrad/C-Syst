from queue import Queue
from threading import Thread, Event, Barrier

from magent import MAgentThread

#class MasterAgentThread(Thread):
class MasterAgentThread():
    
    def __init__(self, env):
        #Thread.__init__(self)
        self.agents = {}
        
        self.env = env
        
        self.event = Event()
        self.master_bus = {}
        self.agent_bus = {}
    
    
    def set_barrier(self, n):
        def custom_action():
            print(" //////////////// *** Barrier passee *** \\\\\\\\\\\\\\\\")
        self.barrier = Barrier(n, action=custom_action)
    
    def add_agent(self, Id, env):
        self.agent_bus[Id] = Queue()
        self.master_bus[Id] = Queue()
        
        sync = [self.event, self.agent_bus, self.master_bus, self.barrier]
        params = [Id] + [env] + sync
        agent = MAgentThread(*params)
        self.agents[Id] = agent
        
    
    def active_agents(self):
        for id, agent in self.agents.items():
            print("Start id : ",id)
            agent.start()
    
    def send_order_to_agents(self, data={"msg" : "start work", "stop" : False, "paper" : True}):
        for id, agent in self.agents.items():
            print("Set order for id : ",id)
            self.master_bus[id].put(data) 
    
    def update_params(self, Id, name, param):
        self.agents[Id].update_policy(name, param)
        
        
    def select_active_agent(self, activeAgent = 1):
        ""
    
    def get_agent_report(self):
        temp = {}
        for id, agent in self.agents.items():
            temp[id] = self.agent_bus[id].get()
        return temp
    
    def fitness(self):
        ""
        
    def analyse_report(self, agentData):
        ""
    
    def stop_simulation(self, agentData):
        if list(agentData.values())[0]["stop"]:
            print("------ STOP -------")
            for id, agent in self.agents.items():
                agent.join()
            return True
        else:
            return False
    
    def run(self):
        while True:
                
            # Start simulation
            print(" ---------------   Master : Let's go ... ")
            self.send_order_to_agents()
            self.select_active_agent(1)
            
            # Set the event  to signal agents to start 
            self.event.set()
            print(f"master_bus : {self.master_bus}")
                
            # Wait agents finish thier tasks
            print("Master wait finish thier work ... ")
                           
            # After all agents execute their work, get agent msg
            agentData = self.get_agent_report()
            print(f"Agent report {agentData}")
                
            # Decision for next step
            self.analyse_report(agentData)
            self.event.clear()
            
            # Stop simulation
            if self.stop_simulation(agentData):
                print("--- MASTER BREAK ---")
                break
 
            
