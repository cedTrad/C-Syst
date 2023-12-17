from queue import Queue
from threading import Thread, Condition, Event, Barrier

from magent import MAgentThread

class MasterAgentThread(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.agents = []
        
        self.condition = Condition()
        #self.event = Event()
        self.master_bus = {}
        self.agent_bus = {}
        self.barrier = Barrier(4)
    
    
    def addAgent(self, agentId, env):
        self.agent_bus[agentId] = Queue()
        self.master_bus[agentId] = Queue()
        
        sync = [self.condition, self.barrier, self.agent_bus[agentId], self.master_bus[agentId]]
        params = agentId + [env] + sync
        agent = MAgentThread(*params)
        self.agents.append(agent)
        
    
    def active_agents(self, msg = "start"):
        for agent in self.agents:
            agent.start()
            self.master_bus[agent.Id].put("start work")
            agent.join()
            
        
    def select_active_agent(self, activeAgent = 1):
        self.master_bus.update({"activeAgent" : activeAgent})
    
    def wait_agent_finish_step(self):
        msg = self.agent_bus["fstep"]
        return not all(msg)
    
    def get_agent_report(self):
        return {agentId : self.agent_bus["msg"].pop(agentId, None) for agentId in self.agentList}
    
    def fitness(self):
        ""
        
    def analyse_report(self, agentData):
        ""
    
    def stop_simulation(self):
        if self.master_bus["stop"]:
            print("------ STOP -------")
            return True
    
    def run(self):
        while True:
            with self.condition:
                
                # Start simulation
                print(" ---------------   Master : Let's go ... ")
                self.active_agents()
                self.select_active_agent(1)
                
                self.condition.notify_all()
                print(f"master_bus : {self.master_bus}")
                
                # Wait agents finish thier tasks
                while self.wait_agent_finish_step():
                    print("Master are waiting for agents finish to execute thier work ... ")
                    print(f" agent_bus : {self.agent_bus}")
                    self.condition.wait()
                
                # After all agents execute their work
                # get agent msg
                agentData = self.get_agent_report()
                print(f"Agent report {agentData}")
                
                # Decision for next step
                self.analyse_report(agentData)
                
                # Stop simulation
                if self.stop_simulation:
                    break
                

            
