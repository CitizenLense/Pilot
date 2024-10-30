import datetime
import psycopg2
from config import DATABASE_CONFIG
from utils.helper import update_sentiment_aggregate
# Function to connect to the database
def connect_db():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Function to fetch projects
def get_projects():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM projects WHERE location = 'Mathare'")
            projects = cur.fetchall()
            cur.close()
            return projects
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return None
        finally:
            conn.close()
    return None

# Add other database-related functions here (e.g., saving feedback, updating sentiment)

def save_feedback(session_id, service_code, phone_number, text, project_id, message, status, sentiments, urgency):
    conn = connect_db()
    if conn:
        try:
            conn.set_session(autocommit=True)
            cur = conn.cursor()

            # Insert feedback into the database
            insert_query = """
                INSERT INTO ussd_message (
                    session_id, service_code, user_phone, text_input, project_id, 
                    message, status, sentiments, urgency, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, (
                session_id,
                service_code,
                phone_number,
                text,
                project_id,
                message,
                status,
                sentiments,
                urgency,
                datetime.datetime.now()
            ))

            # Now that feedback is saved, update the sentiment aggregation
            update_sentiment_aggregate(project_id, sentiments)

            print("Data insertion and sentiment aggregation update successful!")
            cur.close()
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database while saving feedback.")

