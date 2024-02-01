import threading
from flask import Flask, jsonify, request
from flask_cors import CORS

import sqlite3

con = sqlite3.connect("../wbig.db", timeout=10,check_same_thread=False)
cur = con.cursor()
lock =threading.Lock()

app = Flask(__name__)
CORS(app)  # Dies aktiviert CORS für alle Routen


@app.route('/api/data/get_top_candidates', methods=['GET'])
def get_top_candidates():
    try:
        lock.acquire(True)
        cur.execute(
            """
            SELECT Candidate.*, TopCandidate.*
            FROM Candidate
            JOIN TopCandidate ON Candidate.CandidateID = TopCandidate.CandidateID
            LIMIT 4
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
            LIMIT 3
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



# Das könnte ja für Johannes HR DEPARTMENT relevant sein?
# @app.route('/api/data/get_top_candidates_accepted', methods=['GET'])
# def get_top_candidates_accepted():
#     try:
#         lock.acquire(True)
            
#         cur.execute(
#             """
#             SELECT * FROM TopCandidate
#             where hrmanagerAccepted = 1
#                     """)
#         data= cur.fetchall()

#         columns = [desc[0] for desc in cur.description]
#         result = [dict(zip(columns, row)) for row in data]
#         print(result)
#         return jsonify(result)
#     finally:
#         lock.release()



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

        cur.execute(
            """
            INSERT INTO JobOffers (processID, professionTitel, professionType, numberProfessions, description, hrmanagerAccepted) 
            VALUES (?, ?, ?, ?, ?, ?)
            """, (data['processID'], data['professionTitel'], data['professionType'], data['numberProfessions'], data['description'], 0)
        )

        con.commit()

        return jsonify({'success': True, 'message': 'Job Offer added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    

@app.route('/api/data/add_job_standards', methods=['POST'])
def add_job_standards():
    try:
        data = request.json
        print(data)
        cur.execute(
            """
            INSERT INTO JobStandards (ProcessID, JobTitle, JobType) 
            VALUES (?, ?, ?)
            """, (data['processID'], data['professionType'], data['professionTitel'])
        )

        con.commit()
        return jsonify({'success': True, 'message': 'Job Standards added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



@app.route('/api/data/update_job_offer', methods=['POST'])
def update_job_offer():
    try:
        data = request.json
        cur.execute(
            """
            Update JobOffers
             set hrmanagerAccepted = 1
             where processID = ?
            """, (data['processID'],)
        )

        con.commit()
        print(data['processID'])
        return jsonify({'success': True, 'message': 'Job Offer added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    

@app.route('/api/data/delete_job_offer', methods=['POST'])
def delete_job_offer():

    print("test")
    try:
        lock.acquire(True)
        data = request.json
        cur.execute(
            """
            Delete from JobOffers
            where processID = ?
            """, (data['processID'],)
        )

        con.commit()
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
        data = request.json
        cur.execute(
            """
            Update TopCandidates
             set hrmanagerAccepted = 1
             where processID = ?
            """, (data['processID'],)
        )

        con.commit()
        print(data['processID'])
        return jsonify({'success': True, 'message': 'Top Candidates added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    

@app.route('/api/data/delete_top_candidates', methods=['POST'])
def delete_top_candidates():

    print("test")
    try:
        lock.acquire(True)
        data = request.json
        cur.execute(
            """
            Delete from TopCandidates
            where processID = ?
            """, (data['processID'],)
        )

        con.commit()
        print(data['processID'])

        return jsonify({'success': True, 'message': 'Top candidate delete successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        lock.release()


# NEU: Soll Jobstandarts und die passenden topcandidaten ausgeben.

# @app.route('/api/data/get_jobstandards_with_top_candidates', methods=['GET'])
# def get_jobstandards_with_top_candidates():
#     try:
#         lock.acquire(True)
#         cur.execute(
#             """
#             SELECT JobStandards.*, TopCandidate.*
#             FROM JobStandards
#             LEFT JOIN TopCandidate ON JobStandards.processID = TopCandidate.processID
#             LIMIT 3
#             """)
#         data = cur.fetchall()

#         columns = [desc[0] for desc in cur.description]
#         result = [dict(zip(columns, row)) for row in data]
#         print(result)
#         return jsonify(result)
#     finally:
#         lock.release()



if __name__ == '__main__':
    app.run(debug=True)