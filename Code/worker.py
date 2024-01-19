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
        corKey=f'{job.process_instance_key}2010'
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
    async def send_job_standards(job: Job, jobType: str, JobName:str, required_experience: int, job_description: str, responsibilities:str, location:str, job_mode:str, weekly_hours: int, pay: int, pto: int, benefits: str, industry:str, min_education_level:str, language:str, number_of_positions: int):
        print("Job standards send")
        print("Inserting into DB")
        db.insert_job_standards_in_db(job.process_instance_key, jobType, JobName, required_experience, job_description, responsibilities, location, job_mode, weekly_hours, pay, pto, benefits, industry, min_education_level, language,  number_of_positions)
       
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

    #move the first 10 entrys in the topcandidateDB and Create Array for Multi Instance Process
    @worker.task(task_type="moveCandidatesToTopDatabase")
    async def move_candidates_to_topDatabase(job: Job):
        db.move_top10_candidates_into_topCandidateDB(job.process_instance_key)
        print("Candidates moved")
        array = db.create_Array_for_MultiInstance(job.process_instance_key)
        print(array)
        print("TopCandidate Array created")
        return{"TopTenCandidatesIDs": array, "ArrayCounter": -1} #-1 that the first element is not supased
         
        
        
    @worker.task(task_type="removeCandidateFromDatabase")
    async def remove_candidates_from_database(job: Job, TopTenCandidatesIDs: list, ArrayCounter: int):
        CandidateID = TopTenCandidatesIDs[ArrayCounter]
        db.remove_candidate_from_topCandidateDB(CandidateID)
        print(f"Candidate with ID {TopTenCandidatesIDs[ArrayCounter]} removed")
    

    @worker.task(task_type="fetchCandidateData")
    async def fetch_TopCandidate_Data(job: Job, TopTenCandidatesIDs: list, ArrayCounter: int):
        ArrayCounter+=1
        CandidateID = TopTenCandidatesIDs[ArrayCounter]
        
        CandidateDetails = db.Join_TopCandidate_with_CandidateDB(CandidateID)
        print(CandidateDetails[0])
        print(f"Top Ten Candidate IDs: {TopTenCandidatesIDs}")
        print(f"Array Counter: {ArrayCounter}")
        data = { }
        keys = ['ProcessID', 'CandidateID', 'first_name', 'last_name', 'gender', 'email', 'linkedin', 'adress', 'city', 'zip_code', 'country', 'age', 'previous_company', 'rating']
        # Use a loop to populate the dictionary
        for key, value in zip(keys, CandidateDetails[0]):
            data[key] = value
        
        data["ArrayCounter"]=ArrayCounter
        
        #
        #
        #delete later
        #
        data["final_selection_passed"]="True"
        #
        #
        #
        #
        #
        return data
        
    # do smth
    #
    #
    #
    #
    #
    @worker.task(task_type="rejectionMailToCandidate")
    async def rejection_mail_to_candidate(job: Job, email:str):
        print("Rejection Mail send") 
    
    @worker.task(task_type="sendConfirmationToCandidate")
    async def send_confirmation_to_candidate(job: Job, email:str):
        print("Job COnfirmation send")
    
    @worker.task(task_type="sendCandidateInterviewDate")
    async def send_candidate_interview_date(job: Job, email:str):
        print("Interview Date send") 


    # create also variables as dbcount and countvar for later stages 
    @worker.task(task_type="checkTopCandidatesAmount")
    async def check_top_candidates_amount(job: Job):
        candidates_in_top_db = db.create_Array_for_MultiInstance(job.process_instance_key)
        return {"remainingCandidatesInTopDB": db.check_amount_of_candidates_in_TopCandidateDB(job.process_instance_key)[0][0]>0, "countDB": (len(candidates_in_top_db)), "countVar": 0, "RemainingCandidates": candidates_in_top_db, "Beginn": "", "InterviewDate":"", "End":"" }
    
        
    @worker.task(task_type="checkEntrysInCandidateDB")
    async def check_candidates_amount(job: Job):
        
        return {"remainingCandidatesInDB": db.check_amount_of_candidates_in_CandidateDB(job.process_instance_key)[0][0]}
    
    
    
    
    @worker.task(task_type="checkInterviewDate")
    async def check_interview_date(job: Job, countVar: int, RemainingCandidates: list):
        target_date = None
        target_start_time = None
        target_end_time = None
        while(True):        
            start_date =datetime.datetime.now() + datetime.timedelta(days=7)
            end_date = start_date + datetime.timedelta(days=30)
            random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

            hour = random.randint(8, 16)
            minute = random.choice(['00', '15', '30', '45'])

            target_date = random_date.strftime("%Y-%m-%d")
            target_start_time=f'{hour}:{minute}'
            target_end_time=f'{hour+1}:{minute}'
            print(f'{target_date} _ {target_start_time} - {target_end_time}')
            if db.check_interview_dates(target_date, target_start_time, target_end_time):
                print('Time found')
                break
            time.sleep(5)
            
        #date found --> make entry in db
        event_ids = db.make_entry_in_calendar(target_date, target_start_time, target_end_time, RemainingCandidates[countVar])
        time.sleep(5)
        print(countVar)
        print(RemainingCandidates)
        countVar+=1
        return{"countVar": countVar, "InterviewDate": target_date, "Beginn": target_start_time, "End": target_end_time, "CandidateID": RemainingCandidates[countVar-1], "EventIDs": event_ids}
        
          
    @worker.task(task_type="checkInterviewerAnswer")
    async def check_interviewer_answer(job: Job, hrRepAnswer: str, hrManagerAnswer: str, vpAnswer: str):
        if hrRepAnswer == "False" or hrManagerAnswer== "Flase" or vpAnswer =="False":
            return{"onlyConfirmations": False}
        else:
            return{"onlyConfirmations": True}
        
    @worker.task(task_type="storeDateAnswer")
    async def store_date_answer(job: Job, CandidateID: int, InterviewAccepted: bool):
        db.store_answer(InterviewAccepted, CandidateID)
        

    @worker.task(task_type="checkingDateAnswers")
    async def checking_date_answers(job: Job):
        posAnswers = db.checking_date_answers(job.process_instance_key)[0][0]
        entrysInDb = db.check_amount_of_candidates_in_TopCandidateDB(job.process_instance_key)[0][0]
        percentage = (posAnswers/entrysInDb)*100
        if percentage > 60:
            return{"percentage": True}
        else:
            return{"percentage": False}
        
    @worker.task(task_type="removeDeclinedCandidates")
    async def delete_candidates_declined_interview(job: Job):
        db.delete_TopCandidates(job.process_instance_key)
        
    @worker.task(task_type="deleteConflictingInterviews")
    async def delete_company_calendry_entries(job: Job):
        print("Deleting Conflicting Interviews")
        candidates_in_top_db=db.delete_calendry_entries(job.process_instance_key)
        time.sleep(60)
        return {"RemainingCandidates": candidates_in_top_db, "countVar": 0}
        
            
    
    
    @worker.task(task_type="orderByDate")
    async def order_TopCandidates_by_interview(job: Job):
        return {"InterviewOrder": db.order_by_interview(job.process_instance_key)}

    @worker.task(task_type="cancelInterviewDateWithInterviewers")
    async def cancle_interview_date_with_interviewers(job: Job, CandidateID: int):
        db.delete_TopCandidate_due_Candidate_rejection(CandidateID)
        return {"InterviewOrder": db.order_by_interview(job.process_instance_key)}

    @worker.task(task_type="calculateEvaluation")
    async def calculate_evaluation(job: Job, ratingHrManager: int, ratingHrRepresentative: int, ratingVP: int):
        finalScore = ratingHrManager + ratingHrRepresentative + ratingVP
        if finalScore > 20:
            return{"finalSelectionPassed": True}
        else:
            return{"finalSelectionPassed": False}
        
    @worker.task(task_type="storeFinalAnswer")
    async def store_final_answer(job: Job, CandidateID: int, JobAccepted: int):
        db.store_job_answer(JobAccepted, CandidateID)
        
    @worker.task(task_type="deleteTopCandidatesDeclinedJob")
    async def delete_topcandidates_declined_job(job: Job):
        db.delete_TopCandidates_final(job.process_instance_key)    
            
    @worker.task(task_type="checkingFinalAnswers")
    async def checking_final_answers(job: Job):
        amount = db.check_amount_of_candidates_in_TopCandidateDB(job.process_instance_key)
        if amount > 0:
            return{"confirmations": True}
        else:
            return{"confirmations": False}
        
    @worker.task(task_type="moveCandidateToNewEmployee")
    async def move_candidates_to_new_employee(job: Job):
        candidates = db.select_new_employees(job.process_instance_key)
        db.join_new_employee_data(job.process_instance_key, candidates)

    @worker.task(task_type="checkingEmployedCandidates")
    async def checking_employed_candidates(job: Job):
        newEmployeeCount = db.check_Count_new_employees(job.process_instance_key)
        numberOfpositions = db.check_number_of_positions(job.process_instance_key)
        if newEmployeeCount == numberOfpositions:
            return{"positionsFilled": True}
        else:
            return{"positionsFilled": False}
        
    @worker.task(task_type="receiveAnswer12")
    async def test(job: Job):
        print("Test")
        x=int(f'{job.process_instance_key}2010')
        print(x)
        print(type(x))
        return{"receiveAnswer": f'{job.process_instance_key}2010'}
    
    @worker.task(task_type="sendWeplacmInfoEmployed")
    async def send_weplacm_info_employed(job: Job):
        newEmployeeCount = db.check_Count_new_employees(job.process_instance_key)
        await cW.sendEmployeeAmount(newEmployeeCount)
    
    @worker.task(task_type="checkInvoice")
    async def check_invoice(job: Job, salarie_sum: int):
        newEmployeeCount = db.check_Count_new_employees(job.process_instance_key)
        Salary = db.check_annual_salary(job.process_instance_key)
        CalculatedSalarySum = newEmployeeCount*Salary
        if CalculatedSalarySum == salarie_sum:
            return{"invoiceCorrect": True}
        else:
            return{"invoiceCorrect": False}
    
    @worker.task(task_type="sendWeplacmInfoWrongInvoice")
    async def send_weplacm_info_wrong_invoice(job: Job):
        await cW.sendFaultyInvoiceInfo()
        print("Faulty Invoice Info send")

    @worker.task(task_type="sendWeplacmInfoPayment")
    async def send_payment(job: Job):
        await cW.sendPayment()
        print("Payment send")

    



    

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
