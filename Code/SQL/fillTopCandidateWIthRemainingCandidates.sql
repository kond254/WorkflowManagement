CREATE TEMPORARY TABLE IF NOT EXISTS tmp_ProcessID AS SELECT ? AS ProcessID;

CREATE TEMPORARY TABLE IF NOT EXISTS tmp_MaxTopCandidates AS
SELECT 10 AS MaxTopCandidates;  

CREATE TEMPORARY TABLE IF NOT EXISTS tmp_CurrentTopCandidates AS
SELECT COUNT(*) AS CurrentTopCandidatesCount
FROM TopCandidate
JOIN Candidate ON TopCandidate.CandidateID = Candidate.CandidateID
WHERE Candidate.ProcessID = (SELECT ProcessID FROM tmp_ProcessID);

INSERT INTO TopCandidate (CandidateID)
SELECT CandidateID
FROM Candidate
WHERE ProcessID = (SELECT ProcessID FROM tmp_ProcessID)
  AND CandidateID NOT IN (SELECT CandidateID FROM TopCandidate)
ORDER BY Candidate.rating DESC
LIMIT (SELECT MaxTopCandidates FROM tmp_MaxTopCandidates) - (SELECT CurrentTopCandidatesCount FROM tmp_CurrentTopCandidates);

DROP TABLE IF EXISTS tmp_ProcessID;
DROP TABLE IF EXISTS tmp_CurrentTopCandidates;
DROP TABLE IF EXISTS tmp_MaxTopCandidates;  
