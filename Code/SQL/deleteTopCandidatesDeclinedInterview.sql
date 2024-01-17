DELETE FROM Candidate
JOIN Candidate ON Candidate.CandidateID=TopCandidate.CandidateID
WHERE Candidate.Process_ID=? AND InterviewAccepted=0 OR InterviewAccepted=NULL