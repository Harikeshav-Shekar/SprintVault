-- Active: 1697515802955@@127.0.0.1@3306@sprinthub
CREATE TABLE User(  
    User_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    Name VARCHAR(50),
    Username VARCHAR(50),
    Password VARCHAR(50),
    Role VARCHAR(60),
    Sprint_ID int
) COMMENT 'User Login Table';

CREATE TABLE Sprint(
    Sprint_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    Sprint_Name VARCHAR(50),
    Sprint_Start_Date DATE,
    Sprint_End_Date DATE,
    Sprint_Status VARCHAR(50),
    Sprint_Description VARCHAR(50),
    MASTER_ID int,
    STORY_ID int
) COMMENT 'Sprint Table';

CREATE TABLE Story(
    Story_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    Story_Name VARCHAR(50),
    Story_Description VARCHAR(50),
    Story_Status VARCHAR(50),
    Story_Priority VARCHAR(50),
    Attachement_ID int
) COMMENT 'Story Table';

CREATE TABLE Attachement(
    Attachement_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    Attachement_Name VARCHAR(50),
    Attachement_URL VARCHAR(50)
) COMMENT 'Attachement Table';

CREATE TABLE Scrum_Master(
    MASTER_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    USER_ID int 
) COMMENT 'Scrum Master Table';

CREATE TABLE Project(
    Project_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    Project_Name VARCHAR(50),
    Project_Description VARCHAR(50),
    Project_Status VARCHAR(50),
    Project_Start_Date DATE,
    Project_End_Date DATE,
    Project_Story_ID int,
    Project_Sprint_ID int,
    Budget int
) COMMENT 'Project Table';

CREATE TABLE Project_Budget(
    Budget int,
    Project_ID int
) COMMENT 'Project Budget Table';

CREATE TABLE Team_Member(
    Team_Member_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    Description VARCHAR(50),
    USER_ID int,
    Team_ID int
) COMMENT 'Team Member Table';

CREATE TABLE Team(
    Team_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    Team_Name VARCHAR(50),
    Team_Description VARCHAR(50)
) COMMENT 'Team Table';

CREATE TABLE Task(
    Task_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    Task_Name VARCHAR(50),
    Task_Description VARCHAR(50),
    Task_Status VARCHAR(50),
    Task_Priority VARCHAR(50),
    Task_Start_Date DATE,
    Task_End_Date DATE,
    Sprint_ID int,
    Attachment_ID int
);

CREATE TABLE Scrum_Meeting(
    Meeting_ID int NOT NULL UNIQUE,
    Meeting_Notes VARCHAR(50),
    Meeting_Date DATE,
    Sprint_ID int
);

CREATE TABLE Retrospective_Meeting(
    Meeting_ID int NOT NULL UNIQUE,
    Meeting_Notes VARCHAR(50),
    Meeting_Date DATE,
    Sprint_ID int
);

CREATE TABLE Comments(
    Comment_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    Comment_Task VARCHAR(50),
    Comment_Timestamp DATE,
    Comment_Task_ID int
);

CREATE TABLE Phone_Number(
    Phone_Number VARCHAR(50),
    USER_ID int
);

CREATE TABLE Acceptance_Criteria(
    Acceptance_Criteria_Description VARCHAR(50),
    Acceptance_Story_ID int
);

ALTER TABLE User ADD FOREIGN KEY (Sprint_ID) REFERENCES Sprint(Sprint_ID);

ALTER TABLE Sprint ADD FOREIGN KEY (MASTER_ID) REFERENCES Scrum_Master(MASTER_ID);

ALTER TABLE Sprint ADD FOREIGN KEY (STORY_ID) REFERENCES Story(Story_ID);

ALTER TABLE Story ADD FOREIGN KEY (Attachement_ID) REFERENCES Attachement(Attachement_ID);

ALTER TABLE scrum_master ADD FOREIGN KEY (USER_ID) REFERENCES User(User_ID);

ALTER TABLE Project ADD FOREIGN KEY (Project_Story_ID) REFERENCES Story(Story_ID);

ALTER TABLE Project ADD FOREIGN KEY (Project_Sprint_ID) REFERENCES Sprint(Sprint_ID);

ALTER TABLE Project_Budget ADD FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID);

ALTER TABLE Team_Member ADD FOREIGN KEY (USER_ID) REFERENCES User(User_ID);

ALTER TABLE Team_Member ADD FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID);

ALTER TABLE Task ADD FOREIGN KEY (Sprint_ID) REFERENCES Sprint(Sprint_ID);

ALTER TABLE Task ADD FOREIGN KEY (Attachment_ID) REFERENCES Attachement(Attachement_ID);

ALTER TABLE Scrum_Meeting ADD FOREIGN KEY (Sprint_ID) REFERENCES Sprint(Sprint_ID);

ALTER TABLE Retrospective_Meeting ADD FOREIGN KEY (Sprint_ID) REFERENCES Sprint(Sprint_ID);

ALTER TABLE Comments ADD FOREIGN KEY (Comment_Task_ID) REFERENCES Task(Task_ID);

ALTER TABLE Phone_Number ADD FOREIGN KEY (USER_ID) REFERENCES User(User_ID);

ALTER TABLE Acceptance_Criteria ADD FOREIGN KEY (Acceptance_Story_ID) REFERENCES Story(Story_ID);
