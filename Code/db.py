import sqlite3
import random
import numpy as np
con = sqlite3.connect("wbig.db")


class Databank:
    
    def __init__(self):
        cur = con.cursor()
        # Aktiviere Fremdschlüssel-Unterstützung
        cur.execute("PRAGMA foreign_keys = ON")

  
    def insert_contract_in_systemdb(self, process_id: int, contract_signed: str, compensation: float):
        with con:
            cur = con.cursor()
      
            cur.execute("INSERT INTO SystemDB (ProcessID, Contract, ContractSigned, Compensation) VALUES (" + str(process_id) +",\"\", "+str(contract_signed)+", "+str(compensation)+");")
            con.commit()
            print("DB INSERT EXECUTED")
            
            
    def insert_job_standards_in_db(self, process_id: int, jobType: str, jobTitle:str, required_experience: int, job_description: str, responsibilities:str, location:str, job_mode:str, weekly_hours: int, pay: int, pto: int, benefits: str, industry:str, min_education_level:str, language:str):
        with open('SQL/insertIntoJobStandards.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cur = con.cursor()
            
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
            'language': language
    }

            cur.execute(sql_script, tuple(data.values()))
            con.commit()
            print("DB INSERT EXECUTED")

    def insert_candidates_in_db(self, process_id: int, first_name: str, last_name: str, gender: str, email: str, linkedin: str, adress: str, city: str, zip_code: str, country: str, age: int, previous_company: str, rating: int):
        with open('SQL/insertCandidatesIntoCandidateDB.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cur = con.cursor()
            
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
    
    def move_top10_candidates_into_topCandidateDB(self, process_id: int):
        with open('SQL/fillTopCandidateWIthRemainingCandidates.sql', 'r') as sql_file:
            sql_content = sql_file.read()
            #only one script at a time --> split
            sql_scripts = [s.strip() for s in sql_content.split(';') if s.strip()]
            cur = con.cursor()
            x=0
            for sql_script in sql_scripts:
                if sql_script.strip():
                    if x==0:
                        cur.execute(sql_script, (process_id,))
                    else:
                        cur.execute(sql_script)
                    x+=1
            print("Candidate insertet into TopCandidate")
            con.commit()
            print("Top 10 Candidates moved")


    def remove_candidate_from_topCandidateDB(self, candidate_id:int):
        with open('SQL/deleteCandidateFromTopCandidateDB.sql', 'r') as sql_file:
            sql_content = sql_file.read()
            cur = con.cursor()

            cur.execute(sql_content, (candidate_id,))
            con.commit()
            print("Candidate removed from TopCandidateDatabase")


    def check_amount_of_candidates_in_TopCandidateDB(self, process_id: int):
        with open('SQL/checkAmountTopCandidateDB.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cur = con.cursor()

            cur.execute(sql_script, (process_id,))
            result = cur.fetchall()
            
            return result

    def check_amount_of_candidates_in_CandidateDB(self, process_id: int):
        with open('SQL/checkAmountCandidateDB.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cur = con.cursor()

            cur.execute(sql_script, (process_id,))
            result = cur.fetchall()
            return result
            

    def create_Array_for_MultiInstance(self, process_id: int):
        with open('SQL/createArrayForMultiInstance.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cur = con.cursor()

            cur.execute(sql_script, (process_id,))
            result = cur.fetchall()
            
            TopCandidates = []

            for row in result:
                TopCandidates.append(row[0])

            return TopCandidates
        
    def Join_TopCandidate_with_CandidateDB(self, CandidateID: int):
        with open('SQL/joinTopCandidateWithCandidateDB.sql', 'r') as sql_file:
            sql_content = sql_file.read()
            cur = con.cursor()

            cur.execute(sql_content, (CandidateID,))
            data = cur.fetchall()
            print(type(data))
            con.commit()
            return data

            