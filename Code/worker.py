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

    #send confirmation to Candidate about new job
    @worker.task(task_type="sendConfirmationToCandidate")
    async def send_confirmation_to_candidate(job: Job):
        print("-----Send Confirmation to Candidate-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        process_correlation_key=f"{job.process_instance_key}2I15"
        return {"process_correlation_key": process_correlation_key}
        
    
    #Calculate the Evaluation of the 3 interviewer
    @worker.task(task_type="calculatingEvaluation")
    async def calculate_evaluation(job: Job, ratingHrManager: int, ratingHrRepresentive: int, ratingVP: int, candidate_id:int):
        print("-----Calculate Interviewers Answers-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        #calculate the final score
        finalScore = ratingHrManager + ratingHrRepresentive + ratingVP
        print("Candidate ", candidate_id)
        print("FinalScore: ", finalScore)
        # is the final score greater 20 let candidate pass
        if finalScore > 20:
            return{"finalSelectionPassed": True}
        else:
            return{"finalSelectionPassed": False}
        
    #store the final Answer of Candidate
    @worker.task(task_type="storeFinalAnswer")
    async def store_final_answer(job: Job, CandidateID: int, JobAccepted: int):
        print("-----Store the Job Answer for Candidate -----")
        print("Process Instance Key: " +str(job.process_instance_key))
        db.store_job_answer(JobAccepted, CandidateID)
        
        
    # Delete candidate in table when he declined the job
    @worker.task(task_type="deleteTopCandidatesDeclinedJob")
    async def delete_topcandidates_declined_job(job: Job):
        print("-----Delete Candidate-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        db.delete_TopCandidates_final(job.process_instance_key)    
            
            
    #check all final answers
    @worker.task(task_type="checkingFinalAnswer")
    async def checking_final_answers(job: Job):
        print("-----Check all final Answers-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        #get the amount of the total open positions and subtract with the amount of newly employeed candidates
        newEmployeeCount = db.check_Count_new_employees(job.process_instance_key)
        numberOfpositions = db.check_number_of_positions(job.process_instance_key)
        print("NewEmpCOunt ", newEmployeeCount)
        print("NumOfPos ", numberOfpositions)
        openPositions = numberOfpositions - newEmployeeCount
        #get the amount of candidates in top candidate db. When one Candidate is in the table. We have atleast one new employee 
        amount = db.check_amount_of_candidates_in_TopCandidateDB(job.process_instance_key)
        print("Amount ", amount)
        if amount[0][0] <= openPositions:
            return{"confirmations": True}
        else:
            return{"confirmations": False, "OpenPositions": openPositions}
        
    #Select Candidates which will be rejected
    @worker.task(task_type="selectCandidatesToReject")
    async def select_candidates_to_reject(job: Job, OpenPositions: int):
        print("-----Candidates to reject-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        amount = db.check_amount_of_candidates_in_TopCandidateDB(job.process_instance_key)[0][0]
        print("Amount ", amount)
        print("OpenPositions ", OpenPositions)
        while amount > OpenPositions:
            #Select ID from candidate to reject
            rejectedCandidate = db.rejected_candidates(job.process_instance_key)
            ######################
            ###do smth Mail#######
            ######################
            print("Informed Candidate about rejection")
            print(rejectedCandidate)
            #Remove candidate from TopCandidateDB
            db.remove_candidate_from_topCandidateDB(rejectedCandidate)
            amount-=1
            print("newAmount: ", amount)
        

    #Create new Employee
    @worker.task(task_type="moveCandidateTonewEmployee")
    async def move_candidates_to_new_employee(job: Job):
        print("-----From Candidate to Employee-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        candidates = db.select_new_employees(job.process_instance_key)
        db.join_new_employee_data(candidates)


    # Check how many Candidates where employed
    @worker.task(task_type="checkingEmployedCandidatesFinal")
    async def checking_employed_candidates(job: Job):
        print("-----Employmend status of current process-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        newEmployeeCount = db.check_Count_new_employees(job.process_instance_key)
        numberOfpositions = db.check_number_of_positions(job.process_instance_key)
        if newEmployeeCount == numberOfpositions:
            return{"positionsFilled": True}
        else:
            return{"positionsFilled": False}

    #sending WEPLACM info about new employment 
    @worker.task(task_type="sendWeplacmInfoEmployed")
    async def send_weplacm_info_employed(job: Job, correlation_key_weplacm):
        print("-----Sending information about new employees to WEPLACM-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        newEmployeeCount = db.check_Count_new_employees(job.process_instance_key)
        process_correlation_key=f"{job.process_instance_key}28"
        # await cW.sendEmployeeAmount(newEmployeeCount, correlation_key_weplacm, process_correlation_key)
        return {"process_correlation_key": process_correlation_key}
    
    #Check invoice
    @worker.task(task_type="checkInvoice")
    async def check_invoice(job: Job, salarie_sum: int):
        print("-----Check Invoice for correctness-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        newEmployeeCount = db.check_Count_new_employees(job.process_instance_key)
        Salary = db.check_annual_salary(job.process_instance_key)
        compensation = db.select_contract_compensation(job.process_instance_key)
        #WEPLACM gets payed for each candidate we employed 
        CalculatedSalarySum = newEmployeeCount*Salary*compensation
        #does the invoice add up to our callculations
        if CalculatedSalarySum == salarie_sum:
            return{"invoiceCorrect": True}
        else:
            return{"invoiceCorrect": False}
        
    #send weplacm info about wrong invoice 
    @worker.task(task_type="sendWeplacmInfoWrongInvoice")
    async def send_weplacm_info_wrong_invoice(job: Job, correlation_key_weplacm: int):
        print("-----Sending WEPLACM Information about wrong Invoice-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        # await cW.sendFaultyInvoiceInfo(correlation_key_weplacm)
        print("Faulty Invoice Info send")

    #sending WEPLACM info about payment
    @worker.task(task_type="sendWeplacmInfoPayment")
    async def send_payment(job: Job, correlation_key_weplacm: int):
        print("-----Sending WEPLACM information that payment in on the way-----")
        print("Process Instance Key: " +str(job.process_instance_key))
        # await cW.sendPayment(correlation_key_weplacm)
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
