SELECT Candidate.ProcessID, Candidate.last_name, Candidate.first_name FROM TopCandidate
JOIN Candidate ON TopCandidate.CandidateID=Candidate.CandidateID
WHERE Candidate.ProcessID=?;