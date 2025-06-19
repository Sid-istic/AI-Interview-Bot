# 🧠 AI Interview Feedback Bot

An intelligent, voice-based mock interview system that conducts adaptive, role-specific interviews and provides real-time feedback to users — all powered by Machine Learning, Deep Learning, and Transformers.

## 🚀 Demo
🔗 [Live Demo ](https://ai-interview-bot-sid.streamlit.app/)  
📹 Coming soon: Demo video showcasing voice-based adaptive interviews.

---

## 📌 Features

✅ **Job Role Prediction** — Automatically predicts the job role based on uploaded resume.  
✅ **Dynamic Interviewer Personas** — Get a new personality every session: calm HR, strict tech lead, casual senior, etc.  
✅ **Voice-Based Conversation** — AI asks spoken questions; users reply via microphone.  
✅ **Speech-to-Text & Transcription** — Converts user’s voice answers into text using Whisper.  
✅ **Contextual Question Generation** — Each follow-up question is based on the previous response.  
✅ **Feedback Generation** — Gives detailed feedback (tone, clarity, relevance, etc.) after every answer or full interview.  
✅ **Multimodal Input/Output** — Supports both text and voice interactions.

---

## 🧰 Tech Stack

| Area | Tools & Frameworks |
|------|--------------------|
| Machine Learning | Scikit-learn, TensorFlow |
| NLP & Transformers | Google Gemini 1.5-flash |
| Audio | Speech Recognition, ElevenLabs TTS |
| Web App | Streamlit |
| Backend | Python |
| Deployment | Streamlit Cloud / Hugging Face Spaces (TBD) |

---

## 🗂️ Project Structure

```

ai-interview-bot/
├── resume\_classifier/        # ML model for role classification
├── persona\_engine/           # Interviewer personality logic
├── question\_generator/       # Transformer-based dynamic Q generation
├── audio\_interface/          # Voice input/output modules
├── feedback\_module/          # Response evaluation + feedback
├── app.py                    # Streamlit app main file
├── requirements.txt
└── README.md

```

---

## 📄 How It Works

1. **Resume Upload → Job Role Prediction OR choose Yourself**
2. **Random Interviewer Assigned (JSON personality profiles)**
3. **Bot Speaks First Question → User Responds via Voice**
4. **Voice Transcribed → Bot Evaluates and Asks Next Question**
5. **Adaptive Conversation Loop**
6. **Final Feedback Generated (text/audio)**

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/Sid-istic/AI-Interview-Bot.git
cd ai-interview-bot

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

## 🧪 Datasets Used

* **Resume Classification Dataset** by Noran Mohamed — for job role prediction.

---

## 🎯 Goals

* Help job seekers practice interviews in a realistic, non-judgmental environment.
* Provide actionable feedback to improve speaking, technical articulation, and confidence.
* Build a truly interactive AI that adapts to every individual response.

---

## 🔮 Coming Soon

* ✨ Emotion detection via voice
* 📊 Analytics dashboard for interview sessions
* 🎓 Domain-specific interview packs (DS, Backend, HR, etc.)
* 🧠 GPT-4o integration

---


## 📬 Contact

👤 **Siddharth Pratap Singh**
📧 [siddharthsingh10454@gmail.com](mailto:siddharthsingh10454@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/siddharth-pratap-singh-5b12ba203/) | [GitHub](https://github.com/Sid-istic)

---


