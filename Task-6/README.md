# Multilingual Customer Service Chatbot

## Task 6

A multilingual customer service chatbot that extends an existing
RAG-based chatbot to support multilingual conversations while
maintaining context, intent, and conversational continuity.

## Features

- Automatic language detection
- English language support
- Hindi language support
- Telugu language support
- Spanish language support
- Mixed-language input handling
- Roman Hindi / Hinglish detection
- Roman Telugu / Tenglish detection
- Conversation context retention
- Context-aware follow-up questions
- Cross-lingual question processing
- Consistent responses across languages
- RAG-based question answering
- FAISS vector database
- Open-source embedding model
- Streamlit user interface

## Technologies Used

- Python
- Streamlit
- LangChain
- FAISS
- Hugging Face Sentence Transformers
- Google Gemini
- LangDetect
- Pandas
- Python Dotenv

## System Workflow

User Question
      ↓
Language Detection
      ↓
Language Translation
      ↓
Context Resolution
      ↓
FAISS Knowledge Retrieval
      ↓
Gemini Response Generation
      ↓
Translation to User Language
      ↓
Final Response

## Supported Languages

| Language | Code |
|----------|------|
| English | en |
| Hindi | hi |
| Telugu | te |
| Spanish | es |

## Example Inputs

### English

How can I track my order?

### Hindi

मैं अपने ऑर्डर को कैसे ट्रैक कर सकता हूँ?

### Telugu

నా ఆర్డర్‌ను ఎలా ట్రాక్ చేయాలి?

### Spanish

¿Cómo puedo rastrear mi pedido?

### Mixed Hindi + English

Mera order कहाँ है?

### Mixed Telugu + English

నా order ని ఎలా track చేయాలి?

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt