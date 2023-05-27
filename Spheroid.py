from DischargeFeatures import discharge_planning
from EntityRecogniser import predict_intent
from RiskAnalysis import RiskAnalysis_predict
import speech_recognition as sr
import pandas as pd
import urllib as ul
import webbrowser
import pywhatkit as pw
import speech_recognition as Sr
import pyttsx3
import tkinter as tk
import csv
import tkinter as tk
import mysql.connector

doctors = [
    {"name": "Dr.jake", "specialty": "Cardiologist"},
    {"name": "Dr.kumar", "specialty": "Pediatrician"},
    {"name": "Dr.ravi", "specialty": "Dermatologist"},
]

# global query
Asst = pyttsx3.init("sapi5")
voices = Asst.getProperty("voices")

Asst.setProperty("voices", voices[1].id)
Asst.setProperty("rate", 170)

user_spoke = False

def Speak(audio):
    # print(f"Bot : {audio}")
    # print("  ")
    Asst.say(audio)
    Asst.runAndWait()



# pip install mysql-connector-python
conn = mysql.connector.connect(host='localhost', user = 'root', password = '*****',database ='spheroid_db')
mycursor = conn.cursor()

import pyttsx3
Asst = pyttsx3.init("sapi5")
voices = Asst.getProperty("voices")
# print(voices)

Asst.setProperty("voices", voices[1].id)
Asst.setProperty("rate", 170)

def process_audio_input():
    global user_spoke
    user_spoke = True
    print("Listening..")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        input_text.delete(0, tk.END)
        input_text.insert(0, r.recognize_google(audio))
        display_usermsg_and_process()
        print("Recognized")
    except sr.UnknownValueError:
        displaybotmsg("Sorry, I did not understand what you said.")
    except sr.RequestError:
        displaybotmsg("Sorry, there was an error processing your request.")


def appointment():
    displaybotmsg("Sure, please provide the following details:")
    form_window = tk.Toplevel()

    # create labels and entry fields for the form
    tk.Label(form_window, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(form_window)
    name_entry.grid(row=0, column=1)

    tk.Label(form_window, text="Age").grid(row=1, column=0)
    age_entry = tk.Entry(form_window)
    age_entry.grid(row=1, column=1)

    tk.Label(form_window, text="Gender").grid(row=2, column=0)
    gender_entry = tk.Entry(form_window)
    gender_entry.grid(row=2, column=1)

    tk.Label(form_window, text="Medical History").grid(row=3, column=0)
    medical_history_entry = tk.Entry(form_window)
    medical_history_entry.grid(row=3, column=1)

    tk.Label(form_window, text="Insurance Number").grid(
        row=4, column=0)
    insurance_entry = tk.Entry(form_window)
    insurance_entry.grid(row=4, column=1)

    tk.Label(form_window, text="Date").grid(row=5, column=0)
    date_entry = tk.Entry(form_window)
    date_entry.grid(row=5, column=1)

    tk.Label(form_window, text="Time").grid(row=6, column=0)
    time_entry = tk.Entry(form_window)
    time_entry.grid(row=6, column=1)

    selected_doctor = tk.StringVar()
    tk.Label(form_window, text="Choose Doctor").grid(row=7, column=0)
    for i, doctor in enumerate(doctors):
        doctor_radio = tk.Radiobutton(form_window, text=doctor["name"] + " (" + doctor["specialty"] + ")", variable=selected_doctor, value=doctor["name"])
        doctor_radio.doctor = doctor  # store doctor data in the radio button object
        doctor_radio.grid(row=8+i, column=1, sticky=tk.W)

    submit_button = tk.Button(form_window, text="Submit", command=lambda: submit_form(name_entry.get(), age_entry.get(), gender_entry.get(), medical_history_entry.get(), insurance_entry.get(), date_entry.get(), time_entry.get(), selected_doctor.get(), form_window))
    submit_button.grid(row=8+len(doctors), column=1)

def submit_form(name, age, gender, medical_history, insurance, date, time,selected_doctors, form_window):
    try:
        RiskAnalysis_predict(name,age,gender,medical_history,conversation,user_spoke)
    except KeyError:
        print("Unable to recognize")
    except ValueError as vr:
        print(vr)
        print("Value error crossed over")
    with open('appointments.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(
            [name, age, gender, medical_history, insurance, date, time,selected_doctors])

    sql = "INSERT INTO patients_appointments (Firstname, Age, Gender, Date, Time, Doctor) VALUES (%s, %s, %s,%s, %s, %s)"
    values = (name, age, gender, date, time, selected_doctors)
    mycursor.execute(sql, values)

    conn.commit()

    print(mycursor.rowcount, "record inserted.")
    displaybotmsg("Thank you, your appointment has been booked")
    form_window.destroy()

def TaskExe(query):
    tag = predict_intent(query)
    if tag == "greeting":
        displaybotmsg("Hello I am spheroid")
    elif tag == "thanks":
        displaybotmsg("thank you,I am happy to help you anytime")

    elif tag == "goodbye":
        displaybotmsg("bye, see you again")

    elif tag == "appointment":
        displaybotmsg("proceeding for appointment process")
        appointment()
    elif tag == "break":
        displaybotmsg("Ok you can call me back anytime")

    elif tag == "riskfactorAnalysis":
        try:
            # patient_registration()
            appointment()
        except ValueError as vr:
            displaybotmsg(
                "Sorry data is insuffient/inappropriate to analyze i am still learning please do")
            displaybotmsg("proceed with the appointment")

    elif tag == "discharge":
        displaybotmsg("Please do enter these details if you are planning for the discharge")
        displaybotmsg("Sure, please provide the following details:")
        discharge_planning(conversation)

    elif "how are you" in query:
        displaybotmsg("I am fine!")
        displaybotmsg("What about you ?")

    elif "you are doing well" in query:
        displaybotmsg("Thank you, Happy to hear that .. ")
        
    elif "search" in query:
        displaybotmsg("This is what I have found for your search")
        query = query.replace("Spheroid", "")
        query = query.replace("Google search", "")
        pw.search(query)
        displaybotmsg("Done")
    elif "fine" in query:
        displaybotmsg("That's great")

    elif "website" in query:
        displaybotmsg(" Searching for the website")
        new = 2
        query = query.replace("Spheroid", "")
        query = query.replace("website", "")
        web1 = query.replace("open", "")
        web1 = web1.replace(" ", "")
        web2 = "https://www." + web1 + ".com"
        webbrowser.open(web2, new=new)
        displaybotmsg("Launched")
    elif "yes" in query:
        appointment()
    elif "no" in query:
        displaybotmsg("Thank you for using AI Chatbot")
    elif "check risk factor" in query:
        displaybotmsg("To check risk factor please do book appointment")
    elif "unboundlocalerror" in query:
        displaybotmsg("Speak again")
    elif "typeerror" in query:
        displaybotmsg("Speak again")
    elif "discharge" in query:
        discharge_planning()
        displaybotmsg("Thank you")
    else:
        displaybotmsg("Sorry I am still learning")


def display_usermsg_and_process():
    global user_spoke
    user_input = input_text.get()
    # create new message frame for user input
    user_message_frame = tk.Frame(conversation)
    user_message_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    user_label = tk.Label(user_message_frame, text="You:",
                          font=("Arial", 12), fg="blue", anchor="w")
    user_label.pack(side=tk.LEFT, padx=(0, 5))
    user_message = tk.Label(user_message_frame, text=user_input, font=(
        "Arial", 12), fg="#000000", anchor="w", wraplength=250)
    user_message.pack(side=tk.LEFT, fill=tk.X)
    TaskExe(user_input)

def display_usermsg_and_process_Speech(user_said):
    global user_spoke 
    user_spoke = True
    user_input = user_said
    # create new message frame for user input
    user_message_frame = tk.Frame(conversation)
    user_message_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    user_label = tk.Label(user_message_frame, text="You:",
                          font=("Arial", 12), fg="blue", anchor="w")
    user_label.pack(side=tk.LEFT, padx=(0, 5))
    user_message = tk.Label(user_message_frame, text=user_input, font=(
        "Arial", 12), fg="#000000", anchor="w", wraplength=250)
    user_message.pack(side=tk.LEFT, fill=tk.X)
    TaskExe(user_input)


def display_usermsg():
    user_input = input_text.get()
    # create new message frame for user input
    user_message_frame = tk.Frame(conversation)
    user_message_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    user_label = tk.Label(user_message_frame, text="You:",
                          font=("Arial", 12), fg="blue", anchor="w")
    user_label.pack(side=tk.LEFT, padx=(0, 5))
    user_message = tk.Label(user_message_frame, text=user_input, font=(
        "Arial", 12), fg="#000000", anchor="w", wraplength=250)
    user_message.pack(side=tk.LEFT, fill=tk.X)
    return user_input


def displaybotmsg(bot_response):
    # create new message frame for bot response
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

    input_text.delete(0, tk.END)


root = tk.Tk()
root.title("Spheroid")
root.geometry("700x600")
root.configure(bg="floral white")

conversation = tk.Frame(root, bg="old lace")
conversation.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

input_text = tk.Entry(root, font=("Arial", 14), width=30)
input_text.grid(row=1, column=0, padx=10, pady=10, sticky="w")

speak_button = tk.Button(root, text="Speak", font=(
    "Arial", 14), bg="#611b6e", fg="white", command=process_audio_input)
speak_button.grid(row=1, column=1, padx=(10, 0), pady=10, sticky="w")

send_button = tk.Button(root, text="Send", font=(
    "Arial", 14), bg="#611b6e", fg="white", command=display_usermsg_and_process)
send_button.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="e")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

conversation.columnconfigure(0, weight=1)
conversation.columnconfigure(1, weight=1)
conversation.rowconfigure(0, weight=0)

root.mainloop()
