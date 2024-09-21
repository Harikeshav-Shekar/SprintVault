-- Active: 1697515802955@@127.0.0.1@3306@sprinthub

DELIMITER //

CREATE PROCEDURE GetUserTasks(IN uName VARCHAR(50))
BEGIN
    SELECT 
        T.Task_ID,
        T.Task_Name,
        T.Task_Description,
        T.Task_Status,
        T.Task_Priority,
        T.Task_Start_Date,
        T.Task_End_Date
    FROM User U
    JOIN Task T ON U.Sprint_ID = T.Sprint_ID
    WHERE U.Username = uName;
END;
//

DELIMITER ;

CALL GetUserTasks('anshul2004');