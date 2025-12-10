from flask import Flask, render_template, request
from google import genai
import os
import PyPDF2

app = Flask(__name__)

os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY_HERE"

client = genai.Client()

def predict_fake_or_real_email_content(text: str) -> str:
    """
    Uses Gemini to classify email/message content as real or scam.
    """
    prompt = f"""
    You are an expert in detecting online scams, phishing and fraud.

    Analyze the following text and classify it as one of:
    - Real/Legitimate
    - Scam/Fake

    Then briefly explain why.

    Text:
    \"\"\"{text}\"\"\"

    Return only a short explanation starting with either:
    - "Real/Legitimate:" ...
    - "Scam/Fake:" ...
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    if not response or not getattr(response, "text", None):
        return "classification_failed"

    return response.text.strip()


def url_detection(url: str) -> str:
    """
    Uses Gemini to classify a URL as:
    benign, phishing, malware, or defacement.
    Returns ONLY the class name in lowercase.
    """
    prompt = f"""
    You are an advanced AI model specializing in URL security.

    Classify the following URL into exactly one of these categories
    (all lowercase, single word):
    - benign
    - phishing
    - malware
    - defacement

    URL: {url}

    Return ONLY the class name, nothing else.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    if not response or not getattr(response, "text", None):
        return "unknown"

    return response.text.strip().lower()


# ==========================
# Routes
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scam/", methods=["POST"])
def detect_scam():
    # Check file present
    if "file" not in request.files:
        return render_template("index.html", message="No file uploaded.")

    file = request.files["file"]

    if file.filename == "":
        return render_template("index.html", message="No file selected.")

    extracted_text = ""

    # PDF
    if file.filename.lower().endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            pages_text = []
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    pages_text.append(page_text)
            extracted_text = " ".join(pages_text)
        except Exception as e:
            return render_template("index.html", message=f"Error reading PDF: {e}")

    # TXT
    elif file.filename.lower().endswith(".txt"):
        try:
            extracted_text = file.read().decode("utf-8", errors="ignore")
        except Exception as e:
            return render_template("index.html", message=f"Error reading TXT file: {e}")

    else:
        return render_template(
            "index.html",
            message="Invalid file type. Please upload a PDF or TXT file."
        )

    if not extracted_text.strip():
        return render_template("index.html", message="File is empty or text could not be extracted.")

    message = predict_fake_or_real_email_content(extracted_text)
    return render_template("index.html", message=message)


@app.route("/predict", methods=["POST"])
def predict_url():
    url = request.form.get("url", "").strip()

    if not url:
        return render_template("index.html", message="Please enter a URL.")

    # Auto-add http:// if missing so user can type 'google.com'
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    classification = url_detection(url)

    return render_template(
        "index.html",
        input_url=url,
        predicted_class=classification
    )




if __name__ == "__main__":
    app.run(debug=True)
