# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 11:59:13 2019

@author: maily
"""


class job():
    """
    A job object with terminal and service time information
    """
    def __init__(self, env, job_id, service_time):
        self.env = env
        self.__job_id = job_id
        self.__service_time = service_time
        self.job_complete_status = False
        self.number_of_cpu_quantum = 0
        self.cpu_in_time = []
        self.cpu_out_time = []
        self.queue_entry_time = None
    
    def get_job_id(self):
        return self.__job_id
    
    def get_service_time(self):
        return self.__service_time
    
    def set_service_time(self, time):
        self.__service_time = time
        return




        