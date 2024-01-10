SELECT *
FROM Kalender
WHERE EventDate = ? 
AND(
    (? BETWEEN time(EventStartTime, '+1 minute') AND time(EventEndTime, '-1 minute'))
    OR (? BETWEEN time(EventStartTime, '+1 minute') AND time(EventEndTime, '-1 minute'))
    OR (time(EventStartTime, '+1 minute') BETWEEN ? AND ?)
)  