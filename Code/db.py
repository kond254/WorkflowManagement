import sqlite3
import random
import numpy as np
con = sqlite3.connect("../wbig.db", timeout=10)
cur = con.cursor()


#This class is the backend for the camunda worker
class Databank:

    def __init__(self):
        # Aktiviere Fremdschlüssel-Unterstützung
        cur.execute("PRAGMA foreign_keys = ON")



    #insert contract suggestion for frontend 
    def insert_contract_in_contract_phase(self, process_id: int, compensation: float, suggestion: float):
        with con: 
            #insert into table
            cur.execute("""
                        INSERT INTO ContractPhase (processID, suggestion, compensation)
                        VALUES (?, ?, ?)
                        """, (process_id, suggestion, compensation))
            con.commit()
            print("Inserted into ContractPhase Table")
            
    def update_switch_for_candidate_in_frontend(self, candidate_id: int, switch: int):
        with con:
            cur.execute("""
                        UPDATE TopCandidate
                        SET currentlyDisplayed = ? WHERE CandidateID = ?;
                        """, (switch, candidate_id))
            con.commit()
            print("Candidate displayed in Frontend")
            
    
    #delete contract in ContractPhase table as it is not important anymore because contract was sent to weplacm or process is canceld
    def delete_contract_in_contract_phase(self, process_id: int):
        with con:
            cur.execute("""
                        DELETE FROM ContractPhase
                        WHERE processID=?
                        """, (process_id, ))
            con.commit()
            print("Deleted from ContractPhase Table") 
    
    
    # insert Contract to System Table
    def insert_contract_in_systemdb(self, process_id: int, contract_signed: str, compensation: float):
        with con:
            #execute sql statement if all important information
            cur.execute("INSERT INTO SystemDB (ProcessID, Contract, ContractSigned, Compensation) VALUES (" + str(process_id) +",\"\", "+str(contract_signed)+", "+str(compensation)+");")
            con.commit()
            print("DB INSERT EXECUTED")
            
    #insert job standards in the table
    def insert_job_standards_in_db(self, process_id: int, jobType: str, jobTitle:str, required_experience: int, job_description: str, responsibilities:str, location:str, job_mode:str, weekly_hours: int, pay: int, pto: int, benefits: str, industry:str, min_education_level:str, language:str, numberOfPositions: int):
        #finding file in the sql folder
        with open('SQL/insertIntoJobStandards.sql', 'r') as sql_file:
            sql_script = sql_file.read()           
            #generating json format
            data = {
            'job_process_instance_key': process_id,
            'jobTitle': jobTitle,
            'jobType': jobType,
            'required_experience': required_experience,
            'job_description': job_description,
            'responsibilities': responsibilities,
            'location': location,
            'job_mode': job_mode,
            'weekly_hours': weekly_hours,
            'AnnualSalary': pay,
            'pto': pto,
            'benefits': benefits,
            'industry': industry,
            'min_education_level': min_education_level,
            'language': language,
            'numberOfPosition': numberOfPositions
        }
            #create a tuple for json format that the sql file can read the data
            cur.execute(sql_script, tuple(data.values()))
            con.commit()
            print("DB INSERT EXECUTED")

    #insert candidates in databank
    def insert_candidates_in_db(self, process_id: int, first_name: str, last_name: str, gender: str, email: str, linkedin: str, adress: str, city: str, zip_code: str, country: str, age: int, previous_company: str, rating: int):
        with open('SQL/insertCandidatesIntoCandidateDB.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cur = con.cursor()
            #creating json format for candidate
            data = {
            'job_process_instance_key': process_id,
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'email': email,
            'linkedin': linkedin,
            'adress': adress,
            'city': city,
            'zip_code': zip_code,
            'country': country,
            'age': age,
            'previous_company': previous_company,
            'rating': rating
            }
            
            cur.execute(sql_script, tuple(data.values()))
            print("Candidate insertet into CandidateDB")
            sql_query = "SELECT * FROM Candidate ORDER BY rating DESC;"
            cur.execute(sql_query)
            print("Candidates Sorted descending")
            con.commit()
    
    #get top 10 candidates from candidate table and insert them into top10candidate table
    def move_top10_candidates_into_topCandidateDB(self, process_id: int):
        with open('SQL/fillTopCandidateWIthRemainingCandidates.sql', 'r') as sql_file:
            sql_content = sql_file.read()
            #only one script at a time --> split
            sql_scripts = [s.strip() for s in sql_content.split(';') if s.strip()]
            x=0
            for sql_script in sql_scripts:
                if sql_script.strip():
                    #creating temp. tables the first only needs the process id
                    if x==0:
                        cur.execute(sql_script, (process_id,))
                    else:
                        cur.execute(sql_script)
                    x+=1
            print("Candidate insertet into TopCandidate")
            con.commit()
            print("Top 10 Candidates moved")

    #remove candidate from top candidate db
    def remove_candidate_from_topCandidateDB(self, candidate_id:int):
        #deletes the candidate from candidate db because candidate table and top candidate table are linked to one another 
        with open('SQL/deleteCandidateFromTopCandidateDB.sql', 'r') as sql_file:
            sql_content = sql_file.read()
            cur.execute(sql_content, (candidate_id,))
            con.commit()
            print("Candidate removed from TopCandidateDatabase")

    #check amount of candidates in top candidate table for one unique process
    def check_amount_of_candidates_in_TopCandidateDB(self, process_id: int):
        with open('SQL/checkAmountTopCandidateDB.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cur.execute(sql_script, (process_id,))
            result = cur.fetchall()
            return result


    #check the amount of candidate in candidate table for one unique process
    def check_amount_of_candidates_in_CandidateDB(self, process_id: int):
        with open('SQL/checkAmountCandidateDB.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cur.execute(sql_script, (process_id,))
            result = cur.fetchall()
            return result[0][0]
            
    #create an array for each entry for a unique process with candidates in top candidate table 
    def create_Array_for_MultiInstance(self, process_id: int):
        with open('SQL/createArrayForMultiInstance.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cur.execute(sql_script, (process_id,))
            result = cur.fetchall()
            
            TopCandidates = []

            for row in result:
                TopCandidates.append(row[0])

            return TopCandidates
    
    #joining top candidate table with candidate table to get data for each candidate in top candidate table 
    def Join_TopCandidate_with_CandidateDB(self, CandidateID: int):
        with open('SQL/joinTopCandidateWithCandidateDB.sql', 'r') as sql_file:
            sql_content = sql_file.read()
            cur.execute(sql_content, (CandidateID,))
            data = cur.fetchall()
            print(type(data))
            con.commit()
            return data
        
    #check if time slot is avaiable for each person
    def check_interview_dates(self, target_date:str, target_start_time:str, target_end_time:str):
        with open('SQL/checkCalendryEntry.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur = con.cursor()
            cur.execute(sql_content, (target_date, target_start_time, target_end_time, target_start_time, target_end_time))
            result = cur.fetchall()
            return_var=False
            if result:
                return_var=False
            else:
                return_var=True
            return return_var        
        
    #insert timeslot for each person
    def make_entry_in_calendar(self, target_date:str, target_start_time:str, target_end_time:str, event_name_candidate_id:int):
        #first element in tuple is always the person id --> is hard coded because the id will remain the same only the person behind it changes through databank update
        data = [
            (1, 'Candidate Interview', target_date, target_start_time, target_end_time, event_name_candidate_id),
            (2, 'Candidate Interview', target_date, target_start_time, target_end_time, event_name_candidate_id),
            (5, 'Candidate Interview', target_date, target_start_time, target_end_time, event_name_candidate_id)
        ]
        print(event_name_candidate_id)
        print(type(event_name_candidate_id))
        #for each person insert the time for the interview
        for x in data:
            cur.execute(
                """
                INSERT INTO Kalender (PersonID, EventName, EventDate, EventStartTime, EventEndTime, CandidateID)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                x
            )
        print('')
        con.commit()
        print('Committed')
        #safe time time for the candidate
        cur.execute(
        """
        UPDATE TopCandidate
        SET InterviewDate = ? WHERE CandidateID = ?;
        
        """,
        (target_start_time, event_name_candidate_id)
        )
        con.commit()
        print("Date in TopCandidate inserted")
        
        
        #getting the times and the time ids for each person
        cur.execute(
        """
        SELECT EventID FROM "Kalender"
        WHERE EventDate=date(?) and EventStartTime=? and EventEndTime=?
        """,
        (target_date, target_start_time, target_end_time)
        )
        
        single_tuple = tuple(item[0] for item in cur.fetchall())
        print(f'EventIDs: {single_tuple}')
        return single_tuple
        
    #store the answer for the candidate
    def store_answer(self, InterviewAccepted: bool, CandidateID: int):
        with open('SQL/storeInterviewDateAnswer.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (InterviewAccepted, CandidateID))
            con.commit()
            print("DB Updated")
    
    #return the amount of how many candidates answered and accapted the interview date and time 
    def checking_date_answers(self, process_id: int):
        with open('SQL/checkingDateAnswers.sql') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            result = cur.fetchall()
            return result

    #delete top candidates that declined or did not answered the interview date
    def delete_TopCandidates(self, process_id: int):
        with open('SQL/deleteTopCandidatesDeclinedInterview.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            con.commit()
            print("Candidates Deleted")
            
            
    #delte entrys and enable new entrys in calendaer
    def delete_calendry_entries(self, process_id: int):
        with open('SQL/deleteEntriesInCalendry.sql', 'r') as sql_file:
            print(process_id)
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            con.commit()
            print("Candidates Deleted")
            
        #create new array for multiinstance to ask for different time
        with open('SQL/createArrayForMultiInstance.sql', 'r') as sql_file:
            sql_script = sql_file.read()

            cur.execute(sql_script, (process_id,))
            result = cur.fetchall()
            
            TopCandidates = []

            for row in result:
                TopCandidates.append(row[0])

            return TopCandidates
            
    #return the candidates orderd by their interview dates 
    def order_by_interview(self, process_id: int):
        with open('SQL/orderByInterview.sql')as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            result = cur.fetchall()
            con.commit()
            print("Candidates Ordered")
            return result

    #delete candidate from candidate table
    def delete_TopCandidate_due_Candidate_rejection(self, CandidateID: int):
         with open('SQL/deleteTopCandidateDueRejection.sql')as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (CandidateID, ))
            con.commit()
            print("Candidate Deleted")

    #store candidates answer if he accapted/declined the job
    def store_job_answer(self, JobAccepted: int, CandidateID: int):
        with open('SQL/storeFinalJobAnswer.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (JobAccepted, CandidateID, ))
            con.commit()
            print("DB Updated")

    #delete all candidates that declined the job 
    def delete_TopCandidates_final(self, process_id: int):
        with open('SQL/deleteTopCandidatesDeclinedJob.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            con.commit()
            print("Candidates Deleted")

    #move candidates that accapted the job to the top employment table 
    def select_new_employees(self, process_id: int):
        with open('SQL/selectTopCandidates.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            con.commit()
            candidateIDs = cur.fetchall()
            return candidateIDs
    
    
    #saving all candidates which are remaining in the topcandidatedb (candidates is a list with the processid and first & last name of candidate)
    def join_new_employee_data(self, candidates: list):
        with open('SQL/insertNewEmployees.sql', 'r') as sql_file:
            if(candidates):
                for x in candidates:
                    cur.execute(
                        """
                        INSERT INTO Employees (ProcessID, Name, Surname)
                        VALUES (?, ?, ?)
                        """,
                        x
                    )
                con.commit()
                print("New Employees saved")
                print(candidates[0][0])
                
                
                #delete new employees from candidate db
                
                
                cur.execute(
                    """DELETE FROM Candidate
                    WHERE CandidateID IN (
                    SELECT Candidate.CandidateID
                    FROM Candidate
                    JOIN TopCandidate ON Candidate.CandidateID=TopCandidate.CandidateID
                    WHERE Candidate.ProcessID=?)""",
                    (candidates[0][0],)
                )
                con.commit()
                
                print("Candidates deleted from Candidates/TopCandidate Table")
            else:
                print("Candidate List is Empty")

    #check how many new employees are currently in this process
    def rejected_candidates(self, process_id: int):
        with open('SQL/selectCandidatesToReject.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            result = cur.fetchall()
            return result[0][0]    #return only the CandidateID

    #check how many new employees are currently in this process
    def check_Count_new_employees(self, process_id: int):
        with open('SQL/checkAmountnewEmplyoees.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            result = cur.fetchall()
            return result[0][0]    #return only the number
    
    #check how many should be employed
    def check_number_of_positions(self, process_id: int):
        with open('SQL/selectNumberOfPositions.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            result = cur.fetchall()
            return result[0][0] #return only the number
    
    #select the salary of new employes
    def check_annual_salary(self, process_id: int):
        with open('SQL/checkAnnualSalary.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            result = cur.fetchall()
            return result[0][0]
        
    #select the compensation
    def select_contract_compensation(self, process_id: int):
        with open('SQL/selectCompensation.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            result = cur.fetchall()
            return result[0][0]
        
    #Test for Interview multi instance
    def interview_multi_instance(self, process_id: int):
        with open('SQL/prepareMultiInstanceforInterview.sql', 'r') as sql_file:
            sql_script = sql_file.read()

            cur.execute(sql_script, (process_id,))
            result = cur.fetchall()
            print(result)
            TopCandidates = []

            for row in result:
                TopCandidates.append(row[0])
                print(row[0])
            print(TopCandidates)
            return TopCandidates
    
    
    def employed_candidates(self, process_id: int):
        with open('SQL/checkCandidatesEmployed.sql', 'r') as sql_file:
            sql_content=sql_file.read()
            cur.execute(sql_content, (process_id, ))
            result = cur.fetchall()
            return result[0][0] 