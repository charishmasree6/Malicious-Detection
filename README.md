# 🔐 ThreatDetector – AI-Powered Malicious URL & Scam Email Detection  
A cyber-security web application built using **Flask**, **Google Gemini AI**, and **PyPDF2** to detect:
✔ Scam / Phishing Email Content  
✔ Malicious URL Types (benign, phishing, malware, defacement)  
ThreatGuard acts like a **mini SOC triage tool**, helping users quickly analyze suspicious files or URLs before interacting with them.

 Features:
1. Scam Email Detection (PDF/TXT)
- Upload a **PDF or TXT** file containing email/message content  
- Extracts text using **PyPDF2**  
- Sends content to **Gemini AI** for scam classification  
- Returns:
  - **Real / Legitimate**, or  
  - **Scam / Fake**, with a clear explanation

2. Malicious URL Detection
- Enter any website URL  
- Automatically normalizes missing `http://`  
- AI classifies URL into:
  - `benign` → safe  
  - `phishing` → credential theft  
  - `malware` → harmful downloads  
  - `defacement` → hacked/altered site  
- Color-coded results (green, red, purple, yellow)

 3. Clean & Modern UI
Built using custom HTML + CSS with:
- Dark SOC-style theme  
- Icons  
- Loading spinners  
- Responsive buttons  
- Professional layout 

  4. Lightweight & Fast
- Runs locally  
- No database required  
- Easy to extend or deploy  


Tech Stack Used
| Component | Technology |
|----------|------------|
| Backend | Python, Flask |
| AI Model | Google Gemini (via google-generativeai) |
| File Extraction | PyPDF2 |
| Frontend | HTML, CSS |

## 📁 Folder Structure

malicious-detection/
│── main.py
│── requirements.txt (optional)
│── templates/
│ └── index.html


🔑 Setting Up the API Key
ThreatDetector uses **Google Gemini AI**.  
You must create your own API key.

✔ Step 1 — Go to Google AI Studio  
https://aistudio.google.com/app/apikey

✔ Step 2 — Click “Create API Key”  
If it asks for a project → click **Create Project** → then **Create Key**.

✔ Step 3 — Copy the API Key

It will look like this:

AIzaSyA...yourKeyHere...

graphql
Copy code

✔ Step 4 — Add the key inside your main.py

python
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

How to Run the Project Locally:
1️⃣ Install dependencies
pip install flask google-generativeai PyPDF2

2️⃣ Start the Flask server
python main.py

3️⃣ Open the app in browser
http://127.0.0.1:5000


