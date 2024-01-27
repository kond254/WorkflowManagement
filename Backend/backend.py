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


@app.route('/api/data/get_job_information', methods=['GET'])
def get_job_information():
    cur.execute(
        """
        SELECT * FROM Candidate
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
                """)
    data= cur.fetchall()

    columns = [desc[0] for desc in cur.description]
    result = [dict(zip(columns, row)) for row in data]
    print(result)
    return jsonify(result)

#
#@app.route('/api/data/post_job_information', methods=['POST'])
#def receive_data():
#    data = request.get_json()
#    reut




if __name__ == '__main__':
    app.run(debug=True)
