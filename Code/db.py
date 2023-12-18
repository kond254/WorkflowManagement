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