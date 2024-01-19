DELETE FROM Candidate
WHERE Candidate.CandidateID IN (
    SELECT Candidate.CandidateID
    FROM Candidate
    JOIN TopCandidate ON Candidate.CandidateID = TopCandidate.CandidateID
    WHERE Candidate.CandidateID = ?
);