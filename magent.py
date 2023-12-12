from threading import Thread
from system.agent import Agent


class MAgentThread(Agent, Thread):
    
    def __init__(self, agentId, symbol, allocation, env, policy_name, condition, agent_bus, master_bus, barrier):
        Agent.__init__(self, agentId, symbol, allocation, env, policy_name)
        Thread.__init__(self)
        self.agentId = agentId
        self.condition = condition
        
        self.agent_bus = agent_bus
        self.master_bus = master_bus
        
        self.barrier = barrier
    
    
    def is_active(self, master_bus):
        return master_bus["activeAgent"] == self.agentId
    
    
    def start_work(self):
        ""
        
    def end_work(self, agent_bus):
        agent_bus
    
    
    def run(self):
        state = self.env.reset()
        
        while True:    
            with self.condition:
                while self.master_bus["agent"].get(self.agentId) is None:
                    print(f"{self.agentId} waiting master's signal ... ")
                    self.condition.wait()
                
                print(f"{self.agentId} get master signal ... ")
                boss_msg = self.master_bus["agent"].pop(self.agentId, None)
                print(f"{self.agentId} - Master signal : {boss_msg}")
                
                try:
                    if self.is_active(self.master_bus):
                        next_state, reward, event = self.update(state)
                        state = next_state
                        print("date : ",event.date)

                except StopIteration:
                    #self.agent_bus["msg"].update({self.agentId : "stop"})
                    self.agent_bus.update({"stop" : True})
                    print(f"---------- STOP {self.agentId}----------")
                    stop = True
                    self.master_bus.update({"stop" : True}) 
                    self.condition.notify()
                    
                    break
                
                self.agent_bus["msg"].update({self.agentId : "action executed ... "})
                self.condition.notify()
            
            self.barrier.wait()
            
            if self.agent_bus.get("stop") is True:
                print(f"{self.agentId} STOP")
                break
        
        

