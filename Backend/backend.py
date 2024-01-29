from flask import Flask, jsonify, request
from flask_cors import CORS

import sqlite3

con = sqlite3.connect("../wbig.db", timeout=10,check_same_thread=False)
cur = con.cursor()


app = Flask(__name__)
CORS(app)  # Dies aktiviert CORS für alle Routen

@app.route('/api/data', methods=['GET'])
def get_data():
    print("Test")
    print(type([{'message': 'Hello from Flask!'},{'message': 'Hello from Flask!'}]))
    return jsonify([{'message': 'Hello from Flask!'},{'message': 'Hello from Flask!'}])


@app.route('/api/data/get_top_candidates', methods=['GET'])
def get_top_candidates():
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


@app.route('/api/data/get_job_standards', methods=['GET'])
def get_job_standards():
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


@app.route('/api/data/get_job_offer', methods=['GET'])
def get_job_offer():
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





# @app.route('/api/data/get_new_employees', methods=['GET'])
# def get_job_offer():
#     cur.execute(
#         """
#         SELECT * FROM newEmployees
#                 """)
#     data= cur.fetchall()

#     columns = [desc[0] for desc in cur.description]
#     result = [dict(zip(columns, row)) for row in data]
#     print(result)
#     return jsonify(result)

@app.route('/api/data/add_job_offer', methods=['POST'])
def add_job_offer():
    try:
        data = request.json  # Annahme, dass die Daten als JSON gesendet werden
        # Annahme: Die JSON-Struktur entspricht den Spalten der JobOffers-Tabelle

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

#
#@app.route('/api/data/post_job_information', methods=['POST'])
#def receive_data():
#    data = request.get_json()
#    reut

@app.route('/api/data/add_job_standards', methods=['POST'])
def add_job_standards():
    try:
        data = request.json  # Annahme, dass die Daten als JSON gesendet werden
        # Annahme: Die JSON-Struktur entspricht den Spalten der JobOffers-Tabelle

        cur.execute(
            """
            INSERT INTO JobStandards (processID, professionTitel, professionType, numberProfessions, description) 
            VALUES (?, ?, ?, ?, ?)
            """, (data['processID'], data['JobTitle'], data['JobType'], data['RequiredExperience'], data['JobDescription'], data['Responsibilities'], data['Location'], data['JobMode'], data['WeeklyHours'], data['AnnualSalary'], data['PaidTimeOff'], data['Benefits'], data['Industry'], data['GraduationLevel'], data['Language'], data['numberOfPositions'])
        )

        con.commit()

        return jsonify({'success': True, 'message': 'Job Standards added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



@app.route('/api/data/update_job_offer', methods=['POST'])
def update_job_offer():
    try:
        data = request.json  # Annahme, dass die Daten als JSON gesendet werden
        # Annahme: Die JSON-Struktur entspricht den Spalten der JobOffers-Tabelle

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
        data = request.json  # Annahme, dass die Daten als JSON gesendet werden
        # Annahme: Die JSON-Struktur entspricht den Spalten der JobOffers-Tabelle

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









if __name__ == '__main__':
    app.run(debug=True)
