from threading import Thread, Condition, Event


class MasterAgentThread(Thread):
    
    def __init__(self, condition, activeAgent, agent_msg, master_msg):
        Thread.__init__(self)
        self.activeAgent = activeAgent
        self.agentList = []
        
        self.condition = condition
        
        self.agent_msg = agent_msg
        self.master_msg = master_msg
    
    
    def addAgent(self, agentId):
        self.agentList.append(agentId)
    
    def fitness(self):
        ""
    
    def run(self):
        while True:
            with self.condition:
                print("**** Master ****")
                for agentId in self.agentList:
                    self.master_msg.update({agentId : "Place an Order ... "})
                self.condition.notify_all()
                print("Let's go ... ")
                
                while all([msg for msg in self.agent_msg.values()]) is False:
                    print("Master are waiting for agents ... ")
                    print(f"{self.agent_msg}")
                    self.condition.wait()
                
                print(f" tracking ... : {self.agent_msg}")
                stop_condition = self.agent_msg == {agent : "stop" for agent in self.agentList}
                if stop_condition:
                    print("---------- STOP(Boss) ----------")
                    break
                
                self.agent_msg.update(
                    {agent : None for agent in self.agentList}
                )
                
                
    def global_report(self):
        ""
                
            
            
