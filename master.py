from queue import Queue
from threading import Thread, Event, Barrier

from magent import MAgentThread

class MasterAgentThread(Thread):
    
    def __init__(self, env):
        Thread.__init__(self)
        self.agents = []
        
        self.env = env
        
        self.event = Event()
        self.master_bus = {}
        self.agent_bus = {}
    
    
    def set_barrier(self, n):
        def custom_action():
            print(" //////////////// *** Barrier passee *** \\\\\\\\\\\\\\\\")
        self.barrier = Barrier(n, action=custom_action)
    
    def addAgent(self, Id, env):
        self.agent_bus[Id] = Queue()
        self.master_bus[Id] = Queue()
        
        sync = [self.event, self.barrier, self.agent_bus[Id], self.master_bus[Id]]
        params = list(Id) + [env] + sync
        agent = MAgentThread(*params)
        self.agents.append(agent)
        
    
    def active_agents(self, msg = "start"):
        for agent in self.agents:
            agent.start()
            self.master_bus[agent.Id].put("start work")
            
    
    def update_params(self, Id, name, param):
        self.agents[Id].update_policy(name, param)
        
        
    def select_active_agent(self, activeAgent = 1):
        self.master_bus.update({"activeAgent" : activeAgent})
    
    
    def wait_agent_finish_step(self):
        msg = self.agent_bus["fstep"]
        return not all(msg)
    
    
    def get_agent_report(self):
        temp = {}
        for agent in self.agents:
            temp[agent.Id] = self.agent_bus[agent.Id].get()
        return temp
    
    def fitness(self):
        ""
        
    def analyse_report(self, agentData):
        ""
    
    def stop_simulation(self):
        if self.master_bus["stop"]:
            print("------ STOP -------")
            for agent in self.agents:
                agent.join()
            return True
    
    def run(self):
        while True:
                
            # Start simulation
            print(" ---------------   Master : Let's go ... ")
            self.active_agents()
            self.select_active_agent(1)
            
            # Set the event  to signal agents to start 
            self.event.set()
            print(f"master_bus : {self.master_bus}")
                
            # Wait agents finish thier tasks
            print("Master wait finish thier work ... ")
            self.event.wait()
                
            # After all agents execute their work, get agent msg
            agentData = self.get_agent_report()
            print(f"Agent report {agentData}")
                
            # Decision for next step
            self.analyse_report(agentData)
                
            # Stop simulation
 
            
