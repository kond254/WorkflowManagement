import asyncio

from pyzeebe import create_insecure_channel, ZeebeWorker, Job
import random
from clientWeplacm import *
from db import Databank 
import random   
import datetime
import time
from array import array

def main():
    channel = create_insecure_channel(hostname="141.26.157.71",
                                      port=26500)
    
    print("Channel created")
    cW = ClientWeplacm()
    db = Databank()
    worker = ZeebeWorker(channel)

    @worker.task(task_type="countIncrease")
    async def count_increase(job: Job, count: int):
        print(count)
        count = count+1
        print(count)
        job.variables.update({"count": count})
        print("Finish")


    #starting Process in WEPLACM to send inital contract information
    @worker.task(task_type="sendContract")
    async def send_contract(job: Job, jobType: str, number_of_positions:int, compensation: float):
        print("Starting contract nagotiation")
        print("Process Instance Key: " +str(job.process_instance_key))
        await cW.sendContract(jobType, number_of_positions, compensation)
        print("Contract send")
        print("Job Type: "+jobType)
        print("Number of Positions: "+ str(number_of_positions))
        print("compensation: "+str(compensation))
        process_correlation_key=f"{job.process_instance_key}21"
        return{"contract_cycle": 0, "ReminderExist": False, "process_correlation_key": process_correlation_key}

    #check the answer and print responses
    @worker.task(task_type="checkContractAnswer")
    async def check_contract_answer(job: Job, suggestion: float, compensation:float, contract_signed: bool, capacity: bool, contract_cycle: int):
        print("Contract answer checked")
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
                    "contract_cycle": contract_cycle+1 
                    }
    #send the adjusted contract to WEPLACM    
    @worker.task(task_type="sendAdjustedContract")
    async def send_adjusted_contract(job: Job, jobType: str, number_of_positions:int, compensation: float, contract_cycle:int):
        print("Adjusted Contract send")
        print("Process Instance Key: " +str(job.process_instance_key))
        await cW.sendContract(jobType, number_of_positions, compensation)
        print("Contract send")
        print("Job Type: "+jobType)
        print("Number of Positions: "+ str(number_of_positions))
        process_correlation_key=f"{job.process_instance_key}21{contract_cycle}"
        print("compensation: "+str(compensation))
        return {"process_correlation_key": process_correlation_key}

    
    #Cancel Contract nagotiation because it cycled too many times
    @worker.task(task_type="cancelContractNegotiation")
    async def cancel_contract_negotiation(job: Job):
        print("Contract Negotiation cancelled")
        print("Process Instance Key: " +str(job.process_instance_key))
        
    @worker.task(task_type="saveContract")
    async def save_contract(job: Job, compensation: float, contract_signed: bool):
        print("Contract saved")
        print("Process Instance Key: " +str(job.process_instance_key))
        
        print("Inserting into DB")
        db.insert_contract_in_systemdb(job.process_instance_key, contract_signed, compensation)
        
        
    #checking if reminder was already send
    @worker.task(task_type="contractReminder")
    async def contract_reminder(job: Job, ReminderExist: bool):
        print("Contract reminder send")
        if(ReminderExist==False):
            return{"ReminderExist": True}
       
       
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker.work())
    except KeyboardInterrupt:
        pass
    

if __name__ == '__main__':
    main()
