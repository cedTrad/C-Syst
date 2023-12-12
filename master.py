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
    
    
    def is_all_running(self, agent_bus):
        msg = agent_bus["running"].values()
        return all(msg)
        
        
    def fitness(self):
        ""
    
    def run(self):
        while True:
            with self.condition:
                print("**** Master ****")
                for agentId in self.agentList:
                    self.master_bus["agent"].update({agentId : "Start work ..."})
                
                self.master_bus.update({"activeAgent" : 1})
                self.condition.notify_all()
                
                print("Let's go ... ")
                print(f"{self.master_bus}")
                
                #while all([msg for msg in self.agent_bus["msg"].values()]) is False:
                while self.is_running(self.agent_bus):
                    print("Master are waiting for agents ... ")
                    print(f"{self.agent_bus}")
                    self.condition.wait()
                
                stop_condition = 'stop' in self.agent_bus["msg"].values()
                print(f"Stop condition : {stop_condition}")
                if stop_condition:
                    print("---------- STOP(Boss) ----------")
                    break
                
                self.agent_bus["msg"].update(
                    {agent : None for agent in self.agentList}
                )
                
                
    def global_report(self):
        ""
                
            
            
