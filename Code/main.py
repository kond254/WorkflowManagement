import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('wbig.db')
cursor = conn.cursor()

# Specify the target date, start time, and end time you want to check
target_date = '2024-01-10'
target_start_time = '08:00:00'
target_end_time = '14:00:00'

# Use a parameterized query to check if the date and time range is taken
query = '''
    SELECT *
    FROM Kalender
    WHERE EventDate = ? 
    AND(
        (? BETWEEN time(EventStartTime, '+1 minute') AND time(EventEndTime, '-1 minute'))
        OR (? BETWEEN time(EventStartTime, '+1 minute') AND time(EventEndTime, '-1 minute'))
        OR (time(EventStartTime, '+1 minute') BETWEEN ? AND ?)
    )   
'''

cursor.execute(query, (target_date, target_start_time, target_end_time, target_start_time, target_end_time))
result = cursor.fetchall()

# Check if there are any rows in the result set
if result:
    print(f'The date and time range are already taken.')
else:
    print(f'The date and time range are available.')

# Close the connection
conn.close()
