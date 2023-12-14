from threading import Thread
from system.agent import Agent

from datetime import datetime

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
        msg = self.master_bus["msg"].pop(self.agentId, None)
        stop = self.master_bus["stop"]
        active = self.master_bus["activeAgent"] == self.agentId
        return msg, stop, active
    
    
    def execute_master_order(self, state, active):
        if active:
            next_state, reward, event = self.update(state)
            state = next_state
            return state, reward, event, True
        else:
            return state, None, None, False
    
    def report_to_master(self, data, finish_step):
        self.agent_bus["msg"].update({self.agentId : "action executed ... "})
        self.agent_bus["fstep"].update({self.agentId : finish_step})
        
        
    def stop_simulation(self, currentDate):
        endDate = self.env.end
        date = datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S")
        
        if currentDate == date:
            self.agent_bus["stop"] = True
            self.master_bus["stop"] = True
            return True
        else:
            return False
    
        
    def run(self):
        state = self.env.reset()
        
        while True:
            with self.condition:
                
                # Waitting master order
                while self.master_bus["msg"].get(self.agentId) is None:
                    print(f"{self.agentId} waiting master's signal ... ")
                    self.condition.wait()
                
                # Get master msg (msg , stop)
                master_msg, master_status, active = self.get_master_bus()
                print(f"{self.agentId} - Master signal : {master_msg[0]}")
                
                # Execute order
                state, reward, event, is_executed = self.execute_master_order(state, active)
                if is_executed:
                    print(f"{self.agentId} execute order")
                
                # Report to master
                self.report_to_master(data="", finish_step = True)
                
                # Signal to stop simulation
                stop = self.stop_simulation(event.date) if event is not None else False
                
                # Notify master
                self.condition.notify()
                print(f"{self.agentId} has finished step")
            
            # Wait other agents to the barrier
            self.barrier.wait()
            
            if stop:
                print(f"--- STOP {self.agentId} ----")
                break
        
    


