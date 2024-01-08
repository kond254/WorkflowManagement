INSERT INTO TopCandidate (CandidateID) 
SELECT CandidateID FROM Candidate
WHERE Candidate.ProcessID=?
ORDER BY Candidate.rating DESC
LIMIT 10;