SELECT Candidate.* FROM TopCandidate 
JOIN Candidate ON TopCandidate.CandidateID=Candidate.CandidateID 
WHERE TopCandidate.CandidateID=?