from flask import Flask
from routes.ussd_routes import ussd_callback, index, test_db

app = Flask(__name__)

# Registering Routes
app.add_url_rule('/', 'index', index)
app.add_url_rule('/test_db', 'test_db', test_db)
app.add_url_rule('/ussd', 'ussd_callback', ussd_callback, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
