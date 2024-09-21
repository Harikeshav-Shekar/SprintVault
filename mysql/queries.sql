-- Active: 1697515802955@@127.0.0.1@3306@sprinthub

--Correlated Queries
SELECT Project_Name
FROM Project p
WHERE p.Project_End_Date < CURDATE()
AND p.Project_Status <> 'Completed';

SELECT u.Name AS User_Name
FROM User u
WHERE (
    SELECT COUNT(DISTINCT p.Project_ID)
    FROM Project p
    WHERE p.Project_Sprint_ID = u.Sprint_ID
) > 1;

SELECT s.Sprint_Name, st.Story_Name, a.Attachement_Name
FROM Sprint s
LEFT JOIN Story st ON s.STORY_ID = st.STORY_ID
LEFT JOIN Attachement a ON st.Attachement_ID = a.Attachement_ID;

SELECT
    p.Project_Name,
    s.Sprint_Name,
    COUNT(st.Story_ID) AS Story_Count
FROM
    Project p
LEFT JOIN
    Sprint s ON p.Project_Sprint_ID = s.Sprint_ID
LEFT JOIN
    Story st ON s.STORY_ID = st.Story_ID
GROUP BY
    p.Project_ID, s.Sprint_ID
ORDER BY
    p.Project_Name, s.Sprint_Name;
