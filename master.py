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
    
    
    def run(self):
        while True:
            with self.condition:
                print("**** Master ****")
                for agentId in self.agentList:
                    self.master_msg.update({agentId : "Place an Order ... "})
                self.condition.notify_all()
                print("Master a tous les agents , Activez-vous")
                
                
                while all([msg for msg in self.agent_msg.values()]) is False:
                    print("Waiting for agents ... ")
                    self.condition.wait()
                
                print(f" ooo__oooo=> : {self.agent_msg}")
                stop_condition = self.agent_msg == {self.agentList[0] : "stop", self.agentList[1] : "stop"}
                print(f"stop condition : {stop_condition}")
                if stop_condition:
                    print("---------- STOP(Boss) ----------")
                    break
                    
                
                self.agent_msg.update({self.agentList[0] : None, self.agentList[1] : None})
                
                
    def global_report(self):
        ""
                
            
            
