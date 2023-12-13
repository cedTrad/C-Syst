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
    
    def start(self, msg = "start"):
        for agentId in self.agentList:
            self.master_bus["agent"].update({agentId : "Start work ..."})
        
    def select_active_agent(self, activeAgent = 1):
        self.master_bus.update({"activeAgent" : activeAgent})
    
    def is_all_running(self):
        msg = self.agent_bus["running"].values()
        return all(msg)
    
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
                print("**** Master ****")
                self.start()
                self.select_active_agent()
                
                self.condition.notify_all()
                
                print("Let's go ... ")
                print(f"master_bus : {self.master_bus}")
                
                
                while self.is_all_running():
                    print("Master are waiting for agents finish to execute thier work ... ")
                    print(f" agent_bus : {self.agent_bus}")
                    self.condition.wait()
                
                # After all agents execute their work
                # get agent msg
                agentData = self.get_agent_report()
                
                # Decision for next step
                self.analyse_report(agentData)
                
                # Stop simulation
                
                if self.agent_bus["stop"]:
                    self.master_bus["stop"] = True
                
                print(f" 2- {self.master_bus}")
                if self.master_bus["stop"]:
                    print("---------- STOP(Boss) ----------")
                    break
                
                self.agent_bus["msg"].update(
                    {agent : None for agent in self.agentList}
                )
                
                
    def global_report(self):
        ""
                
            
            
