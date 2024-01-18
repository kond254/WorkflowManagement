SELECT * FROM TopCandidate 
JOIN Candidate ON TopCandidate.CandidateID=TopCandidate.CandidateID
WHERE Candidate.ProcessID=?
ORDER BY InterviewDate ASC
