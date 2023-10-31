from threading import Thread, Condition, Event


class MasterAgentThread(Thread):
    
    def __init__(self, condition, activeAgent="", agent_msg="", master_msg=""):
        Thread.__init__(self)
        self.activeAgent = activeAgent
        self.agentList = []
        
        self.condition = condition
        
        self.agent_msg = agent_msg
        self.master_msg = master_msg
    
    
    def addAgent(self, agentId):
        self.agentList.append(agentId)
    
    
    def run(self):
        while True:
            with self.condition:
                for agentId in self.agentList:
                    self.master_msg.update({agentId : "Place an Order ... "})
                self.condition.notify_all()
                
                while all([msg for msg in self.agent_msg.values()]) is False:
                    print("Waiting for agents ... ")
                    self.condition.wait()
                
                self.agent_msg.clear()
                
                
    def global_report(self):
        ""
                
            
            
