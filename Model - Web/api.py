from flask import Flask, jsonify, request
import psycopg2
import pandas as pd

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    """Establish a database connection."""
    return psycopg2.connect(**DB_CONFIG)

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """API endpoint to retrieve all projects."""
    conn = get_db_connection()
    query = "SELECT id, name FROM projects"
    df = pd.read_sql(query, conn)
    conn.close()
    
    projects = [{"label": row["name"], "value": row["id"]} for _, row in df.iterrows()]
    return jsonify(projects)

@app.route('/api/sentiment', methods=['GET'])
def get_sentiment_data():
    """API endpoint to retrieve sentiment data."""
    project_ids = request.args.getlist('project_ids', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = get_db_connection()

    # Update the query with dynamic filtering and ensure that `project_ids` is handled correctly
    query = """
        SELECT 
            s.project_id,
            p.name AS project_name,
            s.positive,
            s.negative,
            s.total AS feedback,
            s.last_updated AS timestamp
        FROM sentiments_aggregations s
        JOIN projects p ON s.project_id = p.id
        WHERE (%s = '{}' OR s.project_id = ANY(%s))
        AND (%s IS NULL OR s.last_updated >= %s)
        AND (%s IS NULL OR s.last_updated <= %s)
    """
    
    params = (project_ids, project_ids, start_date, start_date, end_date, end_date)
    
    # Run the query with the specified parameters
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    
    # Check if the data frame has valid values for positive, negative, and total counts
    if not df.empty:
        # Transform data to include 'sentiment' column
        df_positive = df[['project_id', 'project_name', 'feedback', 'timestamp']].copy()
        df_positive['sentiment'] = 'positive'
        df_positive['count'] = df['positive']

        df_negative = df[['project_id', 'project_name', 'feedback', 'timestamp']].copy()
        df_negative['sentiment'] = 'negative'
        df_negative['count'] = df['negative']

        # Combine positive and negative data
        df_combined = pd.concat([df_positive, df_negative], ignore_index=True)
    else:
        # If no data, return an empty list
        df_combined = pd.DataFrame(columns=['project_id', 'project_name', 'feedback', 'timestamp', 'sentiment', 'count'])
    
    response_data = df_combined.to_dict(orient="records")
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
