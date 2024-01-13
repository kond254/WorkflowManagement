DELETE FROM Candidate
JOIN Candidate ON Candidate.CandidateID=TopCandidate.CandidateID
WHERE Candidate.Process_ID=? AND JobAccepted=0 OR JobAccepted=NULL