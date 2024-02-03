import asyncio

from pyzeebe import create_insecure_channel, ZeebeWorker, Job
import random
from clientWeplacm import *
from db import Databank 
import random   
import datetime
import time
from array import array


# Define the main function where the worker has his tasks
def main():
    # Create a channel for Zeebe worker to communicate with the broker
    channel = create_insecure_channel(hostname="141.26.157.71",
                                      port=26500)
    # Create instances for Weplacm client and database interaction
    print("Channel created")
    cW = ClientWeplacm()
    db = Databank()
    worker = ZeebeWorker(channel)


    #starting Process in WEPLACM to send inital contract information
    @worker.task(task_type="sendContract")
    async def send_contract(job: Job, jobType: str, number_of_positions:int, compensation: float):
        print("-----Starting contract nagotiation-----")
        process_correlation_key=f"{job.process_instance_key}21" #generating correlation key for the following recieve message task
        response = await cW.send_contract_to_weplacm(jobType, number_of_positions, compensation, process_correlation_key)
        print("Contract send")
        print("Job Type: "+jobType)
        print("Number of Positions: "+ str(number_of_positions))
        print("compensation: "+str(compensation))
        print("Rsponse: " + str(response))
        return{"contract_cycle": 0, "Reminder": False, "process_correlation_key": process_correlation_key, "correlation_key_weplacm": response}
        #return{"contract_cycle": 0, "Reminder": False, "process_correlation_key": process_correlation_key, "correlation_key_weplacm": 1}

    #check the answer and log responses
    @worker.task(task_type="checkContractAnswer")
    async def check_contract_answer(job: Job, suggestion: float, compensation:float, contract_signed: bool, capacity: bool, contract_cycle: int):
        print("-----Contract answer checked-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        print("New Compensation: "  + str(suggestion))
        print("Original Compensation: "  + str(compensation))
        print("Signed: "  + str(contract_signed))
        print("Capacity: "  + str(capacity))
        print("Contract Cycle: "  + str(contract_cycle))

        
        #validate correctness of answer
        if((compensation==suggestion) & contract_signed & capacity): 
            return {"compensation": suggestion,
                    "contract_signed": contract_signed,
                    "capacity": capacity
                    }
        else:
            return {"suggestion": suggestion,
                    "contract_signed": False,
                    "capacity": capacity,
                    "contract_cycle": contract_cycle+1 #contract_cycle is here to prevent infinit loop
                    }
            
            
            
    #send the adjusted contract to WEPLACM    
    @worker.task(task_type="sendAdjustedContract")
    async def send_adjusted_contract(job: Job, jobType: str, number_of_positions:int, compensation: float, contract_cycle:int, correlation_key_weplacm: int):
        print("-----Send Adjusted Contract-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        process_correlation_key=f"{job.process_instance_key}21{contract_cycle}"
        await cW.send_adjusted_contract_to_weplacm(jobType, number_of_positions, compensation, process_correlation_key, correlation_key_weplacm)
        print("Contract send")
        print("Job Type: "+jobType)
        print("Number of Positions: "+ str(number_of_positions))
        print("compensation: "+str(compensation))
        return {"process_correlation_key": process_correlation_key}

    
    #Cancel Contract nagotiation because it cycled too many times
    @worker.task(task_type="cancelContract")
    async def cancel_contract_negotiation(job: Job, correlation_key_weplacm: int):
        print("-----Cancel Contract nagotiation with WEPLACM-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        await cW.cancel_contract(correlation_key_weplacm)
        print("Contract Negotiation cancelled")

        
    # save the Contract in Database    
    @worker.task(task_type="saveContract")
    async def save_contract(job: Job, compensation: float, contract_signed: bool):
        print("-----Save the Contract-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        print("Inserting into DB")
        db.insert_contract_in_systemdb(job.process_instance_key, contract_signed, compensation)
        
        
    #checking if reminder was already send
    @worker.task(task_type="checkReminder")
    async def check_reminder(job: Job, Reminder: bool):
        print("-----Check if contract reminder is already sent-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        if(Reminder==False):
            return{"ReminderExist": False, "Reminder": True}
        else: 
            return{"ReminderExist": True}

    #Send a reminder for contract nagotiation 
    @worker.task(task_type="contractReminder")
    async def contract_reminder(job: Job, ReminderExist: bool, correlation_key_weplacm: int):
        print("-----Send a contract Reminder----")
        print("Process Instance Key: " +str(job.process_instance_key))
        await cW.contract_Reminder(correlation_key_weplacm)
        print("Reminder sent")
       
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker.work())
    except KeyboardInterrupt:
        pass
    

if __name__ == '__main__':
    main()
