SELECT COUNT (Candidate.CandidateID) FROM TopCandidate 
JOIN Candidate ON Candidate.CandidateID=TopCandidate.CandidateID
WHERE Candidate.ProcessID=? AND InterviewAccepted=1;
