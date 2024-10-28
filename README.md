CitizenLens: CDF Project Feedback System 

CITIZENLENS is a sentiment analysis project. It allows users to view the sentiments of a constituency based on the completion of CDF projects. After receiving input from users through a USSD code:
		
	  * 789 *9085635#
This input is taken through a sentiment analysis model that processes the text data and outputs the result of the analyzed sentiment into a webpage. 

The authors are: 

Rachael Kibicho 
rachaelkibicho@gmail.com 

George Karanja
gkkaranja2@gmail.com

Angela Kinoro
angela.kinoro@riarauniversity.ac.keq




  
PROJECT STRUCTURE   USSD ->  MODEL -> WEBPAGE


	PROJECT STRUCTURE 
	
	project/
	│
	├── webpage                        # The main file to run your Flask app
  |         ___ app.py       
	├── models/                        # Directory for machine learning models	
	          └── sentiment_model.py   # Sentiment prediction logic	
	├── database/                      # Directory for database-related operations	
	          └── db_operations.py     # Database connection and queries	
	          └── db_script.sql        # Database connection and queries	
            ___ config.py
	├── routes/                        # Directory for Flask route handlers	
	          └── ussd_routes.py       # USSD routes	
	└── utils/                         # Utility functions	
	          └── helpers.py   
	

     
FEATURES

	- USSD Integration: Allows users to share feedback via USSD.
	- Database: Uses PostgreSQL to store project details and user feedback.
	- Sentiment Analysis: Leverages a fine-tuned DistilBERT model to analyze the sentiment of feedback.
	- Dynamic Menus: Provides a USSD menu where users select constituency, project, project state, and urgency.
	- Webpage that displays aggregated sentiments for particular projects
	


GETTING STARTED
Prerequisites

Make sure you have the following installed:

	- Python 3.8+	
	- PostgreSQL
	- Ngrok (for exposing your local server to the internet, used for USSD callbacks)	
	- A virtual environment (recommended)
	



INSTALLATION

	1. Clone the Repository
	First, clone this repository to your local machine: git clone https://github.com/angelakinoro/KamiLimu-Sentiment_Analysis
	
	2. Navigate into the project directory: cd project
	Create a Virtual Environment:
		python3 -m venv venv
	# linux  source venv/bin/activate    # On Windows use: venv\Scripts\activate
 
	3. Install the Required Dependencies: pip install -r requirements.txt
 
	4. Database Setup
	Set Up PostgreSQL: Ensure you have PostgreSQL running and properly configured with the necessary databases and tables. 
	Create the required tables (Find the schema in the folder database/ db_script.sql):


RUNNING THE APPLCATION 


	- Start the Flask App: python app.py
	The app should now be running on http://127.0.0.1:5000.	
	- Expose to the Internet (for USSD):
	Use Ngrok to expose the local server: ngrok http 5000
	Take note of the Ngrok URL (e.g., http://<ngrok-id>.ngrok.io) and update your USSD service provider's callback URL to point to http://<ngrok-id>.ngrok.io/ussd.	
	- Interacting with the Application
	USSD Menu: Dial the USSD code to interact with the system. You will be prompted to provide feedback about CDF projects in your constituency.
	Feedback Storage: User feedback will be saved in the PostgreSQL database, and the system will perform sentiment analysis using the pre-trained DistilBERT model.

FOR THE WEBPAGE 

	Tailwind + React Project with Vite
	Ensure Dependencies are Installed: cretae a virtual environment (.venv), make sure you have all the required Node.js packages installed.
		
	Run: npm install
	This will ensure that all dependencies and devDependencies listed in package.json are installed locally in the node_modules directory.
	
	Run the Development Server: Now that the dependencies are installed, you can start the development server using the command in the scripts section of your package.json:
	
	npm run dev
	This should start the Vite development server and compile your React and Tailwind CSS code.
	
	Check the Console Output: After running the command, the console will give you the local URL where your app is being served, likely something like:
	Local: http://localhost:5173/

Model Information

	This project uses a fine-tuned DistilBERT model to predict the sentiment of feedback messages. The model is loaded from the models/sentiment_model.py file.
	 Here is the google colab notebook when finetuning the model: https://colab.research.google.com/drive/15aNMyVkEStg-lBtjcFtBqE4I5RJ-N4zK?authuser=1
 


Contributing: 
If you'd like to contribute to this project, please open a pull request or contact either of us.

License: 
This project is licensed under the MIT License.

Slides: 
https://www.canva.com/design/DAGQNMhJrT4/xdDyT0q-Lix4_FLIKvMV4A/edit?utm_content=DAGQNMhJrT4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
