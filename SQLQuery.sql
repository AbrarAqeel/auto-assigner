CREATE DATABASE Meezanship;
USE Meezanship;

GRANT ALL ON *.* to root@localhost IDENTIFIED BY '123321';

CREATE TABLE Agents (
    Agent_ID INT AUTO_INCREMENT PRIMARY KEY,
    Agent_Name VARCHAR(50) NOT NULL,
    Agent_Priority DECIMAL(3, 2) NOT NULL CHECK (Agent_Priority >= 0.01 AND Agent_Priority <= 0.99),
    Agent_Workload INT NOT NULL,
    Agent_Status ENUM('Available', 'Working', 'Offline', 'Break') NOT NULL DEFAULT 'Available',
    Visibility BOOLEAN DEFAULT TRUE
);

CREATE TABLE Agents_Login (
    Login_ID INT AUTO_INCREMENT PRIMARY KEY,
    Agent_ID INT NOT NULL,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    FOREIGN KEY (Agent_ID) REFERENCES Agents(Agent_ID)
) AUTO_INCREMENT = 100;


CREATE TABLE Forms (
    Form_ID INT AUTO_INCREMENT PRIMARY KEY,
    Form_Type VARCHAR(50) NOT NULL,
    Form_Detail VARCHAR(120) NOT NULL,
    Form_Status ENUM('Assigned', 'Unassigned', 'Completed') NOT NULL DEFAULT 'Unassigned',
    Assigned_Agent_ID INT,
    FOREIGN KEY (Assigned_Agent_ID) REFERENCES Agents(Agent_ID)
);


-- ---------------------------------------------- Triggers ------------------------------------------------------------ --


DELIMITER $$

-- Trigger to prevent special characters in Agent_Name

CREATE TRIGGER agent_name_validation
BEFORE INSERT ON Agents
FOR EACH ROW
BEGIN
    IF NEW.Agent_Name REGEXP '[^a-zA-Z0-9 ]' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Agent name must not contain special characters.';
    END IF;
END $$

-- Trigger to prevent special characters in Form_Type

CREATE TRIGGER form_type_validation
BEFORE INSERT ON Forms
FOR EACH ROW
BEGIN
    IF NEW.Form_Type REGEXP '[^a-zA-Z0-9 ]' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Form type must not contain special characters.';
    END IF;
END $$

DELIMITER ;


-- ---------------------------------------------- Dummy Values ------------------------------------------------------------ --


-- INSERT INTO Agents (Agent_Name, Agent_Priority, Agent_Workload) VALUES
-- ('Agent A', 0.20, 4),
-- ('Agent B', 0.10, 2),
-- ('Agent C', 0.25, 5),
-- ('Agent D', 0.30, 8),
-- ('Agent E', 0.15, 3);

INSERT INTO Agents (Agent_Name, Agent_Priority, Agent_Workload, Agent_Status) VALUES
('Agent A', 0.20, 4, 'Available'),
('Agent B', 0.10, 2, 'Offline'),
('Agent C', 0.25, 5, 'Offline'),
('Agent D', 0.30, 8, 'Available'),
('Agent E', 0.15, 3, 'Available');


INSERT INTO Agents_Login (Agent_ID, Username, Password) VALUES
(1, 'agentA', 'password123'),
(2, 'agentB', 'password123'),
(3, 'agentC', 'password123'),
(4, 'agentD', 'password123'),
(5, 'agentE', 'password123');


INSERT INTO Forms (Form_Type, Form_Detail) VALUES
('Account Opening', 'I want to open a current account'),
('Account Closure', 'I want to close my savings account'),
('Balance Inquiry', 'I cannot see my account balance'),
('Dispute Request', 'I want to file for a dispute for a product I did not receive'),
('Increase Account Limit', 'I want to increase my monthly account limit'),
('New Debit Card', 'My card chip is damaged'),
('Credit Card', 'I want a credit card'),
('Loan Inquiry', 'I want information about a personal loan'),
('Change Address', 'I need to update my mailing address'),
('Account Statement', 'I need my account statement for the last year'),
('Fee Waiver Request', 'I would like to request a waiver for the maintenance fee'),
('ATM Issue', 'The ATM did not dispense cash but debited my account'),
('Account Opening', 'I want to open a savings account'),
('Account Closure', 'I want to close my current account'),
('Balance Inquiry', 'My balance seems incorrect'),
('Dispute Request', 'I want to dispute a transaction'),
('Increase Account Limit', 'I want to increase my daily withdrawal limit'),
('New Debit Card', 'My card is lost'),
('Credit Card', 'I want to upgrade my credit card'),
('Loan Inquiry', 'I want information about a car loan'),
('Change Address', 'I need to update my email address'),
('Account Statement', 'I need my account statement for the last month'),
('Fee Waiver Request', 'I would like to request a waiver for the overdraft fee'),
('ATM Issue', 'The ATM ate my card');


-- ---------------------------------------------- Viewing Tables ------------------------------------------------------------ --

select * from Agents;
select * from Agents_Login;
select * from Forms;

-- ---------------------------------------------- Deleting Tables ------------------------------------------------------------ --

drop table Agents_Login;
drop tables Forms, Agents;	
