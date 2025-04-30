# Project : Hospital Reception Chatbot

## 1. Description / Objective

This project is a multilingual AI-powered Hospital Reception Chatbot capable of: 
1) Handling visitor queries
2) Providing hospital details 
3) Listing departments and doctors 
4) Managing appointments (booking, cancellation, and rescheduling) 

- It features speech recognition and voice response 
- Translation across five languages and generates e-OPD appointment reports.

---

## 2. Necessary Libraries / Installation Requirements

Install the required libraries by running:

```bash
pip install -r requirements.txt
```

Or install them manually:

```bash
pip install speechrecognition googletrans==4.0.0-rc1 edge-tts playsound cryptography reportlab
```

> **Note:** `edge-tts` requires Python 3.7+. On macOS, you may also need `portaudio` installed for `speechrecognition`.

---

## 3. Commands to Run the Project

Follow the steps below to run the chatbot:

```bash
# Step 1: Clone the repository
git clone https://github.com/Nikkumar-12345/IIS-CHATBOT-PROJECT

# Step 2: Navigate to the project directory
cd Group_10

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run the chatbot
python Chatbot.py
```

---

## 4. File Structure

```
Group_10/
│
├── README.md                 # Project overview and usage instructions
├── Chatbot.py             # Main script for chatbot logic
├── Knowledge_Base.json       # Stores hospital, department, doctor, and location info
├── appointments.json         # Stores scheduled appointment records
├── visitor_data.enc          # Encrypted visitor check-in data (generated at runtime)
├── secret.key                # Symmetric encryption key (generated on first run)
├── requirements.txt          # List of required Python packages (to be created)
└── appointment_report_*.pdf  # Generated appointment confirmation report (runtime)
```

---

## 5. Features

-  Speech-to-text interaction using Google Speech Recognition  
-  Voice output using Microsoft Edge TTS  
-  Language translation (English, Hindi, French, Spanish, Japanese)  
-  Encrypted visitor data storage and admin-only retrieval  
-  Real-time appointment scheduling, rescheduling, and cancellation  
-  Automated PDF generation for e-OPD appointment slips  
-  Intelligent query handling based on a structured knowledge base  

---

> **Note:** Ensure microphone access is enabled for speech input, and the terminal is interactive.

Happy healthcare automation! 🏥🤖