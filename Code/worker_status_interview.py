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
    db = Databank()
    worker = ZeebeWorker(channel)

    

        
    @worker.task(task_type="checkEntrysInCandidateDB")
    async def check_candidates_amount(job: Job):
        
        return {"remainingCandidatesInDB": db.check_amount_of_candidates_in_CandidateDB(job.process_instance_key)[0][0]}
    
    
    
    #Check possible interview Dates and reserve them for everyone neccessary for the interview
    @worker.task(task_type="checkInterviewDate")
    async def check_interview_date(job: Job, candidate_id:int):
        print("-----Checking possible Interview Dates-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        target_date = None
        target_start_time = None
        target_end_time = None
        # search as long as a possible date and time is found
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
        #date will also be filled in respective column of candidate 
        event_ids = db.make_entry_in_calendar(target_date, target_start_time, target_end_time, candidate_id)
        time.sleep(5)
        print(candidate_id)
        return{"InterviewDate": target_date, "Beginn": target_start_time, "End": target_end_time, "CandidateID": candidate_id, "EventIDs": event_ids}
        
    #check 
    #@worker.task(task_type="checkInterviewerAnswer")
    #async def check_interviewer_answer(job: Job, hrRepAnswer: str, hrManagerAnswer: str, vpAnswer: str):
    #    if hrRepAnswer == "False" or hrManagerAnswer== "Flase" or vpAnswer =="False":
    #        return{"onlyConfirmations": False}
    #    else:
    #        return{"onlyConfirmations": True}
    
    
    # send Candidate the Interview Date
    @worker.task(task_type="sendCandidateInterviewDate")
    async def send_candidate_interview_date(job: Job):
        print("-----Sending the Interview Date-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        ######################
        ###do smth############
        ######################
        print("Interview Date send") 
    
    #Store the answer of the candidate
    @worker.task(task_type="storeDateAnswer")
    async def store_date_answer(job: Job, candidate_id: int, InterviewAccepted: bool):
        print("-----Answer of Candidate recieved an stored-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        db.store_answer(InterviewAccepted, candidate_id)
        
    #Check Candidates answer and calculate percentage of acceptance 
    @worker.task(task_type="checkingDateAnswers")
    async def checking_date_answers(job: Job):
        print("-----Checking Answers for Candidates-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        #Database request to calculate how many answers should be recieved
        posAnswers = db.checking_date_answers(job.process_instance_key)[0][0]
        entrysInDb = db.check_amount_of_candidates_in_TopCandidateDB(job.process_instance_key)[0][0]
        percentage = (posAnswers/entrysInDb)*100
        if percentage > 30:
            return{"percentage": True}
        else:
            return{"percentage": False}
        
    #Remove all candidates that declined are didnt answered    
    @worker.task(task_type="removeDeclinedCandidates")
    async def delete_candidates_declined_interview(job: Job):
        print("-----Remove Candidates from Database that declined-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        db.delete_TopCandidates(job.process_instance_key)
        
        
    #Delete Interview Dates where the candidate can not go if we dont have enough responses
    @worker.task(task_type="deleteConflictingInterviews")
    async def delete_company_calendry_entries(job: Job):
        print("-----Delete Interviews-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        candidates_in_top_db=db.delete_calendry_entries(job.process_instance_key)
        time.sleep(5)
        return {"RemainingCandidates": candidates_in_top_db, "countVar": 0}
        
            
    
    #Create an array of candidates which are ordered by the interview dates 
    @worker.task(task_type="orderByDate")
    async def order_TopCandidates_by_interview(job: Job):
        print("-----Order Interviews by Date-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        #creating new corelation key for next recieving message 
        proccess_corelation_key=f"{job.process_instance_key}2I16"
        print(proccess_corelation_key)
        return {"proccess_corelation_key": proccess_corelation_key, "InterviewOrder": db.order_by_interview(job.process_instance_key)}


    #Delete candidate once we get a cancelation from this candidate
    @worker.task(task_type="cancelInterviewDateWithInterviewers")
    async def cancle_interview_date_with_interviewers(job: Job, CandidateID: int):
        print("-----Delete Candidate and generate new Order-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        db.delete_TopCandidate_due_Candidate_rejection(CandidateID)
        return {"InterviewOrder": db.order_by_interview(job.process_instance_key)}

    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(worker.work())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
