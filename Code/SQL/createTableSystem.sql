CREATE TABLE SystemDB (
    ProcessID INT NOT NULL, 
    Contract VARCHAR(250),
    ContractSigned BOOL,
    Compensation FLOAT,
    PRIMARY KEY (ProcessID)
);