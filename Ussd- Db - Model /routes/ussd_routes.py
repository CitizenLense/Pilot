from flask import request, Response
from database.db_operations import connect_db, get_projects
from utils.helper import save_feedback
from models.sentiment_model import predict_sentiment

# Default route for testing
def index():
    return "USSD API is running."

# Test the database connection
def test_db():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM projects;")
            projects = cur.fetchall()
            cur.close()
            return f"Projects: {projects}"
        except Exception as e:
            return f"Error: {e}"
        finally:
            conn.close()
    return "Failed to connect to the database."

# USSD endpoint
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    # Split the input based on '*' to follow menu progress
    user_input = text.split('*')
    response = ""

    if text == '':
        # Main Menu
        response = "CON Welcome to CitizenLens!\n"
        response += "1. Share Your Thoughts on CDF Projects\n"
        response += "2. Learn More About CitizenLens\n"
        response += "3. Exit"

    elif user_input[0] == '1':
        # Step 1: Select Constituency (only showing Mathare)
        if len(user_input) == 1:
            response = "CON Select Your Constituency\n"
            response += "1. Mathare\n"
        
        # Step 2: Select a Project (Dynamic based on database)
        elif len(user_input) == 2:
            if user_input[1] == '1':  # Mathare selected
                projects = get_projects()
                if projects:
                    response = "CON Select a Project:\n"
                    for index, project in enumerate(projects):
                        response += f"{index + 1}. {project[1]}\n"
                else:
                    response = "END No projects available for Mathare at the moment.\n"
        
        # Step 3: Select Project State
        elif len(user_input) == 3:
            response = "CON What is the current state of the project?\n"
            response += "1. Completed\n"
            response += "2. In Progress\n"
            response += "3. Stalled\n"
            response += "4. Never Started\n"
        
        # Step 4: How has this project impacted the community?
        elif len(user_input) == 4:
            response = "CON How has this project impacted your community? (Short answer)\n"
        
        # Step 5: Biggest Issue with the Project
        elif len(user_input) == 5:
            response = "CON What is the biggest issue with this project?\n"
            response += "1. Poor workmanship\n"
            response += "2. Lack of funds\n"
            response += "3. Poor planning\n"
            response += "4. Corruption/mismanagement\n"
            response += "5. Other (Type your response)\n"
        
        # Step 6: How Urgent is the Completion of this Project?
        elif len(user_input) == 6:
            response = "CON How urgent is the completion of this project?\n"
            response += "1. Extremely Urgent\n"
            response += "2. Urgent\n"
            response += "3. Not Urgent\n"
        
        # Final Step: Confirmation and Save Data
        elif len(user_input) == 7:
            project_id = int(user_input[2])  # Get project ID from step 2
            project_state = user_input[3]
            impact_feedback = user_input[4]
            biggest_issue = user_input[5]
            urgency = user_input[6]

            # Debug information before saving feedback
            print("Before saving feedback:")
            print("Phone number:", phone_number)
            print("Project ID:", project_id)
            print("Impact Feedback:", impact_feedback)
            print("Biggest Issue:", biggest_issue)
            print("Urgency:", urgency)

            # **Sentiment Analysis**: Call predict_sentiment to get sentiment label
            sentiments = predict_sentiment(impact_feedback)

            # Save feedback in the database
            save_feedback(
                session_id, service_code, phone_number, text, 
                project_id, impact_feedback, biggest_issue, sentiments, urgency
            )

            response = "END Thank you for your feedback! Your input will help us push for transparency and accountability in CDF projects."

    elif text == '2':
        response = "END CitizenLens helps you give feedback on community projects and ensures transparency in how CDF funds are used."

    elif text == '3':
        response = "END Thank you for using our service."

    else:
        response = "END Invalid input. Please try again."

    return Response(response, mimetype="text/plain")
