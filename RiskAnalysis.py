
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import pyttsx3
import tkinter as tk

Asst = pyttsx3.init("sapi5")
voices = Asst.getProperty("voices")

Asst.setProperty("voices", voices[1].id)
Asst.setProperty("rate", 170)

user_spoke = False

Asst.setProperty("voices", voices[1].id)
Asst.setProperty("rate", 170)

user_spoke = False

def Speak(audio):
    Asst.say(audio)
    Asst.runAndWait()


def RiskAnalysis_predict(name_db, Age_db, Gender_db, Medical_History_db,conversation,user_spoke):

    patient_data = pd.read_csv(
        r'C:\Users\***PATH***\patient_data.csv')

# Preprocess the data
    le = LabelEncoder()
    # print(patient_data)
    patient_data['Gender'] = le.fit_transform(patient_data['Gender'])
    # print(patient_data)

# Identify and encode the categories for Medical_History
    medical_history_categories = patient_data['Medical_History'].unique()
    # print(medical_history_categories)
    le_medical_history = LabelEncoder()
    le_medical_history.fit(medical_history_categories)
    # print(patient_data)
    patient_data['Medical_History'] = le_medical_history.transform(
        patient_data['Medical_History'])
    # print(patient_data)
    scaler = StandardScaler()
# feature_names = ['Age', 'Gender', 'Medical_History']
    patient_data[['Age', 'Medical_History']] = scaler.fit_transform(
        patient_data[['Age', 'Medical_History']])

# Train an SVM model to predict risk factors
    X = patient_data[['Age', 'Gender', 'Medical_History']]
    y = patient_data['Risk_Factor']

    svm = SVC(kernel='linear', C=1.0, random_state=42)
# svm.fit(X, y,feature_names=feature_names)

    svm.fit(X, y)
    Medical_History_encoded = le_medical_history.transform([Medical_History_db])[
            0]
    gender_encoded = le.transform([Gender_db])[0]
    age_scaled = scaler.transform([[Age_db, Medical_History_encoded]])[0]
    risk_factor = svm.predict(
            [[age_scaled[0], gender_encoded, age_scaled[1]]])
    res = "Thank you for registering. Based on your medical history, we have identified the following potential risk factors:" + str(risk_factor)
    displaybotmsg(res,conversation,user_spoke)
    
def displaybotmsg(bot_response,conversation,user_spoke):
    # create new message frame for bot response
    if(user_spoke):
        Speak(bot_response)
        user_spoke = False
    bot_message_frame = tk.Frame(conversation)
    bot_message_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    bot_label = tk.Label(bot_message_frame, text=":Bot",
                         font=("Arial", 12), fg="red", anchor="w")
    bot_label.pack(side=tk.RIGHT, padx=(30, 5))
    bot_message = tk.Label(bot_message_frame, text=bot_response, font=(
        "Arial", 12), fg="#000000", anchor="w", wraplength=250)
    bot_message.pack(side=tk.RIGHT, fill=tk.X)
