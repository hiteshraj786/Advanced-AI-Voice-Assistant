# Jarvis Advanced AI Assistant

![Jarvis AI](https://img.shields.io/badge/AI-Jarvis-blue?style=for-the-badge&logo=openai)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-brightgreen?style=for-the-badge&logo=python)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-orange?style=for-the-badge&logo=qt)

**Jarvis Advanced AI Assistant** is a highly capable, voice-controlled virtual assistant designed to perform a myriad of tasks ranging from conversational AI and real-time web scraping to automation, image generation, and system control. Powered by robust Language Models like **Cohere** and **Groq**, and crafted with an interactive **PyQt5** interface, Jarvis elevates the personal assistant experience.

---

## 🌟 Key Features

### 1. **Advanced Decision-Making Model (DMM)**
Utilizes **Cohere's** cutting-edge LLMs (Command model) to understand the context of every user prompt. The DMM intelligently categorizes user queries into specific actions like `general` conversation, `realtime` search, `open` applications, `generate image`, etc., ensuring an optimized and precise response.

### 2. **Conversational AI Chatbot**
Powered by the **Groq API** utilizing the Llama-3 model. It is capable of answering general inquiries, engaging in deep conversations, and retaining memory of prior interactions. 

### 3. **Realtime Web Search & Scraper**
Automatically navigates the web to find real-time answers that are beyond the AI model's training data. Uses **BeautifulSoup** and **Pywhatkit** to scrape answers directly from Google Search, providing you with up-to-date information.

### 4. **AI Image Generation**
Features an integrated **Stable Diffusion (Hugging Face)** image generator. Just ask Jarvis to generate an image, and it will fetch high-resolution, ultra-detailed images asynchronously and save them in the local directory.

### 5. **PC & Web Automation**
Say goodbye to manual clicks! Jarvis can:
- Open and close local PC applications (via `AppOpener`).
- Open websites seamlessly.
- Perform YouTube searches and automatically play videos.

### 6. **Content Writing & Documentation**
Need an application or an email written? Just ask. Jarvis will use Groq AI to draft clean, concise content, save it into a `.txt` file, and automatically pop it open for you in Notepad.

### 7. **Speech-to-Text & Text-to-Speech**
- **Speech Recognition:** Implements the `speech_recognition` module for highly accurate wake-word and command listening.
- **Voice Response (TTS):** Uses `edge-tts` to deliver smooth, natural, and highly responsive audio feedback.

### 8. **Multithreaded Interactive GUI**
Built with **PyQt5**, the modern interface continuously runs on a separate thread, providing real-time feedback of the assistant's state (`Listening...`, `Thinking...`, `Searching...`, `Answering...`) without blocking the core AI execution.

### 9. **Multi-Tasking (Multi-Command Execution)**
Jarvis can handle multiple commands in a single prompt! You can say things like *"Open Facebook, open Instagram and close WhatsApp"* and the intelligent Decision-Making Model will split and execute these tasks perfectly.

### 10. **Context Memory & History Awareness**
Jarvis maintains a dynamic memory of your current session. It reads and writes to a local chat log (`ChatLog.json` / `Database.data`) to keep track of the conversation history. This means you can ask follow-up questions and Jarvis will remember the context seamlessly.

---

## 🛠️ Architecture

- **`Frontend/`**: Contains `GUI.py` executing the PyQt5 graphical interface alongside graphical assets.
- **`Backend/`**: 
  - `Model.py`: Cohere-powered DMM logic.
  - `Chatbot.py`: Groq-powered conversational engine.
  - `Automation.py`: Automation utilities for system and web interactions.
  - `ImageGeneration.py`: Hugging Face API interface for image generation.
  - `RealtimeSearchEngine.py`: Live data scraping utility.
  - `SpeechToText.py` & `TextToSpeech.py`: Voice I/O handling.
- **`main.py`**: The central orchestrator that merges all features, handles multithreading, and manages continuous wake-word listening.

---

## ⚙️ Requirements & Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/hiteshraj786/Advanced-AI-Voice-Assistant.git
   cd Advanced-AI-Voice-Assistant
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r Requirements.txt
   ```
   *(Ensure you have `pyaudio`, `speech_recognition`, `PyQt5`, `groq`, `cohere`, `edge-tts`, and other libraries listed)*

3. **Environment Setup (`.env`):**
   You must create a `.env` file in the root directory and provide the necessary API keys:
   ```env
   Username=YourName
   Assistantname=Jarvis
   GroqAPIKey=your_groq_api_key_here
   CO_API_KEY=your_cohere_api_key_here
   HuggingFaceAPIKey=your_huggingface_api_key_here
   ```

4. **Run Jarvis:**
   ```bash
   python main.py
   ```

---

## 🎤 How to Use

- **Wake Word:** Start your interaction by saying **"Jarvis"**. The GUI status will change to `Listening...` indicating the mic is unlocked.
- **Conversations:** *"Jarvis, tell me a joke."*
- **Realtime Information:** *"Jarvis, who won the match yesterday?"*
- **Automation:** *"Jarvis, open Chrome and Spotify."* or *"Jarvis, close Notepad."*
- **Content Creation:** *"Jarvis, write an application for sick leave."*
- **Image Generation:** *"Jarvis, generate an image of a futuristic city."*

---

## 🤝 Contribution & License

Feel free to fork this repository, submit Pull Requests, or open Issues for new feature requests and bug fixes. 
Enjoy interacting with your personalized, local AI companion!
