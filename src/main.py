# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 09:57:36 2019

@author: thejas
"""
import numpy as np
import simpy
from job import job 
from cluster import CommmonMachine
from stats import average_response, cpu_utilization, queue_time_average


RANDOM_SEED = 42
NUM_CPUS = 1  
CPU_SLOT = 0.1
CPU_OVERHEAD = 0.015      
NUM_TERMINALS = 35      
SIM_JOBS = 1000     # Simulation jobs in minutes

################################################################################
def request_cpu(task, ComputeMachine):
    """
    local function which is used to create a process for new/pre-empted job
    """
    global jobs_list
    global queue_count
    if task.number_of_cpu_quantum == 0:
        think_time = np.random.exponential(25)
        print("New job %d is initialized at %.2f with %.2f thinking time and %.2f service time"
              % (task.get_job_id(), task.env.now, think_time, task.get_service_time()))
    
        yield task.env.timeout(think_time)
        print("Job %d ready to request for CPU at %.2f." % (task.get_job_id(), task.env.now))
        task.queue_entry_time = task.env.now
        queue_count[task.queue_entry_time] =1
    with ComputeMachine.cpu.request() as request:
        print("Job %d has requested for CPU at %.2f." % (task.get_job_id(), task.env.now))
        yield request
        print('Job %d enters the queue at %.2f.' % (task.get_job_id(), task.env.now))
        status = yield task.env.process(ComputeMachine.compute(task))
        if status == 1:
            print('Job %d pre-empted at %.2f.' % (task.get_job_id(), task.env.now))
            task.set_service_time(task.get_service_time() - 0.1)
            return task.env.process(request_cpu(task, ComputeMachine))
        else:
            print('Job %d has completed its execution at %.2f.' % (task.get_job_id(),
                                                                   task.env.now))
            task.job_complete_status = True
            queue_count[task.env.now] = -1
            if len(jobs_list) < 1000:
                temp = job(env, job_id = len(jobs_list)+1,
                           service_time = np.random.exponential(0.8))
                task.env.process(request_cpu(temp, ComputeMachine))
                jobs_list[len(jobs_list)+1] = temp
###############################################################################
"""
Execution
"""
###############################################################################
np.random.seed(RANDOM_SEED) # This helps reproducing the results
# Create an environment and start the setup process
jobs_list = {}
queue_count = {}
env = simpy.Environment()
ComputeMachine = CommmonMachine(env, NUM_CPUS, CPU_SLOT, CPU_OVERHEAD)
# Initialize first (num_terminals) jobs
for i in range(NUM_TERMINALS):
    temp = job(env, job_id = i+1, service_time = np.random.exponential(0.8))
    env.process(request_cpu(temp, ComputeMachine))
    jobs_list[i+1] = temp
env.run()
##############################################################################
#statistics  
response_mean, response_max, response_array  = average_response(jobs_list)
cum_queue = queue_time_average(queue_count)
cpu_utilization = cpu_utilization(ComputeMachine, jobs_list)
