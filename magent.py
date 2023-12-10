from threading import Thread
from system.agent import Agent


class MAgentThread(Agent, Thread):
    
    def __init__(self, agentId, symbol, allocation, env, policy_name, condition, agent_msg, master_msg, barrier):
        Agent.__init__(self, agentId, symbol, allocation, env, policy_name)
        Thread.__init__(self)
        self.agentId = agentId
        self.condition = condition
        
        self.agent_msg = agent_msg
        self.master_msg = master_msg
        
        self.barrier = barrier
        
    
    def run(self):
        state = self.env.reset()
        i = 0
        while True:    
            with self.condition:
                while self.master_msg.get(self.agentId) is None:
                    print(f"{self.agentId} waiting master's signal ... ")
                    self.condition.wait()
                
                print(f"{self.agentId} get master signal ... ")
                boss_msg = self.master_msg.pop(self.agentId, None)
                print(f"{self.agentId}- Master signal : {boss_msg}")
                
                try:
                    next_state, reward, event = self.update(state)
                    state = next_state
                    i += 1
                except StopIteration:
                    self.agent_msg.update({self.agentId : "stop"})
                    print(f"---------- STOP {self.agentId}----------")
                    self.condition.notify()
                    break
                        
                        
                print(f"{self.agentId} - date : {event.date}, {self.symbol}")
                
                self.agent_msg.update({self.agentId : "action executed ... "})
                
                self.condition.notify()
            
            self.barrier.wait()
        
        

