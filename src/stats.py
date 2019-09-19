# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 10:03:27 2019

@author: thejas
"""
import numpy as np

def average_response(jobs_list):
    response_time = []
    for i in range(1000):
        task = jobs_list[i+1]
        response_time.append(task.cpu_out_time[-1]-task.queue_entry_time)
    return np.array(response_time).mean(), max(response_time), response_time
##############################################################################
def queue_time_average(que_dict):
    exit_count = 0
    time_prev = 0
    cum_sum = 0
    out = 0
    for key, val in que_dict.items():
        if exit_count == 1000 : 
            return out/key
        if val == -1:
            exit_count +=1
        cum_sum += val
        out += (key - time_prev)*cum_sum
        time_prev = key
    return out/key
###############################################################################
def cpu_utilization(ComputeMachine, jobs_list):
    time_utilized = ComputeMachine.cpu_utilization_time
    if jobs_list[1000].job_complete_status == True:
        total_time = jobs_list[1000].cpu_out_time[-1]
    else:
        print("1000th job not yet completed")
        return
    return time_utilized/total_time

