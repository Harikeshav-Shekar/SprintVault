-- Active: 1697515802955@@127.0.0.1@3306@sprinthub

-- Testing the TRIGGER

-- Create a Sprint
INSERT INTO Sprint (Sprint_Name, Sprint_Start_Date, Sprint_End_Date, Sprint_Status, Sprint_Description) 
VALUES ('Sprint 1', '2023-11-01', '2023-11-15', 'Active', 'First Sprint');

-- Add Tasks to Sprint
INSERT INTO Task (Task_Name, Task_Description, Task_Status, Task_Priority, Task_Start_Date, Task_End_Date, Sprint_ID)
VALUES 
    ('Task 1', 'Description for Task 1', 'Completed', 'High', '2023-11-01', '2023-11-05', 13),
    ('Task 2', 'Description for Task 2', 'Completed', 'Medium', '2023-11-02', '2023-11-10', 13),
    ('Task 3', 'Description for Task 3', 'Completed', 'Low', '2023-11-03', '2023-11-12', 13);

-- Check the Sprint status
SELECT Sprint_Status FROM Sprint WHERE Sprint_ID = 13;



