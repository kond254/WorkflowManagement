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


        


    # do smth
    #
    #
    #
    #
    #

    
    @worker.task(task_type="sendConfirmationToCandidate")
    async def send_confirmation_to_candidate(job: Job, email:str):
        print("Job COnfirmation send")
    
    @worker.task(task_type="sendCandidateInterviewDate")
    async def send_candidate_interview_date(job: Job, email:str):
        print("Interview Date send") 


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
