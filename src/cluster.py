# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 10:03:27 2019

@author: thejas
"""

import simpy 

class CommmonMachine():
    """A Common machine has limited number of CPUs that can run in parallel.

    Jobs have to request one of the CPUs. When they got one, they
    can utilize the CPU for CPU_SLOT time and get pre-empted and wait for
    their turn in the queue.

    """
    def __init__(self, env, num_cpus, cpu_slot, cpu_overhead):
        self.env = env
        self.cpu = simpy.Resource(env, num_cpus)
        self.cpu_slot = cpu_slot
        self.cpu_overhead = cpu_overhead
        self.cpu_utilization_time = 0

    def compute(self, task):
        """The compute method tries to utilize the cpu for min(CPU_slot, request_time)
        and then generates a new process with the same job with new request_time"""
        if task.get_service_time() > self.cpu_slot:
            task.cpu_in_time.append(task.env.now)
            task.cpu_out_time.append(task.env.now+0.1)
            self.cpu_utilization_time += (self.cpu_slot + self.cpu_overhead)
            yield self.env.timeout(self.cpu_slot + self.cpu_overhead)
            print("Job", task.get_job_id(), 
                  "executed for 1 CPU slot and has joined the queue")
            task.number_of_cpu_quantum +=1
            return 1
        else:
            task.cpu_in_time.append(task.env.now)
            task.cpu_out_time.append(task.env.now+task.get_service_time())
            self.cpu_utilization_time += (task.get_service_time() + self.cpu_overhead)
            yield self.env.timeout(task.get_service_time() + self.cpu_overhead)
            task.number_of_cpu_quantum +=1
            print("Job", task.get_job_id(), 
                  "execution completed and its terminal has entered  thinking state")
            return -1   
                
        
        
        
        
        
        


