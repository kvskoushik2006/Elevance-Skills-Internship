# 🤖 Multi-Modal AI Assistant

An intelligent **Multi-Modal AI Assistant** built using **Python**, **Streamlit**, and **Google Gemini API**. This application can understand both **text** and **images**, maintain conversation memory, perform intelligent decision-making, validate responses, and provide context-aware AI assistance.

---

## 🚀 Features

- 💬 Text-based AI Chat
- 🖼️ Image Understanding using Google Gemini Vision
- 🧠 Conversation Memory
- 📷 Image Summary Memory
- 🤖 Intelligent Reasoning Engine
- ✅ Response Validation
- 🔄 Multi-turn Conversations
- 🎨 User-Friendly Streamlit Interface
- ⚠️ Error Handling & Exception Management

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google Generative AI SDK
- Pillow
- Python Dotenv

---

## 📂 Project Structure

```
Task2_Multimodal_AI_Assistant/
│── app.py
│── chat.py
│── vision.py
│── memory.py
│── reasoning.py
│── validator.py
│── requirements.txt
│── README.md
│── .env
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Task2_Multimodal_AI_Assistant.git
```

### 2. Navigate to the project folder

```bash
cd Task2_Multimodal_AI_Assistant
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

### 5. Run the application

```bash
streamlit run app.py
```

---

## 🧠 Project Workflow

```
                User
                  │
                  ▼
          Streamlit Interface
                  │
                  ▼
          Reasoning Engine
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
     Text Chat         Image Analysis
          │                 │
          └────────┬────────┘
                   ▼
        Conversation Memory
                   ▼
        Response Validation
                   ▼
            Final Response
```

---

## ✨ Intelligent Features

- Automatically decides whether to use text or image analysis.
- Maintains previous conversation context.
- Stores image summaries for better contextual understanding.
- Validates responses before displaying them.
- Handles ambiguous questions intelligently.
- Provides evidence-based responses whenever possible.

---

## 📸 Sample Use Cases

### Text Chat

```
User:
What is Artificial Intelligence?

Assistant:
Artificial Intelligence (AI) is the simulation of human intelligence by machines...
```

---

### Image Analysis

Upload an image and ask:

```
Describe this image.
```

```
What color is the car?
```

```
How many people are visible?
```

---

### Memory

```
User:
My name is Koushik.

User:
What is my name?
```

Assistant remembers previous conversation.

---

## 🎯 Internship Task Objectives Achieved

- ✅ Text Understanding
- ✅ Image Understanding
- ✅ Conversation Memory
- ✅ Contextual Reasoning
- ✅ Intelligent Decision Making
- ✅ Ambiguity Handling
- ✅ Response Validation
- ✅ Evidence-based Responses
- ✅ Multi-Modal AI Interaction

---

## 📦 Requirements

```
streamlit
google-generativeai
python-dotenv
Pillow
```

---

## 👨‍💻 Developer

**Koushik Venkatasai**

Computer Science Engineering Student

---

## 📄 License

This project is developed for educational and internship purposes.