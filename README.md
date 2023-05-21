# Spheroid_AI_Chatbot
Spheroid is a conversational AI chatbot implemented in Python that provides various functionalities  like  appointment scheduling-risk factor analysis, discharge planning and extracts data for the useful insights to make data-driven decisions, and as it interacts with users through GUI it provides effiective response through by ML algorithms.

## Intent and Entity Recognition Using NLP
This code provides a basic natural language processing (NLP) functionality using the NLTK (Natural Language Toolkit) library.

The ‘intents’ dictionary contains predefined intents and their associated patterns.

- The ‘pre-process’ function tokenizes, removes stop words and punctuation, and lemmatizes a given sentence.

- The ‘predict_intent’ function takes a sentence, pre-processes it, and matches it against the predefined patterns for each intent to predict the most suitable intent.
- To add new intents or modify existing ones, update the ‘intents ’dictionary with the desired patterns and associated intent labels.
-	The ‘nlp’ function takes a query as input for entity recognition
-	It tokenizes the query into words using ‘word_tokenize’ from NLTK.
-	It tags the words with their part of speech using ‘pos_tag’ from NLTK.
-	It identifies named entities using ‘ne_chunk’ from NLTK, which utilizes a pre-trained classifier.
-	The function returns the label and the entity text for each identified named entity.

## Risk Analysis

This code provides how the chatbot utilizes natural language processing and provides risk analysis based on user-provided information. It uses the scikit-learn library for machine learning tasks. Where use Support vector machine algorithm to predict the output using the data.

## Discharge Planning
The chatbot assists with discharge planning for patients and provides recommendations based on their information. It uses the scikit-learn library for machine learning tasks where we use logistic regression algorithm to predict the output for the user based upon data and program interacts with a MySQL database for data storage.

## Functionalities
The AI chatbot offers the following functionalities:

#### Greeting: 

The chatbot can greet the user and initiate a conversation.

#### Appointment Booking:   
Users can schedule appointments with doctors by providing their details, such as name, age, gender, medical history, insurance number, date, and time.

#### Risk Analysis:  
Users can provide their personal information, such as name, age, gender, and medical history. The chatbot uses a Support Vector Machine (SVM) model to predict potential risk factors based on the provided data.

#### Discharge Planning: 
 User can provide their personal and medical information, including name, age, gender, diagnosed medical history, length of stay, insurance type, and residence. The chatbot uses a logistic regression model to predict the likelihood of readmission based on the provided data. It then provides discharge recommendations based on the predicted probability.

#### Web Search: 

The chatbot can perform a Google search based on user queries.

#### Website Launch:

The chatbot can open websites based on user requests.

#### General Conversations:
 The chatbot can engage in general conversations and respond to common queries.

## Dependencies
The following dependencies are required to run the code:

●	SpeechRecognition (`pip install speechrecognition`)

●	pyAudio (required for speech recognition)

●	scikit-learn (`pip install scikit-learn`)

●	pyttsx3 (`pip install pyttsx3`)

●	pandas (`pip install pandas`)

●	urllib (built-in library)

●	webbrowser (built-in library)

●	tkinter (built-in library)

●	mysql-connector-python (`pip install mysql-connector-python`)

## Setup
 Install the required dependencies using :
 ```python 
 pip install SpeechRecognition 
 pip install pandas 
 pip install mysql-connector
 pip install  tkinter
 ```

 Set up the local database connection by providing the necessary credentials in the code.

## Usage
- Clone the repository: 
  git clone https://github.com/your_username/your_repository.git
   
- Install the required dependencies as mentioned above.
- Ensure the NLTK library is installed (`nltk` package)
- Import the necessary libraries: `nltk`, `string`, `WordNetLemmatizer` from `nltk.stem`, `stopwords` from `nltk.corpus`, `word_tokenize` from `nltk.tokenize`, `pos_tag` from `nltk.tag`, and `ne_chunk` from `nltk.chunk`.
- Define the intents in the `intents` dictionary, associating patterns with intent labels.
- Use the `predict_intent` function to predict the intent for a given sentence.
- Use the `nlp` function to perform named entity recognition on a query and obtain the identified entities.
- Prepare the input data:  
-	Create a CSV file named `patient_data.csv` containing the patient data with columns: `Age`, `Gender`, `Medical_History`, and `Risk_Factor`.
-	 Ensure the CSV file is in the same directory as the code file.\

- Make sure to configure the database connection before running the code. Modify the following lines of code to match your MySQL database configuration:
```python 
conn = mysql.connector.connect(host='localhost', user='root', password=*****', database='spheroid_db')
```
-  Run the code: ```python Spheroid.py ```

-  The chatbot GUI will open, allowing you to interact with the chatbot.
-	You can type your queries in the input field and click the "Send" button to receive responses.
-	Alternatively, you can click the "Speak" button and provide input via speech. Make sure your microphone is connected and working correctly.
-	Enter the patient's information in the input fields.
-	Click the "Analyze" button to perform risk analysis.
-	The chatbot will display the identified potential risk factors.
-	Enter the patient's information in the input fields.-●	Click the "Submit" button to perform discharge planning and get recommendations.
-	The chatbot will display the recommended actions based on the predicted likelihood of readmission.
- Follow the prompts and instructions provided by the chatbot to use its various features.

## Notes

-	This chatbot is a work in progress and may have limitations or known issues.
-	The risk analysis uses a Support Vector Machine (SVM) model for risk analysis. Make sure the `patient_data.csv` file is correctly formatted with appropriate columns and data.
-	The chatbot interface is implemented using the tkinter library. Ensure your system supports tkinter for graphical user interface (GUI) rendering.
-	The discharge planning code uses a logistic regression model for predicting the likelihood of readmission. Make sure the `patient_data.csv` file is correctly formatted with appropriate columns and data.
-	The chatbot interface is implemented using the tkinter library. Ensure your system supports tkinter for graphical user interface (GUI) rendering.
-	The Spheroid code  uses the SpeechRecognition library, which requires pyaudio for speech recognition. Depending on your system, you may need to install pyaudio manually before running the code.
-	 The risk factor analysis and discharge planning features are still under development and may not provide comprehensive or accurate results at this stage.

#### Please feel free to contribute to this project and enhance its functionalities.
