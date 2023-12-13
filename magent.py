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
        
    
    def get_master_bus(self):
        msg = self.master_bus["agent"].pop(self.agentId, None)
        stop = self.master_bus["stop"]
        return msg, stop
    
    def is_active(self):
        return self.master_bus["activeAgent"] == self.agentId
    
    def execute_master_order(self, state):
        if self.is_active():
            next_state, reward, event = self.update(state)
            state = next_state
            return state, reward, event, True
        else:
            return state, None, None, False
    
    def report_to_master(self):
        self.agent_bus["msg"].update({self.agentId : "action executed ... "})
        
        
    def end_simulation(self, currentDate):
        if currentDate == self.env.end:
            self.agent_bus["stop"] = True
            self.master_bus["stop"] = True
        
        if self.agent_bus["stop"] or self.master_bus["stop"]:
            return True
    
    
    def run(self):
        state = self.env.reset()
        
        while True:    
            with self.condition:
                
                # Waitting master order
                while self.master_bus["agent"].get(self.agentId) is None:
                    print(f"{self.agentId} waiting master's signal ... ")
                    self.condition.wait()
                
                # Get master msg (msg , stop)
                master_msg = self.get_master_bus()
                print(f"{self.agentId} - Master signal : {master_msg[0]}")
                
                # Execute order
                state, reward, event, is_executed = self.execute_master_order(state)
                self.end_simulation(event.date)
                
                # Report to master
                self.report_to_master()
                
                stop = self.end_simulation(event.date)
                self.condition.notify()
            
            # Wait other agents to the barrier
            self.barrier.wait()
            
            if stop:
                print(f"--- STOP {self.agentId} ----")
                break
        
    


