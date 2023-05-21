from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import random
import pyttsx3
import mysql.connector
import tkinter as tk
import csv

Asst = pyttsx3.init("sapi5")
voices = Asst.getProperty("voices")

Asst.setProperty("voices", voices[1].id)
Asst.setProperty("rate", 170)

user_spoke = False

conn = mysql.connector.connect(host='localhost', user = 'root', password = '******',database ='spheroid_db')
mycursor = conn.cursor()

def Speak(audio):
    Asst.say(audio)
    Asst.runAndWait()

def discharge_planning(conversation):
    patient_data = pd.read_csv(
        r"C:\Users\***PATH***\patient_data.csv"
    )

# Separate categorical and numerical features

    categorical_features = ["Gender", "Insurance_Type", "Medical_History"]
    numerical_features = ["Age", "Length_of_Stay"]

# Define pipeline for preprocessing categorical features
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

# Define pipeline for preprocessing numerical features
    numerical_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")),
               ("scaler", StandardScaler())]
    )

# Use ColumnTransformer to preprocess both categorical and numerical features
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_transformer, categorical_features),
            ("num", numerical_transformer, numerical_features),
        ]
    )

# Train machine learning model to predict likelihood of readmission
    X = patient_data[
        ["Age", "Gender", "Medical_History", "Length_of_Stay", "Insurance_Type"]
    ]
    y = patient_data["Readmission"]

    model = Pipeline(
        steps=[("preprocessor", preprocessor),
               ("classifier", LogisticRegression())]
    )

    model.fit(X, y)
    prediction_discharge(model,conversation)



#chatbot function to assist with discharge planning
def prediction_discharge(model,conversation):
    
    form_window = tk.Toplevel()

    #labels and entry fields for the form
    tk.Label(form_window, text="Name").grid(row=0, column=0)
    name = tk.Entry(form_window)
    name.grid(row=0, column=1)

    tk.Label(form_window, text="Age").grid(row=1, column=0)
    age = tk.Entry(form_window)
    age.grid(row=1, column=1)

    tk.Label(form_window, text="Gender").grid(row=2, column=0)
    gender= tk.Entry(form_window)
    gender.grid(row=2, column=1)

    tk.Label(form_window, text="Diagonsed with : ").grid(row=3, column=0)
    medical_history = tk.Entry(form_window)
    medical_history.grid(row=3, column=1)

    tk.Label(form_window, text="length of stay :").grid(row=4, column=0)
    length_of_stay = tk.Entry(form_window)
    length_of_stay.grid(row=4, column=1)

    tk.Label(form_window, text="Insurance Type").grid(
        row=5, column=0)
    insurance_type = tk.Entry(form_window)
    insurance_type.grid(row=5, column=1)

    tk.Label(form_window, text="Rural(R)/Urban(U)").grid(
        row=6, column=0)
    Location = tk.Entry(form_window)
    Location.grid(row=6, column=1)

    submit_button = tk.Button(form_window, text="Submit", command=lambda: submit_form2(name.get(),age.get(),gender.get(),medical_history.get(),length_of_stay.get(),insurance_type.get(),Location.get(),model,form_window,conversation))
    submit_button.grid(row=7, column=1)

def submit_form2(name,age,gender,medical_history,length_of_stay,insurance_type,Location,model,form,conversation):
    
    sql = "INSERT INTO discharge_table (patient_Name, Age, Gender, Medical_History,Length_Of_Stay,Insurance_Type,Location) VALUES (%s, %s, %s,%s, %s, %s,%s)"
    values = (name, age, gender, medical_history,length_of_stay,insurance_type,Location)
    mycursor.execute(sql, values)
    conn.commit()
    with open('discharge_data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(
            [name,age,gender,medical_history,length_of_stay,insurance_type,Location])
    age = int(age)
    length_of_stay = int(length_of_stay)
    # Use model to predict likelihood of readmission
    input_data = pd.DataFrame(
        [[age, gender, medical_history, length_of_stay, insurance_type]],
        columns=[
            "Age",
            "Gender",
            "Medical_History",
            "Length_of_Stay",
            "Insurance_Type",
        ],
    )
    prob = model.predict_proba(input_data)[:, 1][0]
    form.destroy()
    # Provide discharge recommendations based on readmission probability
    if prob < 0.1:
        str = "Based on your medical history and insurance coverage, we recommend that you follow up with your primary care provider within two weeks of discharge. Thank you for choosing our hospital."
    elif prob < 0.5:
        str ="Based on your medical history and insurance coverage, we recommend that you schedule a follow-up appointment with a specialist within one week of discharge. We will arrange for any necessary medical equipment to be delivered to your home. Thank you for choosing our hospital."
    else:
        str = "Based on your medical history and insurance coverage, we recommend that you schedule a follow-up appointment with a specialist within three days of discharge. We will arrange for a home health nurse to visit you within 24 hours of discharge. Thank you for choosing our hospital."
    displaybotmsg(str,conversation)

def displaybotmsg(bot_response,conversation):
    #new message frame for bot response
    global user_spoke
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

