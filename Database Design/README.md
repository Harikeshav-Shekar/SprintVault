## System Features and Function Requirements 
### User Registration and Authentication:
<pre>
Entities Involved:
    User Entity: This entity represents the users who will register and use the system. It includes attributes such as UserID, Username, Password, Email, Name, Role, and Phone Number.
Input Required:
    User Information: The necessary input includes user-provided information during the registration process, such as:
      •	Username: The chosen username for the user's account.
      •	Password: The user's selected password for secure access.
      •	Email: The user's email address for communication and notifications.
      •	Name: The user's full name for identification.
      •	Role: The user's role or access level within the system (e.g., project manager, team member).
      •	Phone Number: Contact information for the user (if applicable).
The feature involves collecting this user-provided input, validating it, and securely storing the user's registration details for authentication during subsequent logins.
</pre>

### Project Creation and Management:
<pre>
Entities Involved:
    Project Entity: This entity represents the projects that users create and manage within the system. It includes attributes such as ProjectID, Project Name, Start Date, End Date, Status, and Budget.
Input Required:
    Project Details: The necessary input includes project-specific details provided by the user or project manager during project creation and management:
      •	Project Name: A unique name for the project.
      •	Start Date: The date when the project is initiated.
      •	End Date: The projected or planned completion date for the project.
      •	Status: The current status of the project (e.g., planning, in progress, completed).
      •	Budget: Budget allocation or financial resources assigned to the project (if applicable).
This feature allows project managers and authorized users to input and manage project details, enabling effective project planning and oversight within the Agile Project Management Tool.
</pre>

### Sprint Planning:

<pre>
Entities Involved:
    Sprint Entity: This entity represents the individual sprints that are planned and executed within a project. It includes attributes such as SprintID, Sprint Name, Description, Start Date, End Date, and Status.
Input Required:
    Sprint Details: The necessary input includes details specific to the sprint that are provided by project managers or users responsible for sprint planning:
      •	Sprint Name: A unique name or identifier for the sprint.
      •	Description: A brief description outlining the goals and objectives of the sprint.
      •	Start Date: The planned start date of the sprint.
      •	End Date: The planned end date of the sprint.
      •	Status: The current status of the sprint (e.g., planning, active, completed).
Additionally, during sprint planning, project managers and teams may associate user stories and tasks with the sprint, specifying the work that will be addressed during that sprint.
This feature enables project managers and teams to define and schedule sprints, set sprint goals, and establish timelines, providing a structured approach to Agile development within the Agile Project Management Tool.
</pre>

### Comments and Attachments:

<pre>
Entities Involved:
    Task Entity: This entity represents individual tasks that are part of the project. It includes attributes such as TaskID, Task Name, Description, Priority, and Status.
    User Story Entity: This entity represents user stories that define project requirements. It includes attributes such as StoryID, Story Name, Description, Priority, and Status.
    Comments Entity: This entity represents comments made by users related to tasks and user stories. It includes attributes such as CommentID, TaskID (Foreign Key), UserStoryID (Foreign Key), UserID (Foreign Key), Comment Text, and Timestamp.
    Attachment Entity: This entity represents file attachments associated with tasks and user stories. It includes attributes such as AttachmentID, TaskID (Foreign Key), UserStoryID (Foreign Key), FileName, and FileURL.
Input Required:
    Comment Text: Users can input text to provide comments related to specific tasks or user stories. These comments serve as a means of communication, updates, and discussions.
    Attachments: Users can upload files (attachments) related to tasks or user stories. This input allows for the sharing and documentation of relevant files and resources within the project.
The feature enables users to engage in discussions, provide updates, and share files or resources, enhancing collaboration and communication within the Agile Project Management Tool.
</pre>

### Meetings Management:

<pre>
Entities Involved:
    Sprint Entity: This entity represents individual sprints within a project. It includes attributes such as SprintID, Sprint Name, Description, Start Date, End Date, and Status.
    Scrum Meeting (Weak Entity): This weak entity represents Scrum meetings that occur during a sprint. It includes attributes such as MeetingID (Primary Key), SprintID (Foreign Key), Meeting Date, and Meeting Notes.
    Retrospective Meeting (Weak Entity): This weak entity represents retrospective meetings that occur during a sprint. It includes attributes such as RetrospectiveID (Primary Key), SprintID (Foreign Key), Meeting Date, and Meeting Notes.
Input Required:
    Meeting Details: The necessary input includes details specific to the meeting, which may include:
      •	Meeting Date: The date when the meeting is scheduled or took place.
      •	Meeting Notes: Notes or minutes of the meeting capturing discussions, decisions, and action items.
The feature allows users to schedule, document, and manage Scrum Meetings and Retrospective Meetings within the context of specific sprints, facilitating efficient project management and communication within the Agile Project Management Tool.
</pre>

### Task and User Story Management:

<pre>
Entities Involved:
    Task Entity: This entity represents individual tasks that are part of the project. It includes attributes such as TaskID, Task Name, Description, Priority, Status, Start Date (Multivalued attribute), and End Date (Multivalued attribute).
    User Story Entity: This entity represents user stories that define project requirements. It includes attributes such as StoryID, Story Name, Description, Priority, Status, and Acceptance Criteria (Multivalued attribute).
Input Required:
    Task Details: The necessary input includes details specific to tasks that are provided by project managers and team members:
      •	Task Name: A unique name or identifier for the task.
      •	Description: A description outlining the details of the task.
      •	Priority: The priority level of the task (e.g., high, medium, low).
      •	Status: The current status of the task (e.g., to-do, in progress, done).
      •	Start Date (Multivalued): The date when the task was started or planned to start.
      •	End Date (Multivalued): The date when the task was completed or is planned to be completed.
    User Story Details: The necessary input includes details specific to user stories, often defined by product owners or stakeholders:
      •	Story Name: A unique name or identifier for the user story.
      •	Description: A description of the user story, outlining its purpose and requirements.
      •	Priority: The priority level of the user story (e.g., high, medium, low).
      •	Status: The current status of the user story (e.g., to-do, in progress, done).
      •	Acceptance Criteria (Multivalued): Specific conditions that must be met for the user story to be considered complete.
This feature allows project managers, product owners, and team members to create, assign, and track tasks and user stories, enabling effective project planning and execution within the Agile Project Management Tool.
</pre>
