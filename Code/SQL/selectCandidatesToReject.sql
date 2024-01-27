SELECT Candidate.ProcessID FROM TopCandidate
JOIN Candidate ON TopCandidate.CandidateID=Candidate.CandidateID
LIMIT 1