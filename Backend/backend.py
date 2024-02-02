import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import asyncio
import sqlite3
from pyzeebe import ZeebeClient, create_insecure_channel



#Functions to call BPMN
#
#
#
#

login_users = []

async def startProcess(data):
    channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
    client = ZeebeClient(channel)
    try:
        response = await client.run_process(
            bpmn_process_id="WBIG_Process",  # Process ID from WEPLACM
            variables=data
        )
        print(response)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")


async def reviewJobOpening(data, decision:bool):
        channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
        client = ZeebeClient(channel)
        print(f"TEST: {data["processID"]}")
        try:
            await client.publish_message(name="reviewJobOpening", # Process ID from WEPLACM
                                    correlation_key=str(data["processID"]), #Correlation Key from WEPLACM
                                    variables={
                                            "decision": decision
                                }
                            )
        except Exception as e:
            print(f"An error occurred: {e}")

con = sqlite3.connect("../wbig.db", timeout=10,check_same_thread=False)
cur = con.cursor()
lock =threading.Lock()

app = Flask(__name__)
CORS(app) 
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/api/data/get_top_candidates', methods=['GET'])
def get_top_candidates():
    try:
        lock.acquire(True)
        cur.execute(
            """
            SELECT Candidate.*, TopCandidate.*
            FROM Candidate
            JOIN TopCandidate ON Candidate.CandidateID = TopCandidate.CandidateID
            """)
        data= cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()


@app.route('/api/data/get_job_standards', methods=['GET'])
def get_job_standards():
    try:
        lock.acquire(True)
        cur.execute(
            """
            SELECT * FROM JobStandards
          
            """)
        data= cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()
        

@app.route('/api/data/get_job_offer', methods=['GET'])
def get_job_offer():
    try:
        lock.acquire(True)
        cur.execute(
            """
            SELECT * FROM JobOffers
            where hrmanagerAccepted = 0
                    """)
        data= cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()

@app.route('/api/data/get_job_offer_accepted', methods=['GET'])
def get_job_offer_accepted():
    try:
        lock.acquire(True)
            
        cur.execute(
            """
            SELECT * FROM JobOffers
            where hrmanagerAccepted = 1
                    """)
        data= cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()




@app.route('/api/data/get_top_candidates_accepted', methods=['GET'])
def get_top_candidates_accepted():
    try:
        lock.acquire(True)
            
        cur.execute(       
          """
            SELECT Candidate.*, TopCandidate.*
            FROM Candidate
            JOIN TopCandidate ON Candidate.CandidateID = TopCandidate.CandidateID
            WHERE hrmanagerAccepted = 1
            """)
        data= cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()



@app.route('/api/data/get_new_employees', methods=['GET'])
def get_new_employees():
    try:
        lock.acquire(True)
            
        cur.execute(
            """
            SELECT * FROM newEmployees
                    """)
        data= cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()

@app.route('/api/data/add_job_offer', methods=['POST'])
def add_job_offer():
    try:
        
        data = request.json
        print(data)
        dataChanges={
            "jobTitle":data["professionTitel"],
            "jobType":data["professionType"],
            "number_of_positions": data["numberProfessions"]
        }
        processID=asyncio.run(startProcess(dataChanges))
        
        cur.execute(
            """
            INSERT INTO JobOffers (processID, professionTitel, professionType, numberProfessions, description, hrmanagerAccepted) 
            VALUES (?, ?, ?, ?, ?, ?)
            """, (processID, data['professionTitel'], data['professionType'], data['numberProfessions'], data['description'], 0)
        )

        con.commit()
        socketio.emit('job_offer_updated', {'message': 'Job Offer added or updated successfully'})
        
        #starting process in camunda:
        
        
        return jsonify({'success': True, 'message': 'Job Offer added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    

@app.route('/api/data/add_job_standards', methods=['POST'])
def add_job_standards():
    try:
        lock.acquire(True)
        data = request.json
        
        print(data)
        cur.execute(
            """
            INSERT INTO JobStandards (ProcessID, JobType, JobTitle, numberOfPositions, RequiredExperience, JobDescription, Responsibilities, Location, JobMode, WeeklyHours, AnnualSalary, PaidTimeOff, Benefits, Industry, GraduationLevel, Language)   
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (data['ProcessID'], data['JobType'], data['JobTitle'], data['numberOfPositions'], data['RequiredExperience'], data['JobDescription'], data ['Responsibilities'], data ['Location'], data ['JobMode'], data['WeeklyHours'], data ['AnnualSalary'], data ['PaidTimeOff'], data ['Benefits'], data ['Industry'], data ['GraduationLevel'], data ['Language'])   # oben wie es in der Datenbank steht und hier wie es im Interfacer steht
           
                
 
        )

        con.commit()
        socketio.emit('job_standards_updated', {'message': 'Job Standards added successfully'})

        return jsonify({'success': True, 'message': 'Job Standards added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally: 
        lock.release()



@app.route('/api/data/update_job_offer', methods=['POST'])
def update_job_offer():
    #decision
    try:
        data = request.json
        data['decision']=True
        print(data["processID"])
        asyncio.run(reviewJobOpening(data, True))
        cur.execute(
            """
            Update JobOffers
             set hrmanagerAccepted = 1
             where processID = ?
            """, (data['processID'],)
        )

        con.commit()
        socketio.emit('job_offer__accepted_updated', {'message': 'Job Offer updated successfully'})

        print(data['processID'])
        return jsonify({'success': True, 'message': 'Job Offer added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    

@app.route('/api/data/delete_job_offer', methods=['POST'])
def delete_job_offer():
    try:
        lock.acquire(True)
        data = request.json
        asyncio.run(reviewJobOpening(data, False))
        cur.execute(
            """
            Delete from JobOffers
            where processID = ?
            """, (data['processID'],)
        )

        con.commit()
        socketio.emit('job_offer_updated', {'message': 'Job Offer added or updated successfully'})
        print(data['processID'])

        return jsonify({'success': True, 'message': 'Job Offer delete successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        lock.release()


# //////////////////////////////////////////////// 01.02 ///////////////////////////////////////////////////////////////////////////////

@app.route('/api/data/update_top_candidates', methods=['POST'])
def update_top_candidates():
    try:
        lock.acquire(True)
        data = request.json
        cur.execute(
            """
            Update TopCandidate
             set hrmanagerAccepted = 1
             where CandidateID = ?
            """, (data['CandidateID'],)
        )

        con.commit()
        socketio.emit('top_candidates_updated', {'message': 'Top Candidates updated successfully'})
        print(data['CandidateID'])
        return jsonify({'success': True, 'message': 'Top Candidates added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        lock.release()
    
# Noch ändern!!!
@app.route('/api/data/delete_top_candidate', methods=['POST'])
def delete_top_candidates():
    try:
        lock.acquire(True)
        data = request.json
        print(data['CandidateID'])
        cur.execute(
            """
           DELETE FROM Candidate
           WHERE CandidateID = ?
            """, (data['CandidateID'],)  
        )
        cur.execute(
            """
           DELETE FROM TopCandidate
           WHERE CandidateID = ?
            """, (data['CandidateID'],)  
        )
        con.commit()
        #socketio.emit('top_candidates_updated', {'message': 'Top Candidates updated successfully'})
        print(data['processID'])

        return jsonify({'success': True, 'message': 'Top candidate delete successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        lock.release()


# NEU: Soll Jobstandarts und die passenden topcandidaten ausgeben.
@app.route('/api/data/get_jobstandards_with_top_candidates', methods=['GET'])
def get_jobstandards_with_top_candidates():
    try:
        lock.acquire(True)
        data = request.args.get('ProcessID')
        print(data)
        
        cur.execute(
            """
            SELECT JobStandards.*, Candidate.*
            FROM JobStandards
            LEFT JOIN Candidate ON JobStandards.ProcessID = Candidate.ProcessID
            JOIN TopCandidate ON TopCandidate.CandidateID = Candidate.CandidateID
            WHERE TopCandidate.hrmanagerAccepted = 0 AND Candidate.ProcessID = ?                
            """, (data,)  )
    
        data = cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()

@app.route('/api/data/add_login_user', methods=['POST'])
def add_login_user():
    try:
        data = request.json
        
        # Prüfe, ob der Benutzer bereits in der temporären Liste ist
        existing_user = next((user for user in login_users if user['username'] == data['username']), None)

        if existing_user:
            existing_user['isLoggedIn'] = data['isLoggedIn']
        else:
            login_users.append(data)

        socketio.emit('temp_login_users_updated', {'message': 'Temporary Login User added or updated successfully'})

        return jsonify({'success': True, 'message': 'Temporary Login User added or updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/data/get_login_users', methods=['GET'])
def get_login_users():
    try:
        return jsonify(login_users)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/data/delete_login_user', methods=['POST'])
def delete_login_user():
    try:
        data = request.json
        username_to_delete = data.get('username')

        # Entferne den Benutzer aus der Liste der eingeloggten Benutzer
        login_users[:] = [user for user in login_users if user.get('username') != username_to_delete]

        socketio.emit('temp_login_users_updated', {'message': 'Temporary Login User deleted successfully'})

        return jsonify({'success': True, 'message': f'Temporary Login User {username_to_delete} deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
      
# cur.execute("""
#     SELECT COUNT(*) as count FROM (
#         SELECT * FROM (
#             SELECT JobStandards.*, Candidate.*, TopCandidate.*
#             FROM JobStandards
#             LEFT JOIN Candidate ON JobStandards.ProcessID = Candidate.ProcessID
#             LEFT JOIN TopCandidate ON TopCandidate.CandidateID = Candidate.CandidateID
#             WHERE JobStandards.ProcessID = ? AND TopCandidate.hrmanagerAccepted = 0
#         ) LIMIT ?
#     )
# """, (process_id, limit_value))




if __name__ == '__main__':
    app.run(debug=True)