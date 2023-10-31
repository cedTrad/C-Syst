from threading import Thread, Lock, Condition, Event
from system.agent import Agent


class MAgentThread(Agent, Thread):
    
    def __init__(self, agentId, symbol, allocation, env, policy_name, condition, agent_msg="", master_msg="", msg_bus=""):
        Agent.__init__(self, agentId, symbol, allocation, env, policy_name)
        Thread.__init__(self)
        self.agentId = agentId
        self.condition = condition
        
        self.agent_msg = agent_msg
        self.master_msg = master_msg
        self.msg_bus = msg_bus
    
    
    def msg_to_master(self, msg):
        self.agent_msg.append(msg)
    
    def get_msg_from_master(self, msg):
        self.master_msg.append(msg)
    
    
    def wait_msg_from_master(self):
        while self.master_msg.get(self.agentId) is None:
            print(f" {self.agentId} wait msg from master ... ")
            self.condition.wait()
        
    def notify_to_master(self):
        print(f" {self.agentId} send msg to master ... ")
        self.condition.notify()
        self.condition.notify_all()
        
    
    def run(self):
        state = self.env.reset()
        i = 0
        while True:
            with self.condition:
                
                self.wait_msg_from_master()                                
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
            
        
    


class MAgentThread2(Agent, Thread):
    
    def __init__(self, agentId, symbol, allocation, env, policy_name, condition, agent_msg="", master_msg="", barrier=""):
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
                    print(f"{self.agentId} en attente des ordres du master ... ")
                    self.condition.wait()
                    
                get_msg = self.master_msg.get.pop(self.agentId)
                
                try:
                    next_state, reward, event = self.update(state)
                    state = next_state
                    i += 1
                except StopIteration:
                    break
                        
                trades_data = self.env.journal.trades_data.copy()
                if "Close" in self.asset.state:
                    self.post_trade(event=event, trades_data = trades_data, close_trade=True)
                print(f"{self.agentId} - date : {event.date}, {self.symbol}")
                
                self.condition.notify()
            
            self.barrier.wait()
            