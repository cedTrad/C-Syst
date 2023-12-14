from threading import Thread, Condition, Event


class MasterAgentThread(Thread):
    
    def __init__(self, condition, activeAgent, agent_bus, master_bus):
        Thread.__init__(self)
        self.activeAgent = activeAgent
        self.agentList = []
        
        self.condition = condition
        
        self.agent_bus = agent_bus
        self.master_bus = master_bus
    
    
    def addAgent(self, agentId):
        self.agentList.append(agentId)
    
    def active_agents(self, msg = "start"):
        for agentId in self.agentList:
            self.master_bus["msg"].update({agentId : "Start work ..."})
        
    def select_active_agent(self, activeAgent = 1):
        self.master_bus.update({"activeAgent" : activeAgent})
    
    def wait_agent_finish_step(self):
        msg = self.agent_bus["fstep"].values()
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
                if self.agent_bus["stop"]:
                    self.master_bus["stop"] = True
                

            
