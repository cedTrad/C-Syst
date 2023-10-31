from threading import Thread, Condition, Event


class MasterAgentThread(Thread):
    
    def __init__(self, condition, activeAgent="", agent_msg="", master_msg="", msg_bus=""):
        Thread.__init__(self)
        self.activeAgent = activeAgent
        self.agentList = []
        
        self.condition = condition
        
        self.agent_msg = agent_msg
        self.master_msg = master_msg
        self.msg_bus = msg_bus
    
    def addAgent(self, agentId):
        self.agentList.append(agentId)
    
    def assign_work(self):
        ""
    
    def run(self):
        while True:
            with self.condition:
                for agentId in self.agentList:
                    self.master_msg.update({agentId : "Place an Order ... "})
                self.condition.notify_all()
                
                
                while 1:
                    for agentId in self.agentList():
                        if self.agent_msg[agentId] is None:
                            self.condition.wait()
                            
                
                
            
            
