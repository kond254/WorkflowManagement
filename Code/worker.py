import asyncio

from pyzeebe import create_insecure_channel, ZeebeWorker, Job
import random
from clientWeplacm import *
from db import Databank 

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
        return{"contract_cycle": 0, "ReminderExist": False}

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
    async def send_adjusted_contract(job: Job, jobType: str, number_of_positions:int, compensation: float):
        print("Adjusted Contract send")
        print("Process Instance Key: " +str(job.process_instance_key))
        await cW.sendContract(jobType, number_of_positions, compensation)
        print("Contract send")
        print("Job Type: "+jobType)
        print("Number of Positions: "+ str(number_of_positions))
        print("compensation: "+str(compensation))

    
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
        
    #create Job standards in SystemDB
    @worker.task(task_type="sendJobStandards")
    async def send_job_standards(job: Job, jobType: str, JobName:str, required_experience: int, job_description: str, responsibilities:str, location:str, job_mode:str, weekly_hours: int, pay: int, pto: int, benefits: str, industry:str, min_education_level:str, language:str):
        print("Job standards send")
        print("Inserting into DB")
        db.insert_job_standards_in_db(job.process_instance_key, jobType, JobName, required_experience, job_description, responsibilities, location, job_mode, weekly_hours, pay, pto, benefits, industry, min_education_level, language)
       
    #receive Candidates from WEPLACM
    @worker.task(task_type="storeAndSortCandidates")
    async def store_and_sort_candidates(job: Job, candidates):#, first_name: str, last_name: str, gender: str, email:str, linkedin: str, adress: str, city: str, zip_code: str, country: str, age: int, previous_company: str, rating: int):
        for candidate in candidates:
            process_id = job.process_instance_key
            first_name = candidate.get("first_name")
            last_name = candidate.get("last_name")
            gender = candidate.get("gender")
            email = candidate.get("email")
            linkedin = candidate.get("linkedin")
            address = candidate.get("adress")  # Note: "adress" is a typo, it should be "address"
            city = candidate.get("city")
            zip_code = candidate.get("zip_code")
            country = candidate.get("country")
            age = candidate.get("age")
            previous_company = candidate.get("previous_company")
            rating = candidate.get("rating")
            db.insert_candidates_in_db(process_id, first_name, last_name, gender, email, linkedin, address, city, zip_code, country, age, previous_company, rating)
            print("Candidate added in CandidateDB")
        print("All Candidates are added in CandidateDB") 

    #move the first 19 entrys in the topcandidateDB
    @worker.task(task_type="moveCandidatesToTopDatabase")
    async def move_candidates_to_topDatabase(self):
        db.move_top10_candidates_into_topCandidateDB()
        print("Candidates moved")



    ##  else:
    ## Worker runs until it will be canceled manually
    ##

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker.work())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
