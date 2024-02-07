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
        # Create instances for Weplacm client and database interaction
        print("Channel created")
        cW = ClientWeplacm()
        db = Databank()
        worker = ZeebeWorker(channel)

        
        @worker.task(task_type="getProcessIDforCamunda")
        async def retrieveProcessId(job:Job):
                print("-----ProcessID selected-----")
                return {"ProcessIDforFrontend": str(job.process_instance_key)}
        
        

        #starting Process in WEPLACM to send inital contract information
        @worker.task(task_type="setProcessIDforFrontend")
        async def set_processid_frontend(job: Job):
                return {'processIDforFrontend': str(job.process_instance_key)}
                #return{"contract_cycle": 0, "Reminder": False, "process_correlation_key": process_correlation_key, "correlation_key_weplacm": 1}
                
                
        #starting Process in WEPLACM to send inital contract information
        @worker.task(task_type="sendContract")
        async def send_contract(job: Job, jobType: str, number_of_positions:int, compensation: float):
                print("-----Starting contract nagotiation-----")
                process_correlation_key=f"{job.process_instance_key}21" #generating correlation key for the following recieve message task
       
                await cW.send_contract_to_weplacm(jobType, number_of_positions, compensation, process_correlation_key)

                print("Contract send")
                print("Job Type: "+jobType)
                print("Number of Positions: "+ str(number_of_positions))
                print("compensation: "+str(compensation))

                return{"contract_cycle": 0, "Reminder": False, "process_correlation_key": process_correlation_key}
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
                        db.delete_contract_in_contract_phase(job.process_instance_key)
                        return {"compensation": suggestion,
                        "contract_signed": contract_signed,
                        "capacity": capacity
                        }
                else:
                        db.insert_contract_in_contract_phase(job.process_instance_key, compensation, suggestion)
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
                db.delete_contract_in_contract_phase(job.process_instance_key)
                await cW.send_adjusted_contract_to_weplacm(jobType, number_of_positions, compensation, process_correlation_key, correlation_key_weplacm)
                print("Contract send")
                print("Job Type: "+jobType)
                print("Number of Positions: "+ str(number_of_positions))
                print("compensation: "+str(compensation))
                return {"process_correlation_key": process_correlation_key}

        
        #Cancel Contract nagotiation because it cycled too many times
        @worker.task(task_type="cancelContract")
        async def cancel_contract_negotiation(job: Job, correlation_key_weplacm: int):
                db.delete_contract_in_contract_phase(job.process_instance_key)
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



        #
        #
        #Job standards
        #
        #
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
        async def checking_employed_candidates2(job: Job):
                print("-----Check Employed Candidates-----")
                print("Process Instance Key: " +str(job.process_instance_key))
                amount = db.employed_candidates(job.process_instance_key)
                if amount == 0:
                        return{"amount": False}
                else:
                        return{"amount": True}

        # #sending Weplacm the information that we currently employed x number of people to get the invoice 
        # @worker.task(task_type="sendWeplacmInfoEmployed")
        # async def send_weplacm_info_employed(job: Job, correlation_key_weplacm: int, process_correlation_key: str):
        #         print("-----Send Weplacm info about the amount of new employees-----")
        #         print("Process Instance Key: " +str(job.process_instance_key))
        #         amount = db.employed_candidates(job.process_instance_key)
        #         print(f"Amount {amount}")
        #         await cW.send_Employee_Amount(amount, correlation_key_weplacm, process_correlation_key)

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
                
                return data
    
        @worker.task(task_type="changeSwitchForFrontendCandidate")
        async def switch_currently_displayed_for_frontend(job: Job, candidate_id: int):
                print("-----Switch currently Displayed-----")
                print("Process Instance Key: " +str(job.process_instance_key))
                print(candidate_id)
        
        
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
        
        #Request more Candidates from WEPLACM 
        @worker.task(task_type="MoreRequest")
        async def request_more_candidates(job: Job, correlation_key_weplacm: int):
                process_correlation_key=f"{job.process_instance_key}23"
                await cW.more_candidates(correlation_key_weplacm, process_correlation_key)
                return {"process_correlation_key": process_correlation_key}
        
        
        #
        #
        #Interviews
        #
        
        @worker.task(task_type="checkEntrysInCandidateDB")
        async def check_candidates_amount(job: Job):
                remainingCandidates = db.check_amount_of_candidates_in_CandidateDB(job.process_instance_key)
                return {"remainingCandidatesInDB": remainingCandidates}
        
    
    
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
        async def store_date_answer(job: Job, CandidateID: int, InterviewAccepted: bool):
                print("-----Answer of Candidate recieved an stored-----")
                print("Process Instance Key: " +str(job.process_instance_key))
                print(CandidateID)
                db.store_answer(InterviewAccepted, CandidateID)
                
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
                array = db.interview_multi_instance(job.process_instance_key)
                print(array)
                

                process_correlation_key=f"{job.process_instance_key}2I16"
                print(process_correlation_key)
                return {"process_correlation_key": process_correlation_key, "InterviewOrder": db.order_by_interview(job.process_instance_key), "TopTenCandidatesIDs": array}


        #Delete candidate once we get a cancelation from this candidate
        @worker.task(task_type="cancelInterviewDateWithInterviewers")
        async def cancle_interview_date_with_interviewers(job: Job, CandidateID: int):
                print("-----Delete Candidate and generate new Order-----")
                print("Process Instance Key: " +str(job.process_instance_key))
                db.delete_TopCandidate_due_Candidate_rejection(CandidateID)
                return {"InterviewOrder": db.order_by_interview(job.process_instance_key)}

        #
        #worker
        #
        #
        #
        
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
                await cW.send_Employee_Amount(newEmployeeCount, correlation_key_weplacm, process_correlation_key)
                return {"process_correlation_key": process_correlation_key}
        
        #Check invoice
        @worker.task(task_type="checkInvoice")
        async def check_invoice(job: Job, salarie_sum: int):
                print("-----Check Invoice for correctness-----")
                print("Process Instance Key: " +str(job.process_instance_key))
                new_employee_count = db.check_Count_new_employees(job.process_instance_key)
                salary = db.check_annual_salary(job.process_instance_key)
                compensation = db.select_contract_compensation(job.process_instance_key)
                #WEPLACM gets payed for each candidate we employed 
                calculated_salary_sum = new_employee_count*salary*compensation
                print(f"Invoice:{calculated_salary_sum}")
                print(f"Invoice from WEPLACM:{salarie_sum}")
                #does the invoice add up to our callculations
                if calculated_salary_sum == salarie_sum:
                        return{"invoiceCorrect": True}
                else:
                        return{"invoiceCorrect": False}
                
        #send weplacm info about wrong invoice 
        @worker.task(task_type="sendWeplacmInfoWrongInvoice")
        async def send_weplacm_info_wrong_invoice(job: Job, correlation_key_weplacm: int):
                print("-----Sending WEPLACM Information about wrong Invoice-----")
                print("Process Instance Key: " +str(job.process_instance_key))
                await cW.sendFaultyInvoiceInfo(correlation_key_weplacm)
                print("Faulty Invoice Info send")

        #sending WEPLACM info about payment
        @worker.task(task_type="sendWeplacmInfoPayment")
        async def send_payment(job: Job, correlation_key_weplacm: int, compensation: float, salarie_sum: int, number_of_positions: int):
                print("-----Sending WEPLACM information that payment in on the way-----")
                print("Process Instance Key: " +str(job.process_instance_key))
                await cW.sendPayment(correlation_key_weplacm)
                print("Payment send")
                db.save_invoice(job.process_instance_key, compensation, salarie_sum, number_of_positions)
                
                
                
        
        loop = asyncio.get_event_loop()
        try:
                loop.run_until_complete(worker.work())
        except KeyboardInterrupt:
                pass

if __name__ == '__main__':
    main()