from threading import Thread, Lock, Condition, Event
from system.agent import Agent


class MAgentThread(Agent, Thread):
    
    def __init__(self, Id, symbol, allocation, env, policy_name, condition, agent_msg="", master_msg=""):
        Agent.__init__(self, symbol, allocation, env, policy_name)
        Thread.__init__(self)
        self.Id = Id
        self.condition = condition
        
        self.agent_msg = agent_msg
        self.master_msg = master_msg
        
    
    def run(self):
        state = self.env.reset()
        i = 0
        while True:
            with self.condition:
                print(f"{self.Id} wait msg from the master ...")
                
                while self.master_msg.get(self.Id) is None:
                    self.condition.wait()
                    
                print (f"{self.Id} get msg from the master")
                try:
                    next_state, reward, event = self.update(state)
                    state = next_state
                    i += 1
                except StopIteration:
                    break
                    
                trades_data = self.env.journal.trades_data.copy()
                if "Close" in self.asset.state:
                    self.post_trade(event=event, trades_data = trades_data, close_trade=True)
                    
                self.agent_msg[self.Id] = "order send ..."
                print(f"agent {self.Id} place order successfully ... ")
                self.condition.notify()
            
        
    


class MAgentMP(Agent, Thread):
    
    def __init__(self, symbol, allocation, env, policy_name, condition):
        Agent.__init__(self, symbol, allocation, env, policy_name)
        Thread.__init__(self)
        self.condition = condition
        
    
    def run(self):
        state = self.env.reset()
        i = 0
        while True:
            self.condition.notify()
            try:
                next_state, reward, event = self.update(state)
                state = next_state
                i += 1
            except StopIteration:
                break
                
            trades_data = self.env.journal.trades_data.copy()
            if "Close" in self.asset.state:
                self.post_trade(event=event, trades_data = trades_data, close_trade=True)
            
            self.communication_lock.wait()



