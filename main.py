import streamlit as st
import mysql.connector
from PIL import Image
import pandas as pd

def create_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Password123",
        database="sprintvault",
        port=3306
    )

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()

def execute_select_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        connection = create_connection()
        login_query = f"SELECT * FROM User WHERE Username='{username}' AND Password='{password}'"
        user_data = execute_select_query(connection, login_query)

        if user_data:
            st.success("Login successful!")

            if user_data[0]["Role"] == "Admin":
                st.success("Redirecting to Admin page...")
            elif user_data[0]["Role"] == "User":
                st.success("Redirecting to User page")

        else:
            st.error("Invalid username or password")

        connection.close()

def handle_signup(name, username, password, role, sprint_id):
    connection = create_connection()

    # Inserting data into User table
    signup_query = f"INSERT INTO User (Name, Username, Password, Role, Sprint_ID) VALUES ('{name}', '{username}', '{password}', '{role}', {sprint_id or 'NULL'})"
    execute_query(connection, signup_query)

    st.success("Sign up successful! Redirecting to login page...")
    connection.close()

def home_page():
    image = Image.open(r'C:\Users\there\Documents\Tech Projects\SprintVault\templates\logo.png')
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(image, width=200)  
        
    st.markdown(
        """
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }

            .header {
                text-align: center;
                padding: 20px 0;
            }

            .container {
                border-radius: 10px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                padding: 30px;
                text-align: center;
                margin: 20px auto;
                max-width: 800px;
            }

            h1 {
                color: #660066;
                font-size: 42px;
            }

            h2 {
                color: #660066;
                font-size: 24px;
            }

            p {
                font-size: 18px;
                line-height: 1.6;
            }
            .feature-box {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin: 20px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="header">
            <h1>Welcome to SprintVault</h1>
        </div>

        <div class="container">
            <p>Sprint Vault is a powerful Agile project management tool designed to streamline your software development projects. With features tailored for Scrum, Kanban, and Agile methodologies, Sprint Vault empowers teams to plan, execute, and optimize their projects with ease.</p>
        </div>
            <div class="container">

        <div class="feature-box">
            <h2>Agile Project Management</h2>
            <p>Efficiently manage your software development projects using Agile methodologies.</p>
        </div>

        <div class="feature-box">
            <h2>Scrum & Kanban Support</h2>
            <p>Customize your workflow with support for Scrum and Kanban methodologies.</p>
        </div>

        <div class="feature-box">
            <h2>Optimize Your Projects</h2>
            <p>Optimize your project execution and improve team collaboration.</p>
        </div>
        """
        ,
        unsafe_allow_html=True
    )
    st.subheader('SQL Query Executor')

    query = st.text_area('Enter your SQL query:', '')
    print(query)
    # Execute query on button click
    if st.button('Execute'):
        conn = create_connection()
        if query:
            result = execute_select_query(conn, query)
            if result:
                df = pd.DataFrame(result)
                st.write(df)
            else:
                st.write('No results to display')
        conn.close()

def user_page():
    st.title("User Page")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    if not username or not password:
        st.warning("Please enter both username and password.")
        return
    
    connection = create_connection()
    login_query = f"SELECT * FROM User WHERE Username='{username}' AND Password='{password}'"
    user_data = execute_select_query(connection, login_query)
    connection.close()

    if user_data:
        st.success("Login successful!")
        selected_table = st.selectbox("Select Table", ["Home","Sprint", "Story", "Attachement", "Scrum_Master", "Project","Team_Member", "Team", "Task", "Scrum_Meeting", "Retrospective_Meeting", "Comments", "Phone_Number", "Acceptance_Criteria"])

        if selected_table == "Home":
            st.write("Welcome to the User Page. Select a table from the dropdown to perform operations.")
            st.subheader("Procedure to get all the Tasks Assigned to You")
            username_in = st.text_input("Enter Your Username")
            if st.button("Get all The Tasks Assigned to You"):
                connection = create_connection()
                sql_query = f"CALL GetUserTasks('{username_in}');"
                result = execute_select_query(connection, sql_query)
                connection.close()
                st.table(result)
            
            st.markdown("---") 

            st.subheader("Queries")
            st.write("Selects project names from the 'Project' table that have surpassed their deadlines and are not Completed.")

            if st.button("Get Project Names"):
                connection = create_connection()
                sql_query = f"SELECT Project_Name FROM Project p WHERE p.Project_End_Date < CURDATE() AND p.Project_Status <> 'Completed';"
                result = execute_select_query(connection, sql_query)
                connection.close()
                st.table(result)
            
            st.write("Users that are linked to more than one project through their assigned sprint.")

            if st.button("Get Users"):
                connection = create_connection()
                sql_query = f"SELECT u.Name AS User_Name FROM User u WHERE ( SELECT COUNT(DISTINCT p.Project_ID) FROM Project p WHERE p.Project_Sprint_ID = u.Sprint_ID) > 1"
                result = execute_select_query(connection, sql_query)
                connection.close()
                st.table(result)

        elif selected_table == "Sprint":
            display_sprint_table()

        elif selected_table == "Story":
            display_story_table()
    
        elif selected_table == "Attachement":
            display_attachement_table()
            attachment_operations()

        elif selected_table == "Scrum_Master":
            display_scrum_master_table()

        elif selected_table == "Project":
            display_project_table()

        elif selected_table == "Team_Member":
            display_team_member_table()

        elif selected_table == "Team":
            display_team_table()
        
        elif selected_table == "Task":
            display_task_table()

        elif selected_table == "Scrum_Meeting":
            display_scrum_meeting_table()
        
        elif selected_table == "Retrospective_Meeting":
            display_retrospective_meeting_table()

        elif selected_table == "Comments":
            display_comments_table()
            comments_operations()
        
        elif selected_table == "Phone_Number":
            display_phone_number_table()
            phone_number_operations()
        
        elif selected_table == "Acceptance_Criteria":
            display_acceptance_criteria_table()
    else:
        st.warning("Invalid username or password. Please sign up first.")
        st.warning("Redirecting to Signup page...")    

def stored_function(project_id):
    connection = create_connection()
    sql_query = f"SELECT GetTotalProjectBudget({project_id}) as Total_Budeget;"
    result = execute_select_query(connection, sql_query)
    connection.close()
    return result[0]["Total_Budeget"]

def is_admin_logged_in():
    admin_password = "Anshul@2004"
    entered_password = st.text_input("Enter Admin Password", type="password")
    
    return entered_password == admin_password

def admin_page():
    st.title("Admin Page")

    if not is_admin_logged_in():
        st.warning("Access denied. Please log in as an admin.")
        return
    
    st.empty()
    
    selected_table = st.selectbox("Select Table", ["Home", "User", "Sprint", "Story", "Attachement", "Scrum_Master", "Project", "Project_Budget", "Team_Member", "Team", "Task", "Scrum_Meeting", "Retrospective_Meeting", "Comments", "Phone_Number", "Acceptance_Criteria"])

    if selected_table == "Home":
        st.write("Welcome to the Admin Page. Select a table from the dropdown to perform CRUD operations.")
        st.subheader("Function to Calculate the total budget of the project")
        project_id = st.number_input("Enter the Project ID")
        if st.button("Calculate the total Budget of the Project"):
            total_budget = stored_function(project_id)
            st.write(f"The total budget of the project is {total_budget}")

        st.markdown("---") 

        st.subheader("Queries")
        st.write("Retrieves Sprint names, associated Story names, and their respective attachment names.")

        if st.button("Get Sprint, Story and Attachment Names"):
            connection = create_connection()
            sql_query = f"SELECT s.Sprint_Name, st.Story_Name, a.Attachement_Name FROM Sprint s LEFT JOIN Story st ON s.STORY_ID = st.STORY_ID LEFT JOIN Attachement a ON st.Attachement_ID = a.Attachement_ID;"
            result = execute_select_query(connection, sql_query)
            connection.close()
            st.table(result)
        
        st.write("Retrieves project and sprint names along with the count of associated stories for each project in the system.")

        if st.button("Get Project and Sprint Names"):
            connection = create_connection()
            sql_query = f"SELECT p.Project_Name, s.Sprint_Name, COUNT(st.Story_ID) AS Story_Count FROM Project p LEFT JOIN Sprint s ON p.Project_Sprint_ID = s.Sprint_ID LEFT JOIN Story st ON s.STORY_ID = st.Story_ID GROUP BY p.Project_ID, s.Sprint_ID ORDER BY p.Project_Name, s.Sprint_Name;"
            result = execute_select_query(connection, sql_query)
            connection.close()
            st.table(result)

    if selected_table == "User":
        display_user_table()

        # Add new user form
        st.subheader("Add New User")
        name = st.text_input("Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.text_input("Role")
        sprint_id = st.text_input("Sprint ID (Optional)")
        add_button = st.button("Add User", key="add_user")
        if add_button:
            add_user(name, username, password, role, sprint_id)

        # Update existing user form
        st.subheader("Update User")
         # Form input for update
        user_id = st.text_input("User ID")
        name = st.text_input("New Name (Optional)")
        username = st.text_input("New Username (Optional)")
        password = st.text_input("New Password (Optional)", type="password")
        role = st.text_input("New Role (Optional)")
        sprint_id = st.text_input("New Sprint ID (Optional)")

        # Submit button for update
        update_button = st.button("Update User")

        if update_button:
        # Call the update_user function with the provided values
            update_user(user_id, Name=name, Username=username, Password=password, Role=role, Sprint_ID=sprint_id)


        # Delete user form
        st.subheader("Delete User")
        delete_user_id = st.text_input("User ID to Delete")
        delete_button = st.button("Delete User", key="delete_user")
        if delete_button:
            delete_user(delete_user_id)

    elif selected_table == "Sprint":
        display_sprint_table()

        # Add new sprint form
        st.subheader("Add New Sprint")
        sprint_name = st.text_input("Sprint Name")
        sprint_start_date = st.date_input("Sprint Start Date")
        sprint_end_date = st.date_input("Sprint End Date")
        sprint_status = st.text_input("Sprint Status")
        sprint_description = st.text_input("Sprint Description")
        master_id = st.text_input("Master ID (Optional)")
        story_id = st.text_input("Story ID (Optional)")
        add_sprint_button = st.button("Add Sprint", key="add_sprint")
        if add_sprint_button:
            add_sprint(sprint_name, sprint_start_date, sprint_end_date, sprint_status, sprint_description, master_id, story_id)

        # Update existing sprint form
        st.subheader("Update Sprint")
        sprint_id = st.text_input("Sprint ID")
        sprint_name = st.text_input("New Sprint Name (Optional)")
        sprint_start_date = st.date_input("New Sprint Start Date (Optional)")
        sprint_end_date = st.date_input("New Sprint End Date (Optional)")
        sprint_status = st.text_input("New Sprint Status (Optional)")
        sprint_description = st.text_input("New Sprint Description (Optional)")
        master_id = st.text_input("New Master ID (Optional)")
        story_id = st.text_input("New Story ID (Optional)")

        # Submit button for update
        update_sprint_button = st.button("Update Sprint")
        if update_sprint_button:
            # Call the update_sprint function with the provided values
            update_sprint(sprint_id, Sprint_Name=sprint_name, Sprint_Start_Date=sprint_start_date, Sprint_End_Date=sprint_end_date, Sprint_Status=sprint_status, Sprint_Description=sprint_description, MASTER_ID=master_id, STORY_ID=story_id)

        # Delete sprint form
        st.subheader("Delete Sprint")
        delete_sprint_id = st.text_input("Sprint ID to Delete")
        delete_sprint_button = st.button("Delete Sprint", key="delete_sprint")
        if delete_sprint_button:
            delete_sprint(delete_sprint_id)
    
    elif selected_table == "Story":
        display_story_table()
        story_operations()

    elif selected_table == "Attachement":
        display_attachement_table()
        attachment_operations()
    
    elif selected_table == "Scrum_Master":
        display_scrum_master_table()
        scrum_master_operations()
    
    elif selected_table == "Project":
        display_project_table()
        project_operations()
    
    elif selected_table == "Project_Budget":
        display_project_budget_table()
        project_budget_operations()
    
    elif selected_table == "Team_Member":
        display_team_member_table()
        team_member_operations()
    
    elif selected_table == "Team":
        display_team_table()
        team_operations()
    
    elif selected_table == "Task":
        display_task_table()
        task_operations()

    elif selected_table == "Scrum_Meeting":
        display_scrum_meeting_table()
        scrum_meeting_operations()
    
    elif selected_table == "Retrospective_Meeting":
        display_retrospective_meeting_table()
        retrospective_meeting_operations()

    elif selected_table == "Comments":
        display_comments_table()
        comments_operations()
    
    elif selected_table == "Phone_Number":
        display_phone_number_table()
        phone_number_operations()
    
    elif selected_table == "Acceptance_Criteria":
        display_acceptance_criteria_table()
        acceptance_criteria_operations()

def display_user_table():
    connection = create_connection()
    query = "SELECT * FROM User"
    result = execute_select_query(connection, query)
    connection.close()

    # Display the result using Streamlit
    st.table(result)

def add_user(name, username, password, role, sprint_id):
    connection = create_connection()

    # Inserting data into User table
    query = f"INSERT INTO User (Name, Username, Password, Role, Sprint_ID) VALUES ('{name}', '{username}', '{password}', '{role}', {sprint_id or 'NULL'})"
    execute_query(connection, query)

    connection.close()
    st.success("User added successfully!")

def update_user(user_id, **kwargs):
    connection = create_connection()

    # Generate the SET clause for the UPDATE query
    set_values = []

    for key, value in kwargs.items():
        if value is not None and value != "":
            set_values.append(f"{key} = '{value}'")
        else:
            set_values.append(f"{key} = {key}")  # Keep the field unchanged

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE User SET {set_clause} WHERE User_ID = {user_id}"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"User with ID {user_id} updated successfully!")

    connection.close()

def delete_user(user_id):
    connection = create_connection()

    # Deleting data from User table
    query = f"DELETE FROM User WHERE User_ID={user_id}"
    execute_query(connection, query)

    connection.close()
    st.success("User deleted successfully!")

def display_sprint_table():
    connection = create_connection()
    query = "SELECT * FROM Sprint"
    result = execute_select_query(connection, query)
    connection.close()

    if result:
        st.subheader("Sprint Table")
        st.table(result)
    else:
        st.info("No data available in Sprint table.")

def add_sprint(Sprint_Name, Sprint_Start_Date, Sprint_End_Date, Sprint_Status, Sprint_Description, MASTER_ID=None, STORY_ID=None):
    connection = create_connection()
    query = f"INSERT INTO Sprint (Sprint_Name, Sprint_Start_Date, Sprint_End_Date, Sprint_Status, Sprint_Description, MASTER_ID, STORY_ID) VALUES ('{Sprint_Name}', '{Sprint_Start_Date}', '{Sprint_End_Date}', '{Sprint_Status}', '{Sprint_Description}', {MASTER_ID or 'NULL'}, {STORY_ID or 'NULL'})"
    execute_query(connection, query)
    connection.close()

    st.success("Sprint added successfully!")

def update_sprint(sprint_id, **kwargs):
    connection = create_connection()

    # Generate the SET clause for the UPDATE query
    set_values = []

    for key, value in kwargs.items():
        if value is not None and value != "":
            set_values.append(f"{key} = '{value}'")
        else:
            set_values.append(f"{key} = {key}")  # Keep the field unchanged

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Sprint SET {set_clause} WHERE Sprint_ID = {sprint_id}"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Sprint with ID {sprint_id} updated successfully!")

    connection.close()

def delete_sprint(Sprint_ID):
    connection = create_connection()
    query = f"DELETE FROM Sprint WHERE Sprint_ID={Sprint_ID}"
    execute_query(connection, query)
    connection.close()

    st.success("Sprint deleted successfully!")

def add_story(Story_Name, Story_Description, Story_Status, Story_Priority, Attachement_ID):
    connection = create_connection()
    add_story_query = f"INSERT INTO Story (Story_Name, Story_Description, Story_Status, Story_Priority, Attachement_ID) VALUES " \
                      f"('{Story_Name}', '{Story_Description}', '{Story_Status}', '{Story_Priority}', {Attachement_ID or 'NULL'})"
    execute_query(connection, add_story_query)

    st.success("Story added successfully!")

    connection.close()

def update_story(story_id, **kwargs):
    connection = create_connection()
    set_values = []

    for key, value in kwargs.items():
        if value is not None and value != "":
            set_values.append(f"{key} = '{value}'")
        else:
            set_values.append(f"{key} = {key}")  # Keep the field unchanged

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Story SET {set_clause} WHERE Story_ID = {story_id}"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Story with ID {story_id} updated successfully!")

    connection.close()

def delete_story(story_id):
    connection = create_connection()

    # Deleting data from Story table
    delete_story_query = f"DELETE FROM Story WHERE Story_ID = {story_id}"
    execute_query(connection, delete_story_query)

    st.success(f"Story with ID {story_id} deleted successfully!")

    connection.close()

def display_story_table():
    connection = create_connection()

    story_query = "SELECT * FROM Story"
    story_data = execute_select_query(connection, story_query)
    connection.close()
    st.table(story_data)
    connection.close()

def story_operations():
    st.subheader("Story Operations")

    # Add new story form
    st.subheader("Add New Story")
    Story_Name = st.text_input("Story Name")
    Story_Description = st.text_input("Story Description")
    Story_Status = st.text_input("Story Status")
    Story_Priority = st.text_input("Story Priority")
    Attachement_ID = st.text_input("Attachment ID (Optional)")
    add_button = st.button("Add Story", key="add_story")
    if add_button:
        add_story(Story_Name, Story_Description, Story_Status, Story_Priority, Attachement_ID)

    # Update existing story form
    st.subheader("Update Story")
    # Form input for update
    story_id = st.text_input("Story ID")
    Story_Name = st.text_input("New Story Name (Optional)")
    Story_Description = st.text_input("New Story Description (Optional)")
    Story_Status = st.text_input("New Story Status (Optional)")
    Story_Priority = st.text_input("New Story Priority (Optional)")
    Attachement_ID = st.text_input("New Attachment ID (Optional)")

    # Submit button for update
    update_button = st.button("Update Story")
    if update_button:
        # Call the update_story function with the provided values
        update_story(story_id, Story_Name=Story_Name, Story_Description=Story_Description,
                     Story_Status=Story_Status, Story_Priority=Story_Priority, Attachement_ID=Attachement_ID)

    # Delete story form
    st.subheader("Delete Story")
    delete_story_id = st.text_input("Story ID to Delete")
    delete_button = st.button("Delete Story", key="delete_story")
    if delete_button:
        delete_story(delete_story_id)

def display_attachement_table():
    connection = create_connection()
    query = "SELECT * FROM Attachement"
    result = execute_select_query(connection, query)
    st.table(result)
    connection.close()

def add_attachment(attachement_name, attachement_url):
    connection = create_connection()
    insert_query = f"INSERT INTO Attachement (Attachement_Name, Attachement_URL) VALUES ('{attachement_name}', '{attachement_url}')"
    execute_query(connection, insert_query)
    st.success("Attachement added successfully!")
    connection.close()

def update_attachment(attachement_id, attachement_name=None, attachement_url=None):
    connection = create_connection()
    set_values = []

    if attachement_name is not None:
        set_values.append(f"Attachement_Name = '{attachement_name}'")
    if attachement_url is not None:
        set_values.append(f"Attachement_URL = '{attachement_url}'")

    set_clause = ", ".join(set_values)

    update_query = f"UPDATE Attachement SET {set_clause} WHERE Attachement_ID = {attachement_id}"
    execute_query(connection, update_query)

    st.success(f"Attachement with ID {attachement_id} updated successfully!")

    connection.close()

def delete_attachment(attachement_id):
    connection = create_connection()
    delete_query = f"DELETE FROM Attachement WHERE Attachement_ID = {attachement_id}"
    execute_query(connection, delete_query)
    st.success(f"Attachement with ID {attachement_id} deleted successfully!")
    connection.close()

def attachment_operations():
    st.subheader("Attachment Operations")

    # Add new attachment form
    st.subheader("Add New Attachment")
    attachment_name = st.text_input("Attachment Name")
    attachment_url = st.text_input("Attachment URL")
    add_button = st.button("Add Attachment", key="add_attachment")
    if add_button:
        add_attachment(attachment_name, attachment_url)

    # Update existing attachment form
    st.subheader("Update Attachment")
    # Form input for update
    attachment_id = st.text_input("Attachment ID")
    attachment_name = st.text_input("New Attachment Name (Optional)")
    attachment_url = st.text_input("New Attachment URL (Optional)")

    # Submit button for update
    update_button = st.button("Update Attachment")
    if update_button:
        # Call the update_attachment function with the provided values
        update_attachment(attachment_id, attachement_name=attachment_name, attachement_url=attachment_url)

    # Delete attachment form
    st.subheader("Delete Attachment")
    delete_attachment_id = st.text_input("Attachment ID to Delete")
    delete_button = st.button("Delete Attachment", key="delete_attachment")
    if delete_button:
        delete_attachment(delete_attachment_id)

def display_scrum_master_table():
    # Function to display the Scrum_Master table
    connection = create_connection()
    query = "SELECT * FROM Scrum_Master"
    result = execute_select_query(connection, query)
    st.table(result)
    connection.close()

def add_scrum_master(USER_ID):
    # Function to add a new Scrum Master
    connection = create_connection()
    query = f"INSERT INTO Scrum_Master (USER_ID) VALUES ({USER_ID})"
    execute_query(connection, query)
    connection.close()
    st.success("Scrum Master added successfully!")

def update_scrum_master(MASTER_ID, USER_ID=None):
    # Function to update an existing Scrum Master
    connection = create_connection()
    
    # Generate the SET clause for the UPDATE query
    set_values = []

    if USER_ID is not None and USER_ID != "":
        set_values.append(f"USER_ID = '{USER_ID}'")
    else:
        set_values.append("USER_ID = USER_ID")  # Keep the field unchanged

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Scrum_Master SET {set_clause} WHERE MASTER_ID = {MASTER_ID}"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Scrum Master with ID {MASTER_ID} updated successfully!")

    connection.close()

def delete_scrum_master(MASTER_ID):
    # Function to delete an existing Scrum Master
    connection = create_connection()
    query = f"DELETE FROM Scrum_Master WHERE MASTER_ID = {MASTER_ID}"
    execute_query(connection, query)
    connection.close()
    st.success(f"Scrum Master with ID {MASTER_ID} deleted successfully!")

def scrum_master_operations():
    st.subheader("Scrum Master Operations")

    # Add new Scrum Master form
    st.subheader("Add New Scrum Master")
    user_id = st.text_input("User ID")
    add_button = st.button("Add Scrum Master", key="add_scrum_master")
    if add_button:
        add_scrum_master(user_id)

    # Update existing Scrum Master form
    st.subheader("Update Scrum Master")
    # Form input for update
    master_id = st.text_input("Scrum Master ID")
    user_id = st.text_input("New User ID (Optional)")

    # Submit button for update
    update_button = st.button("Update Scrum Master")
    if update_button:
        # Call the update_scrum_master function with the provided values
        update_scrum_master(master_id, USER_ID=user_id)

    # Delete Scrum Master form
    st.subheader("Delete Scrum Master")
    delete_master_id = st.text_input("Scrum Master ID to Delete")
    delete_button = st.button("Delete Scrum Master", key="delete_scrum_master")
    if delete_button:
        delete_scrum_master(delete_master_id)

def display_project_table():
    # Function to display the Project table
    connection = create_connection()
    query = "SELECT * FROM Project"
    result = execute_select_query(connection, query)
    connection.close()

    if result:
        st.subheader("Project Table")
        st.table(result)
    else:
        st.warning("No data in Project table.")

def add_project(Project_Name, Project_Description, Project_Status, Project_Start_Date, Project_End_Date, Project_Story_ID, Project_Sprint_ID):
    # Function to add a new Project
    connection = create_connection()
    query = f"INSERT INTO Project (Project_Name, Project_Description, Project_Status, Project_Start_Date, Project_End_Date, Project_Story_ID, Project_Sprint_ID) " \
            f"VALUES ('{Project_Name}', '{Project_Description}', '{Project_Status}', '{Project_Start_Date}', '{Project_End_Date}', {Project_Story_ID or 'NULL'}, {Project_Sprint_ID or 'NULL'})"
    execute_query(connection, query)
    connection.close()
    st.success("Project added successfully!")

def update_project(Project_ID, **kwargs):
    # Function to update an existing Project
    connection = create_connection()

    # Generate the SET clause for the UPDATE query
    set_values = []

    for key, value in kwargs.items():
        if value is not None and value != "":
            set_values.append(f"{key} = '{value}'")
        else:
            set_values.append(f"{key} = {key}")  # Keep the field unchanged

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Project SET {set_clause} WHERE Project_ID = {Project_ID}"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Project with ID {Project_ID} updated successfully!")

    connection.close()

def delete_project(Project_ID):
    # Function to delete an existing Project
    connection = create_connection()
    query = f"DELETE FROM Project WHERE Project_ID = {Project_ID}"
    execute_query(connection, query)
    connection.close()
    st.success(f"Project with ID {Project_ID} deleted successfully!")

def project_operations():
    st.subheader("Project Operations")

    # Add new Project form
    st.subheader("Add New Project")
    project_name = st.text_input("Project Name")
    project_description = st.text_input("Project Description")
    project_status = st.text_input("Project Status")
    project_start_date = st.date_input("Project Start Date")
    project_end_date = st.date_input("Project End Date")
    project_story_id = st.text_input("Project Story ID (Optional)")
    project_sprint_id = st.text_input("Project Sprint ID (Optional)")
    add_button = st.button("Add Project", key="add_project")
    if add_button:
        add_project(project_name, project_description, project_status, project_start_date, project_end_date, project_story_id, project_sprint_id)

    # Update existing Project form
    st.subheader("Update Project")
    # Form input for update
    project_id = st.text_input("Project ID")
    project_name = st.text_input("New Project Name (Optional)")
    project_description = st.text_input("New Project Description (Optional)")
    project_status = st.text_input("New Project Status (Optional)")
    project_start_date = st.date_input("New Project Start Date (Optional)")
    project_end_date = st.date_input("New Project End Date (Optional)")
    project_story_id = st.text_input("New Project Story ID (Optional)")
    project_sprint_id = st.text_input("New Project Sprint ID (Optional)")

    # Submit button for update
    update_button = st.button("Update Project")
    if update_button:
        # Call the update_project function with the provided values
        update_project(project_id, Project_Name=project_name, Project_Description=project_description,
                       Project_Status=project_status, Project_Start_Date=project_start_date,
                       Project_End_Date=project_end_date, Project_Story_ID=project_story_id,
                       Project_Sprint_ID=project_sprint_id)

    # Delete Project form
    st.subheader("Delete Project")
    delete_project_id = st.text_input("Project ID to Delete")
    delete_button = st.button("Delete Project", key="delete_project")
    if delete_button:
        delete_project(delete_project_id)

def display_project_budget_table():
    connection = create_connection()
    query = "SELECT * FROM Project_Budget"
    result = execute_select_query(connection, query)
    connection.close()

    st.subheader("Project Budget Table")
    st.table(result)

def add_project_budget(budget, project_id):
    connection = create_connection()
    query = f"INSERT INTO Project_Budget (Budget, Project_ID) VALUES ({budget}, {project_id})"
    execute_query(connection, query)
    st.success("Project Budget added successfully!")
    connection.close()

def update_project_budget(project_id, budget=None):
    connection = create_connection()

    set_values = []
    if budget is not None:
        set_values.append(f"Budget = {budget}")

    set_clause = ", ".join(set_values)

    query = f"UPDATE Project_Budget SET {set_clause} WHERE Project_ID = {project_id}"
    execute_query(connection, query)
    st.success(f"Project Budget for Project ID {project_id} updated successfully!")
    
    connection.close()

def delete_project_budget(project_id):
    connection = create_connection()
    query = f"DELETE FROM Project_Budget WHERE Project_ID = {project_id}"
    execute_query(connection, query)
    st.success(f"Project Budget for Project ID {project_id} deleted successfully!")
    connection.close()

def project_budget_operations():
    # Add new project budget form
    st.subheader("Add New Project Budget")
    budget = st.text_input("Budget")
    project_id = st.text_input("Project ID")
    add_project_budget_button = st.button("Add Project Budget", key="add_project_budget")
    if add_project_budget_button:
        add_project_budget(budget, project_id)

    # Update existing project budget form
    st.subheader("Update Project Budget")
    project_id_update = st.text_input("Project ID to Update")
    budget_update = st.text_input("New Budget (Optional)")
    update_project_budget_button = st.button("Update Project Budget", key="update_project_budget")
    if update_project_budget_button:
        update_project_budget(project_id_update, budget_update)

    # Delete project budget form
    st.subheader("Delete Project Budget")
    project_id_delete = st.text_input("Project ID to Delete")
    delete_project_budget_button = st.button("Delete Project Budget", key="delete_project_budget")
    if delete_project_budget_button:
        delete_project_budget(project_id_delete)

def display_team_member_table():
    connection = create_connection()
    team_member_query = "SELECT * FROM Team_Member"
    team_members = execute_select_query(connection, team_member_query)
    connection.close()

    # Display the Team_Member table
    st.subheader("Team Member Table")
    st.table(team_members)

def add_team_member(description, user_id, team_id):
    connection = create_connection()
    add_team_member_query = f"INSERT INTO Team_Member (Description, USER_ID, Team_ID) VALUES ('{description}', {user_id  or 'NULL'}, {team_id  or 'NULL'})"
    execute_query(connection, add_team_member_query)
    st.success("Team Member added successfully!")
    connection.close()

def update_team_member(team_member_id, description, user_id, team_id):
    connection = create_connection()

    # Generate the SET clause for the UPDATE query
    set_values = []

    for column, value in [("Description", description), ("USER_ID", user_id), ("Team_ID", team_id)]:
        if value is not None and value != "":
            set_values.append(f"{column} = '{value}'")
        else:
            set_values.append(f"{column} = {column}")  # Keep the field unchanged

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Team_Member SET {set_clause} WHERE Team_Member_ID = {team_member_id}"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Team Member with ID {team_member_id} updated successfully!")

    connection.close()

def delete_team_member(team_member_id):
    connection = create_connection()
    delete_team_member_query = f"DELETE FROM Team_Member WHERE Team_Member_ID = {team_member_id}"
    execute_query(connection, delete_team_member_query)
    st.success(f"Team Member with ID {team_member_id} deleted successfully!")
    connection.close()

def team_member_operations():
    # Add new team member form
    st.subheader("Add New Team Member")
    description = st.text_input("Description")
    user_id = st.text_input("User ID (Optional)")
    team_id = st.text_input("Team ID (Optional)")
    add_team_member_button = st.button("Add Team Member", key="add_team_member")
    if add_team_member_button:
        add_team_member(description, user_id, team_id)

    # Update existing team member form
    st.subheader("Update Team Member")
    team_member_id_update = st.text_input("Team Member ID to Update")
    description_update = st.text_input("New Description (Optional)")
    user_id_update = st.text_input("New User ID (Optional)")
    team_id_update = st.text_input("New Team ID (Optional)")
    update_team_member_button = st.button("Update Team Member", key="update_team_member")
    if update_team_member_button:
        update_team_member(team_member_id_update, description_update, user_id_update, team_id_update)

    # Delete team member form
    st.subheader("Delete Team Member")
    team_member_id_delete = st.text_input("Team Member ID to Delete")
    delete_team_member_button = st.button("Delete Team Member", key="delete_team_member")
    if delete_team_member_button:
        delete_team_member(team_member_id_delete)

def display_team_table():
    connection = create_connection()
    teams = execute_select_query(connection, "SELECT * FROM Team")
    connection.close()

    if teams:
        st.subheader("Team Table")
        st.table(teams)
    else:
        st.warning("No teams found in the database.")

def add_team(team_name, team_description):
    connection = create_connection()
    add_team_query = f"INSERT INTO Team (Team_Name, Team_Description) VALUES ('{team_name}', '{team_description}')"
    execute_query(connection, add_team_query)
    st.success("Team added successfully!")
    connection.close()

def update_team(team_id, team_name=None, team_description=None):
    connection = create_connection()

    # Generate the SET clause for the UPDATE query
    set_values = []

    if team_name is not None:
        set_values.append(f"Team_Name = '{team_name}'")

    if team_description is not None:
        set_values.append(f"Team_Description = '{team_description}'")

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Team SET {set_clause} WHERE Team_ID = {team_id}"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Team with ID {team_id} updated successfully!")

    connection.close()

def delete_team(team_id):
    connection = create_connection()
    delete_team_query = f"DELETE FROM Team WHERE Team_ID = {team_id}"
    execute_query(connection, delete_team_query)
    st.success(f"Team with ID {team_id} deleted successfully!")
    connection.close()

def team_operations():
    # Add new team form
    st.subheader("Add New Team")
    team_name = st.text_input("Team Name")
    team_description = st.text_input("Team Description")
    add_team_button = st.button("Add Team", key="add_team")
    if add_team_button:
        add_team(team_name, team_description)

    # Update existing team form
    st.subheader("Update Team")
    team_id_update = st.text_input("Team ID to Update")
    team_name_update = st.text_input("New Team Name (Optional)")
    team_description_update = st.text_input("New Team Description (Optional)")
    update_team_button = st.button("Update Team", key="update_team")
    if update_team_button:
        update_team(team_id_update, team_name_update, team_description_update)

    # Delete team form
    st.subheader("Delete Team")
    team_id_delete = st.text_input("Team ID to Delete")
    delete_team_button = st.button("Delete Team", key="delete_team")
    if delete_team_button:
        delete_team(team_id_delete)

def display_task_table():
    connection = create_connection()
    tasks = execute_select_query(connection, "SELECT * FROM Task")
    connection.close()

    if tasks:
        st.subheader("Task Table")
        st.table(tasks)
    else:
        st.warning("No tasks found in the database.")

def add_task(task_name, task_description, task_status, task_priority, task_start_date, task_end_date, sprint_id=None, attachment_id=None):
    connection = create_connection()

    # Convert None values to SQL NULL
    sprint_id = sprint_id if sprint_id is not None else "NULL"
    attachment_id = attachment_id if attachment_id is not None else "NULL"

    add_task_query = f"INSERT INTO Task (Task_Name, Task_Description, Task_Status, Task_Priority, Task_Start_Date, Task_End_Date, Sprint_ID, Attachment_ID) VALUES " \
                     f"('{task_name}', '{task_description}', '{task_status}', '{task_priority}', '{task_start_date}', '{task_end_date}', {sprint_id}, {attachment_id})"
    execute_query(connection, add_task_query)
    st.success("Task added successfully!")
    connection.close()

def update_task(task_id, **kwargs):
    # Function to update an existing Task
    connection = create_connection()

    # Generate the SET clause for the UPDATE query
    set_values = []

    for key, value in kwargs.items():
        if value is not None and value != "":
            set_values.append(f"{key} = '{value}'")
        else:
            set_values.append(f"{key} = {key}")  # Keep the field unchanged

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Task SET {set_clause} WHERE Task_ID = {task_id}"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Task with ID {task_id} updated successfully!")

    connection.close()

def delete_task(task_id):
    connection = create_connection()
    delete_task_query = f"DELETE FROM Task WHERE Task_ID = {task_id}"
    execute_query(connection, delete_task_query)
    st.success(f"Task with ID {task_id} deleted successfully!")
    connection.close()

def task_operations():
    st.subheader("Task Operations")

    # Add new Task form
    st.subheader("Add New Task")
    task_name = st.text_input("Task Name")
    task_description = st.text_input("Task Description")
    task_status = st.text_input("Task Status")
    task_priority = st.text_input("Task Priority")
    task_start_date = st.date_input("Task Start Date")
    task_end_date = st.date_input("Task End Date")
    sprint_id = st.text_input("Sprint ID (Optional)")
    attachment_id = st.text_input("Attachment ID (Optional)")
    add_button = st.button("Add Task", key="add_task")
    if add_button:
        add_task(task_name, task_description, task_status, task_priority, task_start_date, task_end_date, sprint_id, attachment_id)

    # Update existing Task form
    st.subheader("Update Task")
    # Form input for update
    task_id = st.text_input("Task ID")
    task_name_update = st.text_input("New Task Name (Optional)")
    task_description_update = st.text_input("New Task Description (Optional)")
    task_status_update = st.text_input("New Task Status (Optional)")
    task_priority_update = st.text_input("New Task Priority (Optional)")
    task_start_date_update = st.date_input("New Task Start Date (Optional)")
    task_end_date_update = st.date_input("New Task End Date (Optional)")
    sprint_id_update = st.text_input("New Sprint ID (Optional)")
    attachment_id_update = st.text_input("New Attachment ID (Optional)")

    # Submit button for update
    update_button = st.button("Update Task")
    if update_button:
        # Call the update_task function with the provided values
        update_task(task_id, Task_Name=task_name_update, Task_Description=task_description_update,
                    Task_Status=task_status_update, Task_Priority=task_priority_update,
                    Task_Start_Date=task_start_date_update, Task_End_Date=task_end_date_update,
                    Sprint_ID=sprint_id_update, Attachment_ID=attachment_id_update)

    # Delete Task form
    st.subheader("Delete Task")
    delete_task_id = st.text_input("Task ID to Delete")
    delete_button = st.button("Delete Task", key="delete_task")
    if delete_button:
        delete_task(delete_task_id)

def display_scrum_meeting_table():
    connection = create_connection()
    scrum_meetings = execute_select_query(connection, "SELECT * FROM Scrum_Meeting")
    connection.close()

    if scrum_meetings:
        st.subheader("Scrum Meeting Table")
        st.table(scrum_meetings)
    else:
        st.warning("No scrum meetings found in the database.")

def add_scrum_meeting(meeting_id, meeting_notes, meeting_date, sprint_id=None):
    connection = create_connection()

    # Convert None values to SQL NULL
    sprint_id = sprint_id if sprint_id is not None else "NULL"

    add_scrum_meeting_query = f"INSERT INTO Scrum_Meeting (Meeting_ID, Meeting_Notes, Meeting_Date, Sprint_ID) VALUES " \
                              f"({meeting_id}, '{meeting_notes}', '{meeting_date}', {sprint_id})"
    execute_query(connection, add_scrum_meeting_query)
    st.success("Scrum Meeting added successfully!")
    connection.close()

def update_scrum_meeting(meeting_id, **kwargs):
    connection = create_connection()

    # Generate the SET clause for the UPDATE query
    set_values = []

    for key, value in kwargs.items():
        if value is not None and value != "":
            set_values.append(f"{key} = '{value}'")
        else:
            set_values.append(f"{key} = {key}")  # Keep the field unchanged

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Scrum_Meeting SET {set_clause} WHERE Meeting_ID = {meeting_id}"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Scrum Meeting with ID {meeting_id} updated successfully!")

    connection.close()

def delete_scrum_meeting(meeting_id):
    connection = create_connection()
    delete_scrum_meeting_query = f"DELETE FROM Scrum_Meeting WHERE Meeting_ID = {meeting_id}"
    execute_query(connection, delete_scrum_meeting_query)
    st.success(f"Scrum Meeting with ID {meeting_id} deleted successfully!")
    connection.close()

def scrum_meeting_operations():
    st.subheader("Scrum Meeting Operations")

    # Add new Scrum Meeting form
    st.subheader("Add New Scrum Meeting")
    meeting_id = st.text_input("Meeting ID")
    meeting_notes = st.text_input("Meeting Notes")
    meeting_date = st.date_input("Meeting Date")
    sprint_id = st.text_input("Sprint ID (Optional)")
    add_button = st.button("Add Scrum Meeting", key="add_scrum_meeting")
    if add_button:
        add_scrum_meeting(meeting_id, meeting_notes, meeting_date, sprint_id)

    # Update existing Scrum Meeting form
    st.subheader("Update Scrum Meeting")
    # Form input for update
    update_scrum_meeting_id = st.text_input("Meeting ID to Update")
    meeting_notes_update = st.text_input("New Meeting Notes (Optional)")
    meeting_date_update = st.date_input("New Meeting Date (Optional)")
    sprint_id_update = st.text_input("New Sprint ID (Optional)")

    # Submit button for update
    update_button = st.button("Update Scrum Meeting")
    if update_button:
        # Call the update_scrum_meeting function with the provided values
        update_scrum_meeting(update_scrum_meeting_id, Meeting_Notes=meeting_notes_update,
                              Meeting_Date=meeting_date_update, Sprint_ID=sprint_id_update)

    # Delete Scrum Meeting form
    st.subheader("Delete Scrum Meeting")
    delete_scrum_meeting_id = st.text_input("Meeting ID to Delete")
    delete_button = st.button("Delete Scrum Meeting", key="delete_scrum_meeting")
    if delete_button:
        delete_scrum_meeting(delete_scrum_meeting_id)

def display_retrospective_meeting_table():
    connection = create_connection()
    retrospective_meetings = execute_select_query(connection, "SELECT * FROM Retrospective_Meeting")
    connection.close()

    if retrospective_meetings:
        st.subheader("Retrospective Meeting Table")
        st.table(retrospective_meetings)
    else:
        st.warning("No retrospective meetings found in the database.")

def add_retrospective_meeting(meeting_id, meeting_notes, meeting_date, sprint_id=None):
    connection = create_connection()

    # Convert None values to SQL NULL
    sprint_id = sprint_id if sprint_id is not None else "NULL"

    add_retrospective_meeting_query = f"INSERT INTO Retrospective_Meeting (Meeting_ID, Meeting_Notes, Meeting_Date, Sprint_ID) VALUES " \
                                      f"({meeting_id}, '{meeting_notes}', '{meeting_date}', {sprint_id})"
    execute_query(connection, add_retrospective_meeting_query)
    st.success("Retrospective Meeting added successfully!")
    connection.close()

def update_retrospective_meeting(meeting_id, **kwargs):
    connection = create_connection()

    # Generate the SET clause for the UPDATE query
    set_values = []

    for key, value in kwargs.items():
        if value is not None and value != "":
            set_values.append(f"{key} = '{value}'")
        else:
            set_values.append(f"{key} = {key}")  # Keep the field unchanged

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Retrospective_Meeting SET {set_clause} WHERE Meeting_ID = {meeting_id}"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Retrospective Meeting with ID {meeting_id} updated successfully!")

    connection.close()

def delete_retrospective_meeting(meeting_id):
    connection = create_connection()
    delete_retrospective_meeting_query = f"DELETE FROM Retrospective_Meeting WHERE Meeting_ID = {meeting_id}"
    execute_query(connection, delete_retrospective_meeting_query)
    st.success(f"Retrospective Meeting with ID {meeting_id} deleted successfully!")
    connection.close()

def retrospective_meeting_operations():
    st.subheader("Retrospective Meeting Operations")

    # Add new Retrospective Meeting form
    st.subheader("Add New Retrospective Meeting")
    meeting_id = st.text_input("Meeting ID")
    meeting_notes = st.text_input("Meeting Notes")
    meeting_date = st.date_input("Meeting Date")
    sprint_id = st.text_input("Sprint ID (Optional)")
    add_button = st.button("Add Retrospective Meeting", key="add_retrospective_meeting")
    if add_button:
        add_retrospective_meeting(meeting_id, meeting_notes, meeting_date, sprint_id)

    # Update existing Retrospective Meeting form
    st.subheader("Update Retrospective Meeting")
    # Form input for update
    update_retrospective_meeting_id = st.text_input("Meeting ID to Update")
    meeting_notes_update = st.text_input("New Meeting Notes (Optional)")
    meeting_date_update = st.date_input("New Meeting Date (Optional)")
    sprint_id_update = st.text_input("New Sprint ID (Optional)")

    # Submit button for update
    update_button = st.button("Update Retrospective Meeting")
    if update_button:
        # Call the update_retrospective_meeting function with the provided values
        update_retrospective_meeting(update_retrospective_meeting_id, Meeting_Notes=meeting_notes_update,
                                      Meeting_Date=meeting_date_update, Sprint_ID=sprint_id_update)

    # Delete Retrospective Meeting form
    st.subheader("Delete Retrospective Meeting")
    delete_retrospective_meeting_id = st.text_input("Meeting ID to Delete")
    delete_button = st.button("Delete Retrospective Meeting", key="delete_retrospective_meeting")
    if delete_button:
        delete_retrospective_meeting(delete_retrospective_meeting_id)

def display_comments_table():
    connection = create_connection()
    comments = execute_select_query(connection, "SELECT * FROM Comments")
    connection.close()

    if comments:
        st.subheader("Comments Table")
        st.table(comments)
    else:
        st.warning("No comments found in the database.")

def add_comment(comment_task, comment_timestamp, comment_task_id=None):
    connection = create_connection()

    # Convert None values to SQL NULL
    comment_task_id = comment_task_id if comment_task_id is not None else "NULL"

    add_comment_query = f"INSERT INTO Comments (Comment_Task, Comment_Timestamp, Comment_Task_ID) VALUES " \
                        f"('{comment_task}', '{comment_timestamp}', {comment_task_id})"
    execute_query(connection, add_comment_query)
    st.success("Comment added successfully!")
    connection.close()

def update_comment(comment_id, **kwargs):
    connection = create_connection()

    # Generate the SET clause for the UPDATE query
    set_values = []

    for key, value in kwargs.items():
        if value is not None and value != "":
            set_values.append(f"{key} = '{value}'")
        else:
            set_values.append(f"{key} = {key}")  # Keep the field unchanged

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Comments SET {set_clause} WHERE Comment_ID = {comment_id}"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Comment with ID {comment_id} updated successfully!")

    connection.close()

def delete_comment(comment_id):
    connection = create_connection()
    delete_comment_query = f"DELETE FROM Comments WHERE Comment_ID = {comment_id}"
    execute_query(connection, delete_comment_query)
    st.success(f"Comment with ID {comment_id} deleted successfully!")
    connection.close()

def comments_operations():
    st.subheader("Comments Operations")

    # Add new Comment form
    st.subheader("Add New Comment")
    comment_task = st.text_input("Comment Task")
    comment_timestamp = st.date_input("Comment Timestamp")
    comment_task_id = st.text_input("Comment Task ID (Optional)")
    add_button = st.button("Add Comment", key="add_comment")
    if add_button:
        add_comment(comment_task, comment_timestamp, comment_task_id)

    # Update existing Comment form
    st.subheader("Update Comment")
    # Form input for update
    update_comment_id = st.text_input("Comment ID to Update")
    comment_task_update = st.text_input("New Comment Task (Optional)")
    comment_timestamp_update = st.date_input("New Comment Timestamp (Optional)")
    comment_task_id_update = st.text_input("New Comment Task ID (Optional)")

    # Submit button for update
    update_button = st.button("Update Comment")
    if update_button:
        # Call the update_comment function with the provided values
        update_comment(update_comment_id, Comment_Task=comment_task_update,
                       Comment_Timestamp=comment_timestamp_update, Comment_Task_ID=comment_task_id_update)

    # Delete Comment form
    st.subheader("Delete Comment")
    delete_comment_id = st.text_input("Comment ID to Delete")
    delete_button = st.button("Delete Comment", key="delete_comment")
    if delete_button:
        delete_comment(delete_comment_id)

def display_phone_number_table():
    connection = create_connection()
    phone_numbers = execute_select_query(connection, "SELECT * FROM Phone_Number")
    connection.close()

    if phone_numbers:
        st.subheader("Phone Number Table")
        st.table(phone_numbers)
    else:
        st.warning("No phone numbers found in the database.")

def add_phone_number(phone_number, user_id=None):
    connection = create_connection()

    # Convert None values to SQL NULL
    user_id = user_id if user_id is not None else "NULL"

    add_phone_number_query = f"INSERT INTO Phone_Number (Phone_Number, USER_ID) VALUES " \
                             f"('{phone_number}', {user_id})"
    execute_query(connection, add_phone_number_query)
    st.success("Phone Number added successfully!")
    connection.close()

def update_phone_number(phone_number, user_id=None):
    connection = create_connection()

    # Generate the SET clause for the UPDATE query
    set_values = []

    if user_id is not None:
        set_values.append(f"USER_ID = {user_id}")

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Phone_Number SET {set_clause} WHERE Phone_Number = '{phone_number}'"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Phone Number {phone_number} updated successfully!")

    connection.close()

def delete_phone_number(phone_number):
    connection = create_connection()
    delete_phone_number_query = f"DELETE FROM Phone_Number WHERE Phone_Number = '{phone_number}'"
    execute_query(connection, delete_phone_number_query)
    st.success(f"Phone Number {phone_number} deleted successfully!")
    connection.close()

def phone_number_operations():
    st.subheader("Phone Number Operations")

    # Add new Phone Number form
    st.subheader("Add New Phone Number")
    phone_number = st.text_input("Phone Number")
    user_id = st.text_input("User ID (Optional)")
    add_button = st.button("Add Phone Number", key="add_phone_number")
    if add_button:
        add_phone_number(phone_number, user_id)

    # Update existing Phone Number form
    st.subheader("Update Phone Number")
    # Form input for update
    phone_number_update = st.text_input("Phone Number to Update")
    user_id_update = st.text_input("New User ID (Optional)")

    # Submit button for update
    update_button = st.button("Update Phone Number")
    if update_button:
        # Call the update_phone_number function with the provided values
        update_phone_number(phone_number_update, user_id_update)

    # Delete Phone Number form
    st.subheader("Delete Phone Number")
    delete_phone_number_value = st.text_input("Phone Number to Delete")
    delete_button = st.button("Delete Phone Number", key="delete_phone_number")
    if delete_button:
        delete_phone_number(delete_phone_number_value)

def display_acceptance_criteria_table():
    connection = create_connection()
    acceptance_criteria = execute_select_query(connection, "SELECT * FROM Acceptance_Criteria")
    connection.close()

    if acceptance_criteria:
        st.subheader("Acceptance Criteria Table")
        st.table(acceptance_criteria)
    else:
        st.warning("No acceptance criteria found in the database.")

def add_acceptance_criteria(description, story_id=None):
    connection = create_connection()

    # Convert None values to SQL NULL
    story_id = story_id if story_id is not None else "NULL"

    add_acceptance_criteria_query = f"INSERT INTO Acceptance_Criteria (Acceptance_Criteria_Description, Acceptance_Story_ID) VALUES " \
                                     f"('{description}', {story_id})"
    execute_query(connection, add_acceptance_criteria_query)
    st.success("Acceptance Criteria added successfully!")
    connection.close()

def update_acceptance_criteria(description, story_id=None):
    connection = create_connection()

    # Generate the SET clause for the UPDATE query
    set_values = []

    if story_id is not None:
        set_values.append(f"Acceptance_Story_ID = {story_id}")

    set_clause = ", ".join(set_values)

    # Construct the UPDATE query
    update_query = f"UPDATE Acceptance_Criteria SET {set_clause} WHERE Acceptance_Criteria_Description = '{description}'"

    # Execute the UPDATE query
    execute_query(connection, update_query)

    st.success(f"Acceptance Criteria {description} updated successfully!")

    connection.close()

def delete_acceptance_criteria(description):
    connection = create_connection()
    delete_acceptance_criteria_query = f"DELETE FROM Acceptance_Criteria WHERE Acceptance_Criteria_Description = '{description}'"
    execute_query(connection, delete_acceptance_criteria_query)
    st.success(f"Acceptance Criteria {description} deleted successfully!")
    connection.close()

def acceptance_criteria_operations():
    st.subheader("Acceptance Criteria Operations")

    # Add new Acceptance Criteria form
    st.subheader("Add New Acceptance Criteria")
    description = st.text_input("Acceptance Criteria Description")
    story_id = st.text_input("Story ID (Optional)")
    add_button = st.button("Add Acceptance Criteria", key="add_acceptance_criteria")
    if add_button:
        add_acceptance_criteria(description, story_id)

    # Update existing Acceptance Criteria form
    st.subheader("Update Acceptance Criteria")
    # Form input for update
    description_update = st.text_input("Acceptance Criteria to Update")
    story_id_update = st.text_input("New Story ID (Optional)")

    # Submit button for update
    update_button = st.button("Update Acceptance Criteria")
    if update_button:
        # Call the update_acceptance_criteria function with the provided values
        update_acceptance_criteria(description_update, story_id_update)

    # Delete Acceptance Criteria form
    st.subheader("Delete Acceptance Criteria")
    delete_acceptance_criteria_value = st.text_input("Acceptance Criteria to Delete")
    delete_button = st.button("Delete Acceptance Criteria", key="delete_acceptance_criteria")
    if delete_button:
        delete_acceptance_criteria(delete_acceptance_criteria_value)

def main():

    pages = ["Home", "Signup", "Login", "Users", "Admins"]
    page = st.sidebar.radio("Select Page", pages)

    if page == "Home":
        home_page()

    elif page == "Signup":
        st.title("Sign Up")

        name = st.text_input("Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.text_input("Role")
        sprint_id = st.text_input("Sprint ID (Optional)")

        signup_button = st.button("Sign Up")

        if signup_button:
            handle_signup(name, username, password, role, sprint_id)

    elif page == "Login":
        login()

    elif page == "Users":
        user_page()

    elif page == "Admins":
        admin_page()

if __name__ == "__main__":
    main()