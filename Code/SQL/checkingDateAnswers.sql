SELECT COUNT (Candidate.CandidateID) FROM TopCandidate 
JOIN Candidate ON Candidate.CandidateID=TopCandidate.CandidateID
WHERE Candidate.Process_ID=? AND InterviewAccepted=1;