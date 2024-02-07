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

##This method starts the camunda process
async def startProcess(data):
    channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
    client = ZeebeClient(channel)
    try:
        response = await client.run_process(
            bpmn_process_id="WBIG",  # Process ID from WEPLACM
            variables=data
        )
        print(response)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")


##This method sent the jobOffer which comes from frontend data.service.ts to the camunda task
async def reviewJobOpening(data, decision:bool):
        channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
        client = ZeebeClient(channel)
        try:
            await client.publish_message(name="reviewJobOpening", # Process ID from WEPLACM
                                    correlation_key=str(data["processID"]), #Correlation Key from WEPLACM
                                    variables={
                                            "decision": decision
                                }
                            )
        except Exception as e:
            print(f"An error occurred: {e}")


##This method sent the contract suggestion which comes from frontend data.service.ts to the camunda task
async def analyzeContractSuggestion(data, compensation:float):
        channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
        client = ZeebeClient(channel)
        try:
            await client.publish_message(name="analyzeContract", # Process ID from WEPLACM
                                    correlation_key=str(data["processID"]), #Correlation Key from WEPLACM
                                    variables={
                                            "compensation": float(compensation)
                                }
                            )
        except Exception as e:
            print(f"An error occurred: {e}")


##This method sent the created job standards by hr manager which comes from frontend data.service.ts to the camunda task
async def createJobStandards(data):
        channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
        client = ZeebeClient(channel)
        try:
            await client.publish_message(name="createJobStandards", # Process ID from WEPLACM
                                    correlation_key=str(data["ProcessID"]), #Correlation Key from WEPLACM
                                    variables={
                                            "JobName":data["JobTitle"], 
                                            "jobType":data["JobType"], 
                                            "number_of_positions":data["numberOfPositions"], 
                                            "required_experience":data["RequiredExperience"], 
                                            "job_description":data["JobDescription"], 
                                            "responsibilities":data["Responsibilities"], 
                                            "location":data["Location"],
                                            "job_mode":data["JobMode"],
                                            "weekly_hours":data["WeeklyHours"],
                                            "pay":data["AnnualSalary"],
                                            "pto":data["PaidTimeOff"],
                                            "benefits":data["Benefits"],
                                            "industry":data["Industry"], 
                                            "min_education_level":data["GraduationLevel"], 
                                            "language":data["Language"]           
                                }
                            )
        except Exception as e:
            print(f"An error occurred: {e}")



#Neue Funktion 03.02, hier fehlt noch die invoice?
async def checkStatusInvoice(data):
        channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
        client = ZeebeClient(channel)
        try:
            await client.publish_message(name="checkStatusInvoice", # Process ID from WEPLACM
                                    correlation_key=str(data["processID"]), #Correlation Key from WEPLACM
                                    variables={
                                            
                                }
                            )
        except Exception as e:
            print(f"An error occurred: {e}")


##This method sent the top candidates which comes from frontend data.service.ts to the camunda task
async def setRatingForCandidate(data, ratingHrManager: int, ratingHrRepresentive: int, ratingVP: int):
        channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
        client = ZeebeClient(channel)
        print(ratingHrManager)
        print("TEst")
        print(ratingHrRepresentive)
        try:
            await client.publish_message(name="rateCandidate", # Process ID from WEPLACM
                                    correlation_key=str(data["ProcessID"]), #Correlation Key from WEPLACM
                                    variables={
                                            "ratingHrManager": ratingHrManager,
                                            "ratingHrRepresentive": ratingHrRepresentive,
                                            "ratingVP": ratingVP
                                }
                            )
        except Exception as e:
            print(f"An error occurred: {e}")

async def checkCandidates(data, decision:bool):
        channel = create_insecure_channel(hostname="141.26.157.71", port=26500)
        client = ZeebeClient(channel)
        try:
            await client.publish_message(name="checkCandidates", # Process ID from WEPLACM
                                    correlation_key=str(data["ProcessID"]), #Correlation Key from WEPLACM
                                    variables={
                                            "final_selection_passed": decision
                                }
                            )
        except Exception as e:
            print(f"An error occurred: {e}")


#
#
#API ROUTES
#
#
#
#

con = sqlite3.connect("../wbig.db", timeout=10,check_same_thread=False)
cur = con.cursor()
lock =threading.Lock()

app = Flask(__name__)
CORS(app) 
socketio = SocketIO(app, cors_allowed_origins="*")


##This method stored the contract suggestion from backend in the sql contract phase table
@app.route('/api/data/get_current_contracts_suggestions', methods=['GET'])
def get_current_contracts_suggestions():
    try:
        lock.acquire(True)
        cur.execute(
            """
            SELECT *
            FROM ContractPhase
            JOIN JobOffers ON JobOffers.processID = ContractPhase.processID
            """)
        data= cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()


##This method receive the contract suggestion from backend and return the contract to the frontend data.service.ts and display in the hr department page
@app.route('/api/data/post_current_contracts_suggestions', methods=['POST'])
def post_current_contracts_suggestions():
    try: 
        data = request.json
        asyncio.run(analyzeContractSuggestion(data, data["compensation"]))
        return jsonify({'success': True, 'message': 'Job Offer added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    

##This flask wait for a get request from frontend data.service.ts and returns the variables from the topcandidate to the frontend data.service.ts
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


##This flask wait for a get request from frontend data.service.ts and returns the variables from the jobStandards to the frontend data.service.ts
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


##This flask wait for a get request from frontend data.service.ts and returns the variables from the jobOffer where hrmanager status is accepted to the frontend data.service.ts
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


##This flask wait for a get request from frontend data.service.ts and returns the variables from the accepted jobOffers to the frontend data.service.ts
@app.route('/api/data/get_job_offer_accepted', methods=['GET'])
def get_job_offer_accepted():
    try:
        lock.acquire(True)
            
        cur.execute(
            """
            SELECT * FROM JobOffers
            JOIN SystemDB on SystemDB.ProcessID=JobOffers.processID
            where hrmanagerAccepted = 1 and jobStandardSent = 0
                    """)
        data= cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()


##This flask wait for a get request from frontend data.service.ts and returns the variables from the accepted topCandidates to the frontend data.service.ts
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


##This flask wait for a get request from frontend data.service.ts and returns the variables from the newEmployees sql table to the frontend data.service.ts
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

##This flask wait for a get request from frontend data.service.ts and returns the variables from the invoices sql table to the frontend data.service.ts
@app.route('/api/data/get_invoices', methods=['GET'])
def get_invoices():
    try:
        lock.acquire(True)
            
        cur.execute(
            """
            SELECT * FROM Invoice
                    """)
        data= cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()

##This flask wait for a post request from frontend data.service.ts and add for the variable in the JobOffers sql table, wich are sent by the frondent
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
    

##This flask wait for a post request from frontend data.service.ts and add for the variable in the JobStandard sql table, wich are sent by the frondent
@app.route('/api/data/add_job_standards', methods=['POST'])
def add_job_standards():
    try:
        lock.acquire(True)
        data = request.json
        print(data)
        asyncio.run(createJobStandards(data))
        
       
        cur.execute(
            """
            Update JobOffers
             set jobStandardSent = 1
             where processID = ?
            """, (data['ProcessID'],)
        )

        con.commit()
        socketio.emit('job_standards_updated', {'message': 'Job Standards added successfully'})

        return jsonify({'success': True, 'message': 'Job Standards added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally: 
        lock.release()



##This flask wait for a post request from frontend data.service.ts and add for the variable hrmanagerAccepted = 1 in the jobOffers sql table
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
    


###########################
    
##This flask wait for a post request from frontend data.service.ts and set the variable jobStandardSent = 1 in the JobOffer sql table
@app.route('/api/data/update_job_offer_after_send', methods=['POST'])
def update_job_offer_after_send():
    #decision
    try:
        data = request.json
        data['decision']=True
        print(data["processID"])
        asyncio.run(reviewJobOpening(data, True))
        cur.execute(
            """
            Update JobOffers
             set jobStandardSent = 1
             where processID = ?
            """, (data['processID'],)
        )

        con.commit()
        socketio.emit('job_offer_updated_after_send', {'message': 'Job Offer updated successfully'})

        print(data['processID'])
        return jsonify({'success': True, 'message': 'Job Offer added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

############################


##This flask wait for a post request from frontend data.service.ts and delete the jobOffer in the JobOffer sql table  
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

##This flask wait for a post request from frontend data.service.ts and add for the variable for interview calculation
@app.route('/api/data/set_interview_results_for_candidate', methods=['POST'])
def set_interview_results_for_candidate():
    try:
        # lock.acquire(True)
        data = request.json
        # cur.execute(
        #     """
        #     Update TopCandidate
        #      set hrmanagerAccepted = 1
        #      where CandidateID = ?
        #     """, (data['CandidateID'],)
        # )
        asyncio.run(setRatingForCandidate(data, int(data['ratingHrManager']), int(data['ratingHrRepresentative']),int(data['ratingVP'])))
        # con.commit()
        socketio.emit('top_candidates_updated', {'message': 'Top Candidates updated successfully'})
        print(data['CandidateID'])
        return jsonify({'success': True, 'message': 'Top Candidates added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    

##This flask wait for a post request from frontend data.service.ts and add for the variable hrmanagerAccepted the number 1 in the topCandidate sql table
@app.route('/api/data/update_top_candidates', methods=['POST'])
def update_top_candidates():
    try:
        # lock.acquire(True)
        data = request.json
        # cur.execute(
        #     """
        #     Update TopCandidate
        #      set hrmanagerAccepted = 1
        #      where CandidateID = ?
        #     """, (data['CandidateID'],)
        # )
        asyncio.run(checkCandidates(data, True))
        # con.commit()
        socketio.emit('top_candidates_updated', {'message': 'Top Candidates updated successfully'})
        print(data['CandidateID'])
        return jsonify({'success': True, 'message': 'Top Candidates added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    


##This flask wait for a post request from frontend data.service.ts and delete the candidate in the candidate sql table  
@app.route('/api/data/delete_top_candidate', methods=['POST'])
def delete_top_candidates():
    try:
        # lock.acquire(True)
        data = request.json
        # print(data['CandidateID'])
        # cur.execute(
        #     """
        #    DELETE FROM Candidate
        #    WHERE CandidateID = ?
        #     """, (data['CandidateID'],)  
        # )
        # cur.execute(
        #     """
        #    DELETE FROM TopCandidate
        #    WHERE CandidateID = ?
        #     """, (data['CandidateID'],)  
        # )
        # con.commit()
        # #socketio.emit('top_candidates_updated', {'message': 'Top Candidates updated successfully'})
        # print(data['processID'])
        
        asyncio.run(checkCandidates(data, False))
        

        return jsonify({'success': True, 'message': 'Top candidate delete successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



##This flask wait for a get request from frontend and returns the variables from the sql command execution for the frontend data.service.ts 
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


##This flask wait for a post request from frontend and the server add the current logged-in user
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


##This flask wait for a get request from frontend and returns the list of logged-in users for the frontend data.service.ts 
@app.route('/api/data/get_login_users', methods=['GET'])
def get_login_users():
    try:
        return jsonify(login_users)
    except Exception as e:
        return jsonify({'error': str(e)})


##This flask wait for a post request from frontend data.service.ts and the server delete the current logged-in user
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
    
    
##This flask wait for a get request from frontend and returns the variables from the sql command execution for the frontend data.service.ts 
@app.route('/api/data/get_jobstandards_with_top_candidates_only_one', methods=['GET'])
def get_jobstandards_with_top_candidates_only_one():
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
            WHERE TopCandidate.hrmanagerAccepted = 0 AND Candidate.ProcessID = ?   AND TopCandidate.currentlyDisplayed=1              
            """, (int(data),)  )
    
        data = cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()
        
        
@app.route('/api/data/get_jobstandards_with_top_candidates_only_one_for_interview', methods=['GET'])
def get_jobstandards_with_top_candidates_only_one_for_interview():
    print("TEST____")
    try:
        lock.acquire(True)
        data = request.args.get('ProcessID')
        print("TEST____")
        print(data)
        
        cur.execute(
            """
            SELECT JobStandards.*, Candidate.*
            FROM JobStandards
            LEFT JOIN Candidate ON JobStandards.ProcessID = Candidate.ProcessID
            JOIN TopCandidate ON TopCandidate.CandidateID = Candidate.CandidateID
            JOIN Kalender ON Kalender.CandidateID=TopCandidate.CandidateID
            WHERE TopCandidate.hrmanagerAccepted = 0 AND Candidate.ProcessID = ?   AND TopCandidate.currentlyDisplayed=1      
            LIMIT 1        
            """, (int(data),)  )
    
        data = cur.fetchall()

        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in data]
        print(result)
        return jsonify(result)
    finally:
        lock.release()
      
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