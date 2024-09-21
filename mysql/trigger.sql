-- Active: 1697515802955@@127.0.0.1@3306@sprinthub

DELIMITER //

CREATE TRIGGER Update_Sprint_Status AFTER INSERT ON Task
FOR EACH ROW
BEGIN
    DECLARE total_tasks INT;
    DECLARE completed_tasks INT;

    SELECT COUNT(*) INTO total_tasks FROM Task WHERE Sprint_ID = NEW.Sprint_ID;
    SELECT COUNT(*) INTO completed_tasks FROM Task WHERE Sprint_ID = NEW.Sprint_ID AND Task_Status = 'Completed';

    IF total_tasks = completed_tasks THEN
        UPDATE Sprint SET Sprint_Status = 'Completed' WHERE Sprint_ID = NEW.Sprint_ID;
    END IF;
END;
//

DELIMITER ;