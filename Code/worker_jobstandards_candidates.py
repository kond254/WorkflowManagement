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
    print("-----Channel created-----")
    cW = ClientWeplacm()
    db = Databank()
    # Initialize a Zeebe worker with the created channel
    worker = ZeebeWorker(channel)
    
    
    #create Job standards and insert them into SystemDB
    @worker.task(task_type="sendJobStandards")
    async def send_job_standards(job: Job, jobType: str, JobName:str, required_experience: int, job_description: str, responsibilities:str, location:str, job_mode:str, weekly_hours: int, pay: int, pto: int, benefits: str, industry:str, min_education_level:str, language:str, number_of_positions: int, correlation_key_weplacm: int):
        print("-----Job standards send-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        print("Inserting into DB")
        #generating new correlation key for next recieve answer
        process_correlation_key=f"{job.process_instance_key}22"
        await cW.send_job_standards_to_weplacm(jobType, JobName, required_experience, job_description, responsibilities, location, job_mode, weekly_hours, pay, pto, benefits, industry, min_education_level, language,  number_of_positions, correlation_key_weplacm, process_correlation_key)
        #Insert job standards into the db using the db class (backend)
        db.insert_job_standards_in_db(job.process_instance_key, jobType, JobName, required_experience, job_description, responsibilities, location, job_mode, weekly_hours, pay, pto, benefits, industry, min_education_level, language,  number_of_positions)
        time.sleep(10)
        return {"process_correlation_key": process_correlation_key, "Reminder": False}
    
    # Insquire the status of the candidate search by the other group 
    @worker.task(task_type="inquireCandidateSearchProgress")
    async def inquire_search(job: Job, jobType: str, JobName:str, required_experience: int, job_description: str, responsibilities:str, location:str, job_mode:str, weekly_hours: int, pay: int, pto: int, benefits: str, industry:str, min_education_level:str, language:str, number_of_positions: int, correlation_key_weplacm: int):
        print("-----Inquire Status for Candidate Search-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        process_correlation_key=f"{job.process_instance_key}30"
        await cW.inquire_candidate_search_progress(correlation_key_weplacm, process_correlation_key)
        print("Inquery sent")
    
    #checks if atleast one candidate filled in a position and got employed
    #next process steps will be the invoice  
    @worker.task(task_type="checkingEmployedCandidates")
    async def checking_employed_candidates(job: Job):
        print("-----Check Employed Candidates-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        amount = db.employed_candidates(job.process_instance_key)
        if amount == 0:
            return{"amount": False}
        else:
            return{"amount": True}

    #sending Weplacm the information that we currently employed x number of people to get the invoice 
    @worker.task(task_type="sendWeplacmInfoEmployed")
    async def send_weplacm_info_employed(job: Job, correlation_key_weplacm: int, process_correlation_key: str):
        print("-----Send Weplacm info about the amount of new employees-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        amount = db.employed_candidates(job.process_instance_key)
        print(f"Amount {amount}")
        await cW.send_Employee_Amount(amount, correlation_key_weplacm, process_correlation_key)

    #receive Candidates from WEPLACM
    @worker.task(task_type="storeAndSortCandidates")
    async def store_and_sort_candidates(job: Job, candidates):#, first_name: str, last_name: str, gender: str, email:str, linkedin: str, adress: str, city: str, zip_code: str, country: str, age: int, previous_company: str, rating: int):
        print("-----Store Candidates in DB-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        #getting all the info from each candidate and saving it in the candidate databank using backend 
        for candidate in candidates:
            process_id = job.process_instance_key
            first_name = candidate.get("first_name")
            last_name = candidate.get("last_name")
            gender = candidate.get("gender")
            email = candidate.get("email")
            linkedin = candidate.get("linkedin")
            address = candidate.get("address")  # Note: "adress" is a typo, it should be "address"
            city = candidate.get("city")
            zip_code = candidate.get("zip_code")
            country = candidate.get("country")
            age = candidate.get("age")
            previous_company = candidate.get("previous_company")
            rating = candidate.get("rating")
            db.insert_candidates_in_db(process_id, first_name, last_name, gender, email, linkedin, address, city, zip_code, country, age, previous_company, rating)
            print("Candidate added in CandidateDB")
        print("All Candidates are added in CandidateDB") 
        
    #Setting the new correlation key for the next recieving message 
    @worker.task(task_type="setting_key_for_candidates")
    async def setting_key(job: Job):
            process_correlation_key=f"{job.process_instance_key}23"
            return {"process_correlation_key": process_correlation_key}
        
        
    #move the first 10 entrys in the topcandidateDB and Create Array for Multi Instance Process
    @worker.task(task_type="moveCandidatesToTopDatabase")
    async def move_candidates_to_topDatabase(job: Job):
        print("-----Move Candidates in Top Ten Candidate DB-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        #Databank will select max. 10 Candidates from Candidate Table and make a connection with those candidates and the top candidates table
        db.move_top10_candidates_into_topCandidateDB(job.process_instance_key)
        print("Candidates moved")
        #this array will be used for the following multi instance
        array = db.create_Array_for_MultiInstance(job.process_instance_key)
        print(array)
        print("TopCandidate Array created")
        return{"TopTenCandidatesIDs": array} 
         
    #Removing candidate from the candidate table when HR-Manager declines the candidate
    @worker.task(task_type="removeCandidateFromDatabase")
    async def remove_candidates_from_database(job: Job, candidate_id: int):    
        print("-----Delete Candidate from Candidate Table-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        db.remove_candidate_from_topCandidateDB(candidate_id)
        print(f"Candidate with ID {candidate_id} removed")
        
    
    #fetching data from candidate table to display it in the form
    @worker.task(task_type="fetchCandidateData")
    async def fetch_TopCandidate_Data(job: Job, candidate_id: int):
        print("-----Fetch Candidate Data from Database-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        print(candidate_id)
        print(type(candidate_id))
        #get the data from the databank
        candidate_details = db.Join_TopCandidate_with_CandidateDB(candidate_id)
        print(candidate_details[0])
        data = { }
        keys = ['ProcessID', 'CandidateID', 'first_name', 'last_name', 'gender', 'email', 'linkedin', 'adress', 'city', 'zip_code', 'country', 'age', 'previous_company', 'rating']
        # Use a loop to populate the dictionary
        db.update_switch_for_candidate_in_frontend(candidate_id, 1)
        
        for key, value in zip(keys, candidate_details[0]):
            data[key] = value
    
        data["final_selection_passed"]="True"
        #
        #
        #
        #
        #
        return data
    
    @worker.task(task_type="changeSwitchForFrontendCandidate")
    async def switch_currently_displayed_for_frontend(job: Job, candidate_id: int):
        print("-----Switch currently Displayed-----")
        print("Process Instance Key: " +str(job.process_instance_key))
       
       
        db.update_switch_for_candidate_in_frontend(candidate_id, 0)
    
    
    
    #Write a rejection Mail to the Candidate when HR-Manager declines Candidate
    @worker.task(task_type="rejectionMailToCandidate")
    async def rejection_mail_to_candidate(job: Job):
        print("-----Inform Candidate about Rejection-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        print("Rejection Mail send") 
        
        
    #Check if any top candidate remains in top candidate table
    @worker.task(task_type="checkTopCandidatesAmount")
    async def check_top_candidates_amount(job: Job):
        print("-----Checking Top Candidate Table-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        #create new array for next multi instance (when any candidate passes)
        candidates_in_top_db = db.create_Array_for_MultiInstance(job.process_instance_key)
        #generating new correlation key for next recieving message task
        process_correlation_key=f"{job.process_instance_key}2I10"
        return {"process_correlation_key": process_correlation_key, "remainingCandidatesInTopDB": db.check_amount_of_candidates_in_TopCandidateDB(job.process_instance_key)[0][0]>0, "RemainingCandidates": candidates_in_top_db }
    
    
       
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker.work())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
