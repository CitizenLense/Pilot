
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_mock_data(num_entries=100):
    """Generate a DataFrame with mock sentiment data, including project names."""
    # Example project data
    project_data = {
        1: "Health Clinic Renovation",
        2: "School Building Construction",
        3: "Road Improvement Project"
    }
    
    sentiments = ['positive', 'negative']
    feedback_examples = [
        "Great improvement!", "Needs more work", "Very useful project", 
        "Waste of funds", "Highly appreciated", "Not satisfied with the progress"
    ]
    
    data = {
        "project_id": [random.choice(list(project_data.keys())) for _ in range(num_entries)],
        "sentiment": [random.choice(sentiments) for _ in range(num_entries)],
        "feedback": [random.choice(feedback_examples) for _ in range(num_entries)],
        "timestamp": [
            datetime.now() - timedelta(days=random.randint(0, 30)) for _ in range(num_entries)
        ]
    }
    
    df = pd.DataFrame(data)
    df['project_name'] = df['project_id'].map(project_data)  # Map project names
    return df

# Generate and store mock data
mock_data = generate_mock_data()
