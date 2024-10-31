import datetime
# from database.db_operations import connect_db

# Function to save feedback and all POST data sent by AT
def save_feedback(session_id, service_code, phone_number, text, project_id, message, status, sentiments, urgency):
    from database.db_operations import connect_db  # Move the import here

    conn = connect_db()
    if conn:
        try:
            conn.set_session(autocommit=True)
            cur = conn.cursor()

            # Insert the feedback into the database
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

            print("Data insertion successful!")
            cur.close()
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

# Function to update the sentiment aggregate table
def update_sentiment_aggregate(project_id, sentiment):
    from database.db_operations import connect_db  # Move the import here

    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Log the project ID and sentiment for debugging purposes
            print(f"Updating sentiment aggregation for project_id: {project_id} with sentiment: {sentiment}")

            # Step 1: Check if the project_id already exists in sentiment_aggregations
            cur.execute("SELECT positive, negative, total FROM sentiments_aggregations WHERE project_id = %s", (project_id,))
            result = cur.fetchone()

            # Log the result of the query to see if the project exists in the table
            print(f"Sentiments aggregation query result for project_id {project_id}: {result}")

            if result:
                # Project exists, update the counts based on the sentiment
                positive, negative, total = result

                if sentiment == 1:  # Positive sentiment
                    positive += 1
                elif sentiment == 0:  # Negative sentiment
                    negative += 1
                else:
                    print(f"Unknown sentiment value: {sentiment}")
                    return  # Early exit in case of unexpected sentiment

                total += 1

                # Log the updated counts before executing the query
                print(f"Updating sentiment counts for project_id {project_id}: positive={positive}, negative={negative}, total={total}")

                # Update the sentiment_aggregations table with the new values
                update_query = """
                UPDATE sentiments_aggregations
                SET positive = %s, negative = %s, total = %s, last_updated = %s
                WHERE project_id = %s
                """
                cur.execute(update_query, (
                    positive, negative, total, datetime.datetime.now(), project_id
                ))
                print(f"Updated sentiments aggregation for project_id {project_id}")

            else:
                # Project does not exist, insert a new row
                print(f"Inserting new sentiment record for project_id: {project_id}")

                insert_query = """
                INSERT INTO sentiments_aggregations (project_id, positive, negative, total, last_updated)
                VALUES (%s, %s, %s, %s, %s)
                """
                if sentiment == 1:
                    cur.execute(insert_query, (project_id, 1, 0, 1, datetime.datetime.now()))
                elif sentiment == 0:
                    cur.execute(insert_query, (project_id, 0, 1, 1, datetime.datetime.now()))

                print(f"Inserted new sentiment record for project_id {project_id}")

            conn.commit()  # Commit the transaction
            cur.close()

        except Exception as e:
            print(f"Error updating sentiment aggregate for project_id {project_id}: {e}")
        finally:
            conn.close()
    else:
        print(f"Failed to connect to the database while updating sentiment aggregation for project_id {project_id}")



# Save feedback and update sentiment aggregation
def save_feedback(session_id, service_code, phone_number, text, project_id, message, status, sentiments, urgency):
    from database.db_operations import connect_db  # Move the import here

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

