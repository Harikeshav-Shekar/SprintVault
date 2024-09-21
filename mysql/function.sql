-- Active: 1697515802955@@127.0.0.1@3306@sprinthub

DELIMITER //

CREATE FUNCTION GetTotalProjectBudget(projectID INT) RETURNS INT
READS SQL DATA
BEGIN
    DECLARE totalBudget INT;

    SELECT SUM(Budget) INTO totalBudget
    FROM Project_Budget
    WHERE Project_ID = projectID;

    IF totalBudget IS NULL THEN
        SET totalBudget = 0;
    END IF;

    RETURN totalBudget;
END;
//

DELIMITER ;


SELECT GetTotalProjectBudget(3);