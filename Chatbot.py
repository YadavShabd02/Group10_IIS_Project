# Group Members:
# Rishi Raina - 2024465
# Shabd Yadav - 2024516
# Harsh Panchal - 2024241
# Nikhil Kumar - 2024382
# Mayank Pratap Singh - 2024339
# Aniket Kumar Rai - 2024073

import os
import json
import re
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import speech_recognition as sr
import getpass
from cryptography.fernet import Fernet
from googletrans import Translator  
import threading
import asyncio
import edge_tts
import speech_recognition as sr
import asyncio
import edge_tts
import tempfile
import os
from playsound import playsound
from googletrans import Translator
from queue import Queue
import threading
import asyncio
import os
import threading
import asyncio
import tempfile
from queue import Queue
import speech_recognition as sr
from playsound import playsound
import edge_tts

class zanpakuto:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_queue = Queue()
        self._start_tts_worker()

    def generate_speech_output_language(self, text, voice_code):
        # enqueue every TTS request
        self.tts_queue.put((text, voice_code))

    def _start_tts_worker(self):
        def worker():
            while True:
                text, voice = self.tts_queue.get()
                try:
                    # run the async TTS in this thread
                    asyncio.run(self._generate_speech_output(text, voice))
                except Exception as e:
                    print(f"TTS Error: {e}")
                self.tts_queue.task_done()

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def _take_speech_input(self, language='en-US'):
        """Listen on the mic; fall back to text on error."""
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language=language)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio, please type instead.")
            return input("You: ")
        except sr.RequestError:
            print("Speech service error, please type instead.")
            return input("You: ")

    async def _generate_speech_output(self, text, voice="en-US-AriaNeural"):
        try:
            # create temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                output_path = tmpfile.name

            # fetch and save TTS
            communicate = edge_tts.Communicate(text=text, voice=voice)
            await communicate.save(output_path)

            # play and clean up
            playsound(output_path)
            os.remove(output_path)

        except Exception as e:
            print(f"Error generating or playing speech: {e}")


        


x = int(input("1. English\n2. French\n3. Spanish\n4. Hindi\n5. Japanese\nPlease enter your choice: "))
lang_map = {
    1: ("en-US", "en-US-AriaNeural"),
    2: ("fr-FR", "fr-FR-DeniseNeural"),
    3: ("es-ES", "es-ES-ElviraNeural"),
    4: ("hi-IN", "hi-IN-MadhurNeural"),
    5: ("ja-JP", "ja-JP-NanamiNeural")
}

def translate_text(text, target_lang):
    translator = Translator()
    try:
        translation = translator.translate(text, src='en', dest=target_lang)
        #print(translation.text)
        return translation.text
    except Exception as e:
        return f"Error: {e}"

if x not in lang_map:x=1
sh = zanpakuto()
dest=lang_map[x][0].split("-")[0]
language=lang_map[x][0]
voice=lang_map[x][1]
############################################################################################

def generate_key():

    key = Fernet.generate_key()

    with open("secret.key", "wb") as key_file:

        key_file.write(key)

    return key

def load_key():

    if os.path.exists("secret.key"):

        with open("secret.key", "rb") as key_file:

            return key_file.read()

    return generate_key()

def encrypt_data(key, data):

    f = Fernet(key)

    return f.encrypt(data.encode())

def decrypt_data(key, encrypted_data):

    f = Fernet(key)

    return f.decrypt(encrypted_data).decode()

def save_secure_data(data, file_path, key):

    encrypted_data = encrypt_data(key, json.dumps(data))

    with open(file_path, "wb") as file:

        file.write(encrypted_data)

def load_secure_data(file_path, key):

    try:

        with open(file_path, "rb") as file:

            encrypted_data = file.read()

        return json.loads(decrypt_data(key, encrypted_data))

    except Exception:

        return None

def admin_login():

    ADMIN_PASSWORD = "SecurePass123"

    attempt = getpass.getpass("Enter admin password: ")

    return attempt == ADMIN_PASSWORD

def store_visitor_data():

    visitor_name = input("Enter visitor name: ")

    meeting_person = input("Meeting with: ")

    time = input("Meeting time: ")

    visitor_data = {"visitor_name": visitor_name, "meeting_with": meeting_person, "time": time}

    key = load_key()

    save_secure_data(visitor_data, "visitor_data.enc", key)

def retrieve_visitor_data():

    if not admin_login():
        text=translate_text("Access denied!",language)
        print(text)

        sh.generate_speech_output_language(text,voice)

        return

    key = load_key()

    visitor_data = load_secure_data("visitor_data.enc", key)

    if visitor_data:

        print(f"Visitor: {visitor_data['visitor_name']}, Meeting with: {visitor_data['meeting_with']}, Time: {visitor_data['time']}")

    else:
        print("chatbot: No visitor data found")
        text=translate_text("No visitor data found.",language)
        print("chatbot: ",text)
        sh.generate_speech_output_language(text,voice)
        
def translate_to_english(text):

    translator = Translator()

    try:

        detection = translator.detect(text)

        if detection.lang != 'en':

            translated = translator.translate(text, dest='en')

            print(f"Translated '{text}' to '{translated.text}'")

            return translated.text

        else:

            return text

    except Exception as e:

        print("Translation error:", e)

        sh.generate_speech_output_language("Oh no! An error has occured",voice)

        return text

def load_knowledge_base(file_path):

    try:

        with open(file_path, "r", encoding="utf-8") as file:

            knowledge_base = json.load(file)

        print("\n")

        return knowledge_base

    except FileNotFoundError:

        print("Chatbot: Knowledge base file not found. Please provide a valid JSON file.")

        sh.generate_speech_output_language("Chatbot:Knowledge base file not found. Please provide a valid JSON file.",voice)

        exit()

    except json.JSONDecodeError:

        print("Chatbot: Error decoding the JSON file. Please check the file format.")

        sh.generate_speech_output_language("Chatbot:Error decoding the JSON file. Please check the file format.")

        exit()

def normalize_input(user_input):

    return re.sub(r"[^\w\s]", "", user_input.lower().strip())

def provide_hospital_info(hospital_details):
    text=translate_text("Welcome! Here are the details of our hospital",dest)
    print(text)
    sh.generate_speech_output_language(text,voice)
    print(f"Chatbot: Welcome to {hospital_details['name']}.")

    print(f"Address: {hospital_details['address']}")

    print("Contact Numbers:")

    for key, value in hospital_details['contactNumbers'].items():

        print(f"  - {key.title()}: {value}")

    print("Timings:")

    for key, value in hospital_details['timings'].items():

        print(f"  - {key.title()}: {value}")

def list_departments(departments):
    print("chatbot: Here are the departments available in our hospital:")
    text=translate_text("Here are the departments available in our hospital:",language)
    sh.generate_speech_output_language(text,voice)

    print("Chatbot:",text )

    for dept in departments:

        print(f"  - {dept['name']}: {dept['description']}")

def list_doctors(doctors):
    print("chatbot: Here is a list of available doctors:")
    text=translate_text("Here is a list of available doctors:",dest)
    sh.generate_speech_output_language(text,voice)
    print("Chatbot:",text )


    print("+--------------------+--------------------+-----------------------------------+")

    print(f"| {'Name':<23} | {'Specialization':<23} | {'Consultation Hours':<23} |")

    print("+--------------------+--------------------+-----------------------------------+")

    for doctor in doctors:

        print(f"| {doctor['name']:<23} | {doctor['specialization']:<23} | {doctor['consultationHours']:<23} |")

    print("+--------------------+--------------------+-----------------------------------+")

def schedule_appointment(doctors, appointments):

    try:

        with open("appointments.json", "r", encoding="utf-8") as file:

            existing_appointments = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        existing_appointments = []



    today = datetime.now().strftime('%Y%m%d')

    token_number = 1

    

    for appt in existing_appointments:

        if 'token' in appt and appt['token'].startswith(today):

            existing_token = int(appt['token'][-3:])

            token_number = max(token_number, existing_token + 1)

    

    token = f"{today}{token_number:03d}"

    print("\nChatbot: Let's schedule an appointment.\n")
    text=translate_text("Let's schedule an appointment",dest)
    sh.generate_speech_output_language(text,voice)
    print("Chatbot:",text )


   
    print("Chatbot: Please provide your name.")
    text=translate_text("Please provide your name",dest)
    sh.generate_speech_output_language(text,voice)
    print("Chatbot:",text )


    patient_name = sh._take_speech_input(language).strip()
    print("You:",patient_name)



    while True:

        print("Chatbot: Which doctor would you like to see?")
        text=translate_text("Which doctor would you like to see?",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )
        for i, doctor in enumerate(doctors):

            print(f"  {i + 1}. {doctor['name']} ({doctor['specialization']}) - Consultation Hours: {doctor['consultationHours']}")

        try:
            print("You:",end="")
            doctor_choice = int(sh._take_speech_input(language).strip()) - 1

            if doctor_choice < 0 or doctor_choice >= len(doctors):

                raise IndexError

            break

        except (ValueError, IndexError):

            print("Chatbot: Invalid choice. Please try again.")
            text=translate_text("Which doctor would you like to see?",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            



    doctor = doctors[doctor_choice]



    while True:

        print(f"Chatbot: At what time would you like the appointment with {doctor['name']}?")
        text=translate_text(f"At what time would you like the appointment with {doctor['name']}?",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )
        

        appointment_time = input("You: ").strip()



        if any(appt['doctor_name'] == doctor['name'] and appt['time'] == appointment_time and appt['patient_name'].lower() != patient_name.lower() for appt in existing_appointments):

            print(f"Chatbot: {doctor['name']} already has an appointment at {appointment_time} with another patient. Please choose a different time.")
            text=translate_text(f"{doctor['name']} already has an appointment at {appointment_time} with another patient. Please choose a different time.",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            continue



        consultation_hours = doctor['consultationHours']

        start_time, end_time = consultation_hours.split(" - ")

        

        fmt = "%I:%M %p"

        try:

            requested_time = datetime.strptime(appointment_time, fmt)

            start_time_dt = datetime.strptime(start_time, fmt)

            end_time_dt = datetime.strptime(end_time, fmt)



            if start_time_dt <= requested_time <= end_time_dt:

                break

            else:

                print(f"Chatbot: {doctor['name']} is not available at {appointment_time}. Please choose a time between {consultation_hours}.")
                text=translate_text(f"{doctor['name']} is not available at {appointment_time}. Please choose a time between {consultation_hours}.",dest)
                sh.generate_speech_output_language(text,voice)
                print("Chatbot:",text )


        except ValueError:

            print("Chatbot: Invalid time format. Please use the format 'HH:MM AM/PM'.")
            print("Chatbot: For Example: 4:40 PM or 10:30 AM")
            text=translate_text("Invalid time format. Please use the format 'HH:MM AM/PM'.",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            



    

    appointment = {

        "patient_name": patient_name,

        "doctor_name": doctor["name"],

        "time": appointment_time,

        "token": token

    }

    sh.generate_speech_output_language("Your appointment has been scheduled!",voice)

    print(f"Chatbot: Your appointment with {doctor['name']} has been scheduled at {appointment_time}.")
    text=translate_text(f"Your appointment with {doctor['name']} has been scheduled at {appointment_time}.",dest)
    sh.generate_speech_output_language(text,voice)
    print("Chatbot:",text )

    print(f"Chatbot: Your token number is: {token}")



    

    while True:
        text=translate_text("Please provide your email",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )
        email = input("Chatbot: Please provide your email: ").strip()

        if re.match(r"[^@]+@[^@]+\.[^@]+", email):

            break

        print("Chatbot: Invalid email format. Please try again.")
        text=translate_text("Invalid email format. Please try again.",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )


        #sh.generate_speech_output_language("Invalid email format. Please try again.",voice)



    while True:
        text=translate_text("please provide a valid phone number",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )
        phone = input("Chatbot: Please provide your phone number: ").strip()
        if re.match(r"^\+?\d{10,15}$", phone):
            break

        print("Chatbot: Invalid phone number format. Please enter a valid number with 10 to 15 digits, optionally starting with '+'.")
        text=translate_text("Invalid phone number format. Please enter a valid number with 10 to 15 digits, optionally starting with '+'.",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )


        #sh.generate_speech_output_language("Invalid phone number format. Please enter a valid number with 10 to 15 digits, optionally starting with '+'.",voice)



    while True:
        text=translate_text("Please enter your gender",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )
        gender = input("Chatbot: Please enter your gender (Male/Female/Other): ").strip().lower()
        gender=translate_to_english(gender)
        if gender in ['male', 'female', 'other']:

            gender = gender.capitalize()

            break

        print("Chatbot: Invalid input. Please enter Male, Female, or Other.")
        text=translate_text("Invalid input. Please enter Male, Female, or Other.",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )

        #sh.generate_speech_output_language("Invalid input. Please enter Male, Female, or Other.",voice)



    while True:
        text=translate_text("Please enter your age",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )
        age = input("Chatbot: Please enter your age: ").strip()

        if age.isdigit() and 0 < int(age) < 120:

            age = int(age)

            break

        print("Chatbot: Invalid age. Please enter a number between 1 and 119.")
        text=translate_text("Invalid age. Please enter a number between 1 and 119.",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )


        #sh.generate_speech_output_language("Invalid age. Please enter a number between 1 and 119.",voice)



    while True:
        text=translate_text("Please enter your address",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )
        address = input("Chatbot: Please enter your address: ").strip()

        if address:
            print("Chatbot: Your data is recorded please let us know how can we help further")
            text=translate_text("Your data is recorded please let us know how can we help further",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )


            break

        print("Chatbot: Address cannot be empty. Please try again.")
        text=translate_text("Address cannot be empty. Please try again.",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )

        #sh.generate_speech_output_language("Address cannot be empty. Please try again.",voice)

    

    appointment.update({

         "email": email,

         "phone": phone,

         "gender": gender,

         "age": age,

         "address": address,

    })



    appointments.append(appointment)

def save_appointments(appointments, file_path="appointments.json"):

    try:

        with open(file_path, "r", encoding="utf-8") as file:

            existing_appointments = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        existing_appointments = []



    existing_appointments.extend(appointments)



    with open(file_path, "w", encoding="utf-8") as file:

        json.dump(existing_appointments, file, indent=4)

    print("Chatbot: Appointments have been saved.")
    text=translate_text("Appointments have been saved.",dest)
    sh.generate_speech_output_language(text,voice)
    print("Chatbot:",text )

    #sh.generate_speech_output_language("Appointments have been saved.",voice)

def check_in_meeting(user_input, knowledge_base, appointments):

    match = re.search(r"meeting with\s+(.+?)(?:\s+at\s+.+)?$", user_input, re.IGNORECASE)

    if match:

        meeting_person = match.group(1).strip()

    else:

        print("Chatbot: I didn't catch who you are meeting with. Please specify.")
        text=translate_text("I didn't catch who you are meeting with. Please specify.",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )

       # sh.generate_speech_output_language("I didn't catch who you are meeting with. Please specify.")

        meeting_person = input("You: ").strip()



    print("Chatbot: May I have your name, please?")
    text=translate_text("May I have your name, please?",dest)
    sh.generate_speech_output_language(text,voice)
    print("Chatbot:",text )

    #sh.generate_speech_output_language("May I have your name, please?",voice)
    print("You:",end="")

    visitor_name = sh._take_speech_input(language).strip()



    try:

        with open("appointments.json", "r", encoding="utf-8") as file:

            file_appointments = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        file_appointments = []

    all_appointments = appointments + file_appointments



    def remove_prefix(name):

        prefixes = ["dr. ", "doctor ", "mr. ", "ms. ", "mrs. "]

        for p in prefixes:

            if name.lower().startswith(p):

                return name[len(p):]

        return name



    meeting_person_normalized = remove_prefix(meeting_person).strip().lower()



    found_appointment = None

    for appt in all_appointments:

        if appt.get("patient_name", "").strip().lower() == visitor_name.lower():

            doctor_normalized = remove_prefix(appt.get("doctor_name", "")).strip().lower()

            if meeting_person_normalized in doctor_normalized:

                found_appointment = appt

                break



    if found_appointment:

        doc_name = found_appointment["doctor_name"]

        doctors_locations = knowledge_base.get("locations", {}).get("doctors", {})

        room = doctors_locations.get(doc_name, {}).get("office")

        if room:

            sh.generate_speech_output_language("Welcome! i have notified the doctor of your arrival, please proceed",voice)

            print(f"Chatbot: Welcome, {visitor_name}. I have notified {doc_name} of your arrival.")
            text=translate_text(f"Chatbot: Welcome, {visitor_name}. I have notified {doc_name} of your arrival.",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            print(f"Please proceed to {room}.")
            text=translate_text(f"Please proceed to {room}.",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

        else:
            text=translate_text(f"Sorry! We were not able to find your appointment",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            #sh.generate_speech_output_language("Sorry! We were not able to find your appointment")

            print(f"Chatbot: Sorry, {visitor_name}. I couldn't locate the office for {doc_name}.")

    else:

        print(f"Chatbot: It appears you do not have a scheduled meeting with {meeting_person}.")

        print("Chatbot: Would you like to schedule an appointment now? (yes/no)")
        text=translate_text("Would you like to schedule an appointment now? (yes/no)",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )

        #sh.generate_speech_output_language("Would you like to schedule an appointment now? yes or no",voice)
        print("You: ",end="")
        answer = sh._take_speech_input(language).strip().lower()

        if answer in ["yes", "y"]:

            schedule_appointment(knowledge_base["doctors"], appointments)

        else:

            print("Chatbot: Alright, please let us know if you need further assistance.")
            text=translate_text(" Alright, please let us know if you need further assistance.",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )



            #sh.generate_speech_output_language("Alright, please let us know if you need further assistance.",voice)

def print_appointment_report(appointment, knowledge_base):

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    filename = f"appointment_report_{appointment['patient_name'].replace(' ', '_')}_{timestamp}.pdf"

    

    doc = SimpleDocTemplate(filename, pagesize=letter)

    styles = getSampleStyleSheet()

    

    title_style = ParagraphStyle(

        'CustomTitle',

        parent=styles['Heading1'],

        alignment=1,

        spaceAfter=30

    )

    

    normal_style = styles['Normal']

    heading_style = styles['Heading2']

    

    content = []

    

    content.append(Paragraph("AIIMS, New Delhi", title_style))

    content.append(Paragraph("Ansari Nagar, New Delhi", title_style))

    content.append(Paragraph("Out Patient Department (e-OPD Card)", title_style))

    content.append(Spacer(1, 20))

    

    content.append(Paragraph(f"Appointment ID: {datetime.now().strftime('%Y%m%d%H%M%S')}", normal_style))

    content.append(Paragraph(f"Appointment Date: {datetime.now().strftime('%d/%m/%Y (%I:%M %p)')}", normal_style))

    content.append(Spacer(1, 20))

    

    content.append(Paragraph("Patient Information", heading_style))

    patient_data = [

        ["Token Number:", appointment['token']],

        ["Name:", appointment['patient_name']],

        ["Gender:", appointment['gender']],

        ["Age:", f"{appointment['age']} years"],

        ["Mobile:", appointment['phone']],

        ["Email:", appointment['email']],

        ["Address:", appointment['address']]

    ]

    

    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])

    patient_table.setStyle(TableStyle([

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('PADDING', (0, 0), (-1, -1), 6),

    ]))

    content.append(patient_table)

    content.append(Spacer(1, 20))

    

    doctor_name = appointment['doctor_name']

    doctor_info = next((doc for doc in knowledge_base["doctors"] if doc["name"] == doctor_name), None)

    doctor_location = knowledge_base["locations"]["doctors"].get(doctor_name, {})

    department = doctor_info["specialization"] if doctor_info else "Unknown"

    

    content.append(Paragraph("Appointment Details", heading_style))

    appointment_data = [

        ["Department:", department],

        ["Reporting Time:", appointment['time']],

        ["Doctor's Name:", appointment['doctor_name']],

        ["Room No.:", doctor_location.get('office', 'Unknown')]

    ]

    

    appointment_table = Table(appointment_data, colWidths=[2*inch, 4*inch])

    appointment_table.setStyle(TableStyle([

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('PADDING', (0, 0), (-1, -1), 6),

    ]))

    content.append(appointment_table)

    

    try:

        doc.build(content)

        print(f"\nChatbot: Appointment report has been saved to '{filename}'")
        text=translate_text(f"Appointment report has been saved to '{filename}'",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )

        

    except Exception as e:

        print(f"Chatbot: Error saving the PDF report: {str(e)}")

def cancel_appointment(appointments):

    try:

        with open("appointments.json", "r", encoding="utf-8") as file:

            existing_appointments = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        existing_appointments = []

        print("Chatbot: No appointments found in the system.")
        text=translate_text(" No appointments found in the system.",language)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )

        #sh.generate_speech_output_language("No appointments found in the system.",voice)

        return



    print("\nChatbot: Please provide your name.")
    text=translate_text(" Please provide your name.",language)
    sh.generate_speech_output_language(text,voice)
    print("Chatbot:",text )


    #sh.generate_speech_output_language("Please Provide your name",voice)
    print("You: ",end="")
    patient_name = sh._take_speech_input(language).strip()

    patient_appointments = [

        (i, appt) for i, appt in enumerate(existing_appointments) 

        if appt['patient_name'].lower() == patient_name.lower()

    ]

    

    if not patient_appointments:

        print("Chatbot: No appointments found under your name.")
        text=translate_text("No appointments found under your name.",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )


        #sh.generate_speech_output_language("No appointments found under your name.",voice)

        return

    

    print("\nChatbot: Here are your appointments:")
    text=translate_text(" Here are your appointments:",dest)
    sh.generate_speech_output_language(text,voice)
    print("Chatbot:",text )

    #sh.generate_speech_output_language("Here are your appointments")

    for i, (_, appt) in enumerate(patient_appointments):

        print(f"{i + 1}. {appt['doctor_name']} at {appt['time']}")

    

    while True:

        try:
            text=translate_text("Enter the number of the appointment you want to cancel (0 to exit):",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )
            choice = int(input("\nChatbot: Enter the number of the appointment you want to cancel (0 to exit): "))

            

            #sh.generate_speech_output_language("Enter the number of the appointment you want to cancel",voice)

            if choice == 0:

                return

            if 1 <= choice <= len(patient_appointments):

                index = patient_appointments[choice - 1][0]

                cancelled_appt = existing_appointments.pop(index)

                with open("appointments.json", "w", encoding="utf-8") as file:

                    json.dump(existing_appointments, file, indent=4)

                print(f"\nChatbot: Your appointment with {cancelled_appt['doctor_name']} at {cancelled_appt['time']} has been cancelled.")
                text=translate_text(f"Your appointment with {cancelled_appt['doctor_name']} at {cancelled_appt['time']} has been cancelled.",dest)
                sh.generate_speech_output_language(text,voice)
                print("Chatbot:",text )

                break

            print("Chatbot: Invalid choice. Please try again.")
            text=translate_text(" Invalid choice. Please try again.",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )


            #sh.generate_speech_output_language("Invalid choice. Please try again.",voice)

        except ValueError:

            print("Chatbot: Please enter a valid number.")

            sh.generate_speech_output_language("Please enter a valid number.",voice)

def reschedule_appointment(doctors, appointments):

    try:

        with open("appointments.json", "r", encoding="utf-8") as file:

            existing_appointments = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        existing_appointments = []

        print("Chatbot: No appointments found in the system.")
        text=translate_text("No appointments found in the system.",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )

        #sh.generate_speech_output_language("No appointments found in the system.",voice)

        return



    print("\nChatbot: Please provide your name.")
    text=translate_text("Please provide your name.",dest)
    sh.generate_speech_output_language(text,voice)
    print("Chatbot:",text )

    #sh.generate_speech_output_language("Please provide your name",voice)

    patient_name = sh._take_speech_input(language).strip()

    

    patient_appointments = [

        (i, appt) for i, appt in enumerate(existing_appointments) 

        if appt['patient_name'].lower() == patient_name.lower()

    ]

    

    if not patient_appointments:

        print("Chatbot: No appointments found under your name.")
        text=translate_text("No appointments found under your name.",dest)
        sh.generate_speech_output_language(text,voice)
        print("Chatbot:",text )

        #sh.generate_speech_output_language("No appointments found under your name.",voice)

        return

    

    print("\nChatbot: Here are your appointments:")
    text=translate_text("Here are your appointments:",dest)
    sh.generate_speech_output_language(text,voice)
    print("Chatbot:",text )


    #sh.generate_speech_output_language("Here are your appointments",voice)

    for i, (_, appt) in enumerate(patient_appointments):

        print(f"{i + 1}. {appt['doctor_name']} at {appt['time']}")

    

    while True:

        try:
            text=translate_text("Enter the number of the appointment you want to Reschedule",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )
            #sh.generate_speech_output_language("Enter the number of the appointment you want to Reschedule",voice)

            choice = int(input("\nChatbot: Enter the number of the appointment you want to reschedule (0 to exit): "))

            if choice == 0:

                return

            if 1 <= choice <= len(patient_appointments):

                index = patient_appointments[choice - 1][0]

                old_appt = existing_appointments[index]

                doctor = next(d for d in doctors if d['name'] == old_appt['doctor_name'])

                

                while True:

                    print(f"\nChatbot: Current appointment time: {old_appt['time']}")
                    text=translate_text(f"Current appointment time: {old_appt['time']}",dest)
                    sh.generate_speech_output_language(text,voice)
                    print("Chatbot:",text )

                    print(f"Doctor's consultation hours: {doctor['consultationHours']}")
                    text=translate_text(f"Doctor's consultation hours: {doctor['consultationHours']}",dest)
                    sh.generate_speech_output_language(text,voice)
                    print("Chatbot:",text )

                    new_time = input("Enter new appointment time (HH:MM AM/PM): ").strip()

                    

                    if any(appt['doctor_name'] == doctor['name'] and 

                          appt['time'] == new_time and 

                          appt['patient_name'].lower() != patient_name.lower() 

                          for appt in existing_appointments):

                        print(f"Chatbot: {doctor['name']} already has an appointment at {new_time}.")
                        text=translate_text(f"Chatbot: {doctor['name']} already has an appointment at {new_time}.",dest)
                        sh.generate_speech_output_language(text,voice)
                        print("Chatbot:",text )


                        continue



                    consultation_hours = doctor['consultationHours']

                    start_time, end_time = consultation_hours.split(" - ")

                    

                    fmt = "%I:%M %p"

                    try:

                        requested_time = datetime.strptime(new_time, fmt)

                        start_time_dt = datetime.strptime(start_time, fmt)

                        end_time_dt = datetime.strptime(end_time, fmt)



                        if start_time_dt <= requested_time <= end_time_dt:

                            old_appt['time'] = new_time

                            with open("appointments.json", "w", encoding="utf-8") as file:

                                json.dump(existing_appointments, file, indent=4)

                            print(f"\nChatbot: Your appointment has been rescheduled to {new_time}.")
                            text=translate_text(f"\nChatbot: Your appointment has been rescheduled to {new_time}.",dest)
                            sh.generate_speech_output_language(text,voice)
                            print("Chatbot:",text )


                            #sh.generate_speech_output_language("Your appointment has been rescheduled",voice)

                            return

                        else:

                            print(f"Chatbot: Time must be between {consultation_hours}.")
                            text=translate_text(f"Time must be between {consultation_hours}.",dest)
                            sh.generate_speech_output_language(text,voice)
                            print("Chatbot:",text )

                    except ValueError:

                        print("Chatbot: Invalid time format. Please use HH:MM AM/PM format.")
                        text=translate_text("Invalid time format. Please use HH:MM AM/PM format.",dest)
                        sh.generate_speech_output_language(text,voice)
                        print("Chatbot:",text )

                        #sh.generate_speech_output_language("Invalid time format. Please use HH:MM AM/PM format.",voice)

            else:

                print("Chatbot: Invalid choice. Please try again.")
                text=translate_text("Invalid choice. Please try again.",dest)
                sh.generate_speech_output_language(text,voice)
                print("Chatbot:",text )


                #sh.generate_speech_output_language("Invalid choice. Please try again.",voice)

        except ValueError:

            print("Chatbot: Please enter a valid number.")

            sh.generate_speech_output_language("Please enter a valid number.",voice)

def chatbot(knowledge_base):

    appointments = []

    #speech =sh._take_speech_input()

    print("Chatbot: Hi! Welcome to the Hospital Reception Chatbot. How can I assist you today?")
    text=translate_text("Hi! Welcome to the Hospital Reception Chatbot. How can I assist you today?",dest)
    sh.generate_speech_output_language(text,voice)
    print("Chatbot:",text )

    #sh.generate_speech_output_language("hi welcome to the hospital reception chatbot how can i assist you today",voice)

    while True:

        raw_input = sh._take_speech_input(language).strip()

        translated_input = translate_to_english(raw_input)

        inp = translated_input.lower()



        if any(word in inp for word in ["exit", "quit", "thank you", "thanks", "bye"]):

            save_appointments(appointments)

            if appointments:

                print_appointment_report(appointments[-1], knowledge_base)

            print("Chatbot: Thank you for using the chatbot. Have a great day!")
            text=translate_text("Thank you for using the chatbot. Have a great day!",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            #sh.generate_speech_output_language("Thank you for using the chatbot. Have a great day!",voice)

            break

        elif any(word in inp for word in ["store secure visitor data", "store secure", "store visitor data", "secure"]):

            store_visitor_data()

        elif any(word in inp for word in ["retreive visitor data", "retreive"]):

            retrieve_visitor_data()

        elif "hospital" in inp or "info" in inp:

            print("\nChatbot: Here is the information about our hospital:\n")
            text=translate_text("Here is the information about our hospital",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            provide_hospital_info(knowledge_base["hospitalDetails"])

        elif any(word in inp for word in ["departments", "dept", "dept.", "Dept.", "Dept", "department", "Department", "depart", "Depart", "depart."]):

            print("\nChatbot: Here is the list of departments available in our hospital:\n")
            text=translate_text("here is the list of departments available in our hospital",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            list_departments(knowledge_base["departments"])

        elif any(word in inp for word in ["doctor's list", "doctor list", "about doctors", "about doctor", "doctor information", "doctor details"]):

            print("\nChatbot: Here is the list of doctors available in our hospital:\n")
            text=translate_text("here is the list of dictors available in our hospital",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )
            list_doctors(knowledge_base["doctors"])

        elif any(word in inp for word in ["reschedule", "move", "change", "modify", "edit", "update"]):

            reschedule_appointment(knowledge_base["doctors"], appointments)

        elif any(word in inp for word in ["cancel appointment", "cancel", "cancel an appointment", "cancel appointments"]):

            cancel_appointment(appointments)

        elif any(word in inp for word in ["appointment", "appoint", "book", "Book", "Booking", "booking", "FIX", "fix", "arrange"]):

            schedule_appointment(knowledge_base["doctors"], appointments)

        elif "meeting with" in inp:

            check_in_meeting(inp, knowledge_base, appointments)

        elif any(word in inp for word in ["virtual", "video", "call", "telemedicine", "tele", "online"]):

            print("Chatbot: Sorry, we don't have a virtual consultation service. Please Book an appointment for a physical consultation.")
            text=translate_text("Sorry we don't have a  virtual consultation service Please book an appointment for a physical consultation",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            #sh.generate_speech_output_language("Sorry, we don't have a virtual consultation service. Please Book an appointment for a physical consultation.",voice)

        elif any(word in inp for word in ["support team", "support", "team", "Team"]):

            print("Chatbot: Sorry for the inconvenience. Our support team is available from 9 AM to 5 PM on all weekdays. You can reach us at +91 9876543210.")
            text=translate_text("sorry for the inconvvenience our support team is available from 9 AM to 5 pm on all weekdays you can reach us at 919876543210",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            #sh.generate_speech_output_language("Sorry for the inconvenience. Our support team is available from 9 AM to 5 PM on all weekdays. You can reach us at +91 9876543210.",voice)

            print("Chatbot: Please let us know how we can assist you further.")
            text=translate_text("Please let us know how can we assist you further",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            #sh.generate_speech_output_language("Please let us know how we can assist you further.",voice)

        else:

            print("Chatbot: Invalid Input. Please try again.")
            text=translate_text("Invalid input please try again",dest)
            sh.generate_speech_output_language(text,voice)
            print("Chatbot:",text )

            #sh.generate_speech_output_language("Invalid Input. Please try again.",voice)

if __name__ == "__main__":

    knowledge_base_file = "knowledge_base.json"

    knowledge_base = load_knowledge_base(knowledge_base_file)

    chatbot(knowledge_base)

