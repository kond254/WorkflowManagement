import sqlite3
con = sqlite3.connect("wbig.db")


class Databank:

    #with open('SQL/createTableSystem.sql', 'r') as sql_file:
    #    sql_script = sql_file.read()

    #    cur = con.cursor()

    #    cur.execute(sql_script)
    #
   
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

    def insert_candidates_in_db(self, process_id: int, first_name: str, last_name: str, gender: str, email: str, adress: str, city: str, zip_code: str, country: str, age: int, previous_company: str, rating: int):
        with open('SQL/insertCandidateIntoCandidateDB.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            cur = con.cursor()
            
            data = {
            'job_process_instance_key': process_id,
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'email': email,
            'adress': adress,
            'zip_code': zip_code,
            'country': country,
            'age': age,
            'previous_company': previous_company,
            'rating': rating
            
    }
            cur.execute(sql_script, tuple(data.values()))
            print("Candidate insertet into CandidateDB")
            sql_query = "SELECT * FROM CandidateDB ORDER BY rating DESC;"
            cur.execute(sql_query)
            print("Candidates Sorted descending")
            con.commit()
    
    def move_top10_candidates_into_topCandidateDB(self):
        with con:
            cur = con.cursor()

            sql_query = "INSERT INTO TopCandidateDB SELECT * FROM CandidateDB LIMIT 10;"
            cur.execute(sql_query)
            sql_query = "DELETE FROM CandidateDB WHERE process_id = process_id LIMIT 10;"
            cur.execute(sql_query)
            con.commit()
            print("Top 10 Candidates moved")


    def remove_candidate_from_topCandidateDB(self, first_name: str, last_name: str):
        with con:
            cur = con.cursor()

            sql_query = "DELETE FROM TopCandidateDB WHERE first_name = 'first_name' AND last_name = 'last_name';"
            cur.execute(sql_query)
            con.commit()
            print("Candidate removed from TopCandidateDatabase")


    def check_amount_of_candidates(self):
        with con:
            cur = con.cursor()

            sql_query = "SELECT COUNT(*) FROM TopCandidateDB"
            cur.execute(sql_query)
            con.commit()
            print(cur.execute(sql_query))