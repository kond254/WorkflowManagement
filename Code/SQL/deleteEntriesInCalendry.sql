DELETE FROM Kalender
WHERE CandidateID IN (
    SELECT Kalender.CandidateID
    FROM Kalender
    JOIN Candidate ON Kalender.CandidateID = Candidate.CandidateID
    JOIN TopCandidate ON Candidate.CandidateID = TopCandidate.CandidateID
    WHERE (TopCandidate.InterviewAccepted IS NULL OR TopCandidate.InterviewAccepted = 0) and Candidate.ProcessID=?
);