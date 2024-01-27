SELECT TopCandidate.CandidateID FROM TopCandidate 
JOIN Candidate ON TopCandidate.CandidateID=Candidate.CandidateID 
WHERE Candidate.ProcessID=? and (TopCandidate.InterviewAccepted is null OR TopCandidate.InterviewAccepted=0)