SELECT Candidate.CandidateID FROM TopCandidate
JOIN Candidate ON TopCandidate.CandidateID=Candidate.CandidateID
WHERE Candidate.ProcessID=?
LIMIT 1