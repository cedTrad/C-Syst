from threading import Thread
from system.agent import Agent

from datetime import datetime

class MAgentThread(Agent, Thread):
    
    def __init__(self, Id, policy_name, env, condition, agent_bus, master_bus, barrier):
        Agent.__init__(self, Id, policy_name, env)
        Thread.__init__(self)
        self.Id = Id
        self.condition = condition
        
        self.agent_bus = agent_bus
        self.master_bus = master_bus
        self.barrier = barrier
        
    
    def get_master_bus(self):
        from_master = self.master_bus[self.Id].get()
        msg = from_master["msg"]
        stop = from_master["stop"]
        active = from_master["active"]
        return msg, stop, active
    
    
    def execute_master_order(self, state, active):
        if active:
            next_state, reward, event = self.update(state)
            state = next_state
            return state, reward, event, True
        else:
            return state, None, None, False
    
    def report_to_master(self, data, finish_step):
        self.agent_bus[self.Id].put({"data" : "action executed...", "fstep":finish_step})
        
        
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
                while self.master_bus["msg"].get(self.Id) is None:
                    print(f"{self.Id} waiting master's signal ... ")
                    self.condition.wait()
                
                # Get master msg (msg , stop)
                master_bus, master_status, active = self.get_master_bus()
                print(f"{self.Id} - Master signal : {master_bus[0]}")
                
                # Execute order
                state, reward, event, is_executed = self.execute_master_order(state, active)
                if is_executed:
                    print(f"{self.Id} execute order")
                
                # Report to master
                self.report_to_master(data="", finish_step = True)
                
                # Signal to stop simulation
                stop = self.stop_simulation(event.date) if event is not None else False
                
                # Notify master
                self.condition.notify()
                print(f"{self.Id} has finished step")
            
            # Wait other agents to the barrier
            self.barrier.wait()
            
            if stop:
                print(f"--- STOP {self.Id} ----")
                break
        
    


