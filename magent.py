from threading import Thread
from system.agent import Agent

from datetime import datetime

class MAgentThread(Agent, Thread):
    
    def __init__(self, Id, env, event, agent_bus, master_bus, barrier):
        Agent.__init__(self, Id, env)
        Thread.__init__(self)
        self.Id = Id
        self.event = event
        
        self.agent_bus = agent_bus
        self.master_bus = master_bus
        self.barrier = barrier
        
    
    def get_master_bus(self):
        from_master = self.master_bus[self.Id].get()
        msg = from_master["msg"]
        stop = from_master["stop"]
        active = from_master["paper"]
        return msg, stop, active
    
    
    def execute_master_order(self, state, paper_mode=True):
        next_state, reward, event = self.update(state, paper_mode)
        print(" _________ STEP PASS _________")
        return next_state, reward, event
    
    def report_to_master(self, data, finish_step):
        self.agent_bus[self.Id].put({"data" : data, "fstep":finish_step})
        
        
    def stop_simulation(self, currentDate):
        endDate = self.env.end
        print(f" *** endDate : {endDate}")
        #date = datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S")
        date = datetime.strptime(endDate, "%Y-%m-%d")
        
        if currentDate == date:
            self.agent_bus["stop"] = True
            self.master_bus["stop"] = True
            return True
        else:
            return False
    
        
    def run(self):
        state = self.env.reset()
        
        while True:
            # Waitting master order
            print(f"{self.Id} waiting master's signal ... ")
            self.event.wait()
            
            # Get master msg (msg , stop)
            master_bus, master_status, active = self.get_master_bus()
            print(f"{self.Id} - Master signal : {master_bus}")
            
            # Execute order
            state, reward, event = self.execute_master_order(state)    
            print(f"{self.Id} ORDER EXECUTED ")
                
            # Report to master
            self.event.set()
            self.report_to_master(data="action executed...", finish_step = True)
                
            # Signal to stop simulation
            stop = self.stop_simulation(event.date)
                
            # Notify master
            print(f"{self.Id} has finished step")
            
            # Wait other agents to the barrier
            self.barrier.wait()
            
            if stop:
                print(f"--- STOP {self.Id} ----")
                break
        
    


