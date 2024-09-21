## **User**

- UserID (Primary Key)
- Username
- Password
- Email
- Name
- Role
- Phone Number (Multivalued attribute)

## **Project**

- ProjectID (Primary Key)
- Project Name
- Start Date
- End Date
- Status
- Budget (Multivalued attribute)

## **Team**

- TeamID (Primary Key)
- Team Name
- Description

## **Team Member**

- TeamMemberID (Primary Key)
- TeamID (Foreign Key)
- UserID (Foreign Key)

## **Sprint**

- SprintID (Primary Key)
- ProjectID (Foreign Key)
- Sprint Name
- Description
- Start Date
- End Date
- Status

## **Scrum Master**

- ScrumMasterID (Primary Key)
- UserID (Foreign Key)
- SprintID (Foreign Key)

## **Task**

- TaskID (Primary Key)
- SprintID (Foreign Key)
- Task Name
- Description
- Priority
- Status
- Start Date (Multivalued attribute)
- End Date (Multivalued attribute)

## **User Story**

- StoryID (Primary Key)
- ProjectID (Foreign Key)
- SprintID (Foreign Key)
- Story Name
- Description
- Priority
- Status
- Acceptance Criteria (Multivalued attribute)

## **Comments**

- CommentID (Primary Key)
- TaskID (Foreign Key)
- UserStoryID (Foreign Key)
- UserID (Foreign Key)
- Comment Text
- Timestamp

## **Attachment**

- AttachmentID (Primary Key)
- TaskID (Foreign Key)
- UserStoryID (Foreign Key)
- FileName
- FileURL

## **Scrum Meeting (Weak Entity)**

- MeetingID (Primary Key)
- SprintID (Foreign Key)
- Meeting Date
- Meeting Notes

## **Retrospective Meeting (Weak Entity)**

- RetrospectiveID (Primary Key)
- SprintID (Foreign Key)
- Meeting Date
- Meeting Notes
  

## Relationships:

- User to Team Member: One-to-One (One User can be a member of one Team)
- User to Scrum Master: One-to-Many (One User can be a Scrum Master for many Sprints)
- Team to Team Member: One-to-Many (One Team can have many Team Members)
- Team Member to User: Many-to-One (Many Team Members can be the same User)
- Project to Sprint: One-to-Many (One Project can have many Sprints)
- Sprint to Scrum Master: One-to-Many (One Sprint can have one Scrum Master)
- Sprint to Task: One-to-Many (One Sprint can have many Tasks)
- Sprint to User Story: One-to-Many (One Sprint can have many User Stories)
- Task to Comments: One-to-Many (One Task can have many Comments)
- User Story to Comments: One-to-Many (One User Story can have many Comments)
- Task to Attachment: One-to-Many (One Task can have many Attachments)
- User Story to Attachment: One-to-Many (One User Story can have many Attachments)
- Sprint to Scrum Meeting (Weak Entity): One-to-Many (One Sprint can have many Scrum Meetings)
- Sprint to Retrospective Meeting (Weak Entity): One-to-Many (One Sprint can have many Retrospective Meetings)
