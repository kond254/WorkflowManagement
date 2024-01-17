DELETE FROM Candidate
JOIN Candidate ON Candidate.CandidateID=TopCandidate.CandidateID
WHERE CandidateID=?