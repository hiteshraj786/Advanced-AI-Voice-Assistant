<p align="center">
  <img src="Frontend/Graphics/Jarvis.gif" alt="Jarvis AI" width="280"/>
</p>

<h1 align="center">🤖 J.A.R.V.I.S — Advanced AI Voice Assistant</h1>

<p align="center">
  <em>Your Personal Iron-Man Style AI — Talk, Automate, Search, Create.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/GUI-PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt5"/>
  <img src="https://img.shields.io/badge/AI-Cohere%20%7C%20Groq%20%7C%20HuggingFace-FF6F00?style=for-the-badge&logo=openai&logoColor=white" alt="AI"/>
  <img src="https://img.shields.io/badge/TTS-Edge--TTS-0078D4?style=for-the-badge&logo=microsoft&logoColor=white" alt="TTS"/>
  <img src="https://img.shields.io/badge/Search-SerpAPI-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Search"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/>
</p>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Feature Deep-Dive](#-feature-deep-dive)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Screenshots](#-screenshots)
- [How It Works — Under the Hood](#-how-it-works--under-the-hood)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)

---

## 🌟 Overview

**Jarvis** is a fully offline-capable, voice-activated AI assistant built from scratch in Python. It combines multiple AI models, real-time web intelligence, desktop automation, and a polished desktop GUI into a single cohesive application.

Unlike simple chatbot wrappers, Jarvis features a **multi-layered Decision-Making Model (DMM)** that understands user intent at the sentence level — routing each command to the right subsystem (chatbot, search engine, automation, image generation, etc.) automatically.

**Key Highlights:**
- 🗣️ **"Jarvis" Wake Word** — Always listening, activates hands-free
- 🧠 **Dual-AI Brain** — Cohere for intent classification + Groq (Llama-3.3-70B) for conversations
- 🌐 **Real-Time Web Search** — SerpAPI-powered Google results fed into AI for current answers
- 🖼️ **AI Image Generation** — Stable Diffusion XL via Hugging Face
- 🖥️ **Desktop Automation** — Open/close apps, control volume, play YouTube
- ✍️ **Content Writer** — Generates letters, emails, code & auto-opens in Notepad
- 🔁 **Multi-Task Execution** — Handle multiple commands in a single sentence
- 💬 **Context Memory** — Persistent chat history across sessions
- 🎨 **Premium PyQt5 GUI** — Animated, responsive, frameless desktop interface

---

## 🚀 Feature Deep-Dive

### 1. 🧠 Intelligent Decision-Making Model (DMM)
> **File:** `Backend/Model.py` · **Engine:** Cohere `command-a-03-2025`

The first layer of Jarvis. Every user query passes through a **Cohere-powered classifier** that decides the query type. The DMM uses a detailed preamble with 12+ categories and few-shot chat history examples to achieve high accuracy.

**Supported Classifications:**
| Category | Trigger Example | Action |
|---|---|---|
| `general` | *"What is quantum computing?"* | Routes to Groq Chatbot |
| `realtime` | *"Who is the current PM of India?"* | Routes to SerpAPI → Groq |
| `open` | *"Open Chrome and Spotify"* | Opens desktop apps/websites |
| `close` | *"Close Notepad"* | Closes running applications |
| `play` | *"Play Shape of You"* | Plays on YouTube via PyWhatKit |
| `generate image` | *"Generate image of a futuristic city"* | Triggers Stable Diffusion XL |
| `content` | *"Write a sick leave application"* | AI writes → saves → opens in Notepad |
| `google search` | *"Google search machine learning"* | Opens Google Search in browser |
| `youtube search` | *"YouTube search Python tutorial"* | Opens YouTube Search in browser |
| `system` | *"Volume up" / "Mute"* | Controls system volume via keyboard simulation |
| `reminder` | *"Remind me at 9PM about meeting"* | Stores reminder with datetime |
| `exit` | *"Bye Jarvis"* | Graceful shutdown with farewell |

**Multi-Command Parsing:** A single sentence like *"Open Facebook, Instagram and close WhatsApp"* gets split into `open facebook, open instagram, close whatsapp` — all executed concurrently via `asyncio.gather()`.

---

### 2. 💬 Conversational AI Chatbot
> **File:** `Backend/Chatbot.py` · **Engine:** Groq `llama-3.3-70b-versatile`

A streaming conversational engine that:
- Maintains **full chat history** in `Data/ChatLog.json` (persistent across sessions)
- Injects **real-time date/time context** into every request so Jarvis always knows the current day, date, and time
- Uses **streaming responses** for faster perceived latency
- Automatically **resets corrupted chat logs** and retries on failure
- Responds concisely — instructed not to over-explain or mention training data

---

### 3. 🌐 Real-Time Search Engine
> **File:** `Backend/RealtimeSearchEngine.py` · **Engine:** SerpAPI + Groq

For queries needing up-to-date information (news, current leaders, recent events):
1. Sends the query to **SerpAPI** (Google Search) to fetch organic results (titles + snippets)
2. Feeds those search results as system context into the **Groq Llama-3.3** model
3. The model synthesizes a professional, coherent answer from the raw search data
4. Answer is saved to persistent chat history

This gives Jarvis effectively **unlimited knowledge** — anything Google knows, Jarvis knows.

---

### 4. 🖼️ AI Image Generation
> **File:** `Backend/ImageGeneration.py` · **Engine:** Stable Diffusion XL (Hugging Face)

- Generates **2 high-resolution images** per request using `asyncio` for parallel API calls
- Each image uses a randomized seed for variety
- Prompts are enhanced with `"ultra realistic, 4k, high detail"` suffix
- Generated images are saved locally in `Data/` and auto-displayed using PIL
- Runs as a **separate subprocess** to avoid blocking the main thread
- Triggered via a file-based IPC mechanism (`Frontend/Files/ImageGeneration.data`)

---

### 5. 🖥️ Desktop & Web Automation
> **File:** `Backend/Automation.py` · **Engine:** AppOpener, PyWhatKit, Keyboard

A powerful automation layer that handles:

| Action | Implementation |
|---|---|
| **Open Apps** | `AppOpener` with `match_closest=True` → fallback to `https://www.{app}.com` |
| **Close Apps** | `AppOpener.close()` with fuzzy matching |
| **Play Music/Video** | `pywhatkit.playonyt()` — plays first YouTube result |
| **YouTube Search** | Opens YouTube search URL in default browser |
| **Google Search** | `pywhatkit.search()` — opens Google results |
| **Content Writing** | Groq AI generates content → saved to `.txt` → opens in Notepad |
| **System Controls** | `keyboard` module simulates volume up/down/mute keys |

All automation tasks are dispatched via `asyncio.to_thread()` and gathered with `asyncio.gather()` for **true concurrent multi-tasking**.

---

### 6. 🎤 Speech Recognition (STT)
> **File:** `Backend/SpeechToText.py` · **Engine:** Chrome WebSpeech API via Selenium

An innovative approach to speech recognition:
- Dynamically generates an HTML page with the **Web Speech API** (`webkitSpeechRecognition`)
- Opens it in a **headless Chrome browser** via Selenium WebDriver
- Polls the DOM for recognized text with configurable `timeout` (8s) and `poll_interval` (0.15s)
- Supports **multi-language input** — configurable via `InputLanguage` in `.env`
- Auto-translates non-English speech to English using `mtranslate`
- Uses `QueryModifier()` to properly punctuate and capitalize all recognized text

---

### 7. 🔊 Text-to-Speech (TTS)
> **File:** `Backend/TextToSpeech.py` · **Engine:** Microsoft Edge TTS + Pygame

- Uses **Edge-TTS** for high-quality, natural-sounding neural voices
- Configurable voice (default: `en-CA-LiamNeural`), pitch (`+5Hz`), and rate (`+13%`)
- Each audio file gets a **unique UUID filename** to prevent file-locking issues
- **Smart long-text handling:** If response > 4 sentences / 250 characters, Jarvis speaks the first 2 sentences and says *"The rest is on the chat screen"*
- Audio files are **auto-cleaned** after playback in the `finally` block
- Playback managed via `pygame.mixer` with 10fps tick loop

---

### 8. 🎨 Premium Desktop GUI
> **File:** `Frontend/GUI.py` · **Engine:** PyQt5

A frameless, fully custom desktop application featuring:

- **Two Screens:** Home Screen (animated Jarvis GIF + mic button) & Chat Screen (scrollable message history)
- **Custom Title Bar:** Draggable window with Home, Chat, Minimize, Maximize, Close buttons
- **Animated Jarvis GIF:** 6MB animated visualization centered on screen
- **Responsive Design:** Auto-scales based on screen resolution using `dp()` (density-independent pixels) — works on 1366×768 to 4K displays
- **High-DPI Support:** `AA_EnableHighDpiScaling` and `AA_UseHighDpiPixmaps` enabled
- **Real-Time Status Labels:** Displays `Listening...`, `Thinking...`, `Searching...`, `Answering...`, `Translating...`
- **Mic Toggle Button:** Visual on/off states (`Mic_on.png` / `Mic_off.png`)
- **100ms Timer Polling:** Chat messages and status labels refresh every 100ms via `QTimer`
- **Dark Theme:** Pure black background with white text and cyan accent labels

---

### 9. 🗣️ Wake Word Detection
> **File:** `main.py` · **Keyword:** `"Jarvis"`

- Runs on a **dedicated daemon thread** (`WakeWordListener`)
- Continuously listens via `SpeechRecognition()` when mic is off
- Uses regex-based whole-word matching: `\bjarvis\b`
- On detection: activates mic, sets status to `Listening...`, and unlocks **continuous conversation mode**
- Once unlocked (`WakeUnlocked = True`), Jarvis keeps listening without needing the wake word again

---

### 10. 🔁 Multi-Tasking & Concurrent Execution

Jarvis handles multiple tasks from a single command seamlessly:

```
User: "Open Chrome, play Shape of You, and search Python on Google"
```

**Internal Flow:**
1. DMM splits into: `open chrome`, `play shape of you`, `google search python`
2. Each task is wrapped in `asyncio.to_thread()`
3. All tasks execute **concurrently** via `asyncio.gather()`
4. Results are yielded back through an async generator

---

### 11. 🧠 Persistent Context Memory

- **Chat History:** All conversations stored in `Data/ChatLog.json` — survives restarts
- **GUI Sync:** Chat history is formatted and written to `Data/Database.data` → `Data/Responses.data` for GUI display
- **Chat Log Cleaner:** `Backend/clean_chatlog.py` utility removes stale system messages and creates backups
- **Session Continuity:** Follow-up questions like *"Tell me more about him"* work because prior context is passed to the AI

---

### 12. 📦 Standalone Executable Support

- Includes a `main.spec` (PyInstaller) configuration for building a **single-file `.exe`**
- Bundles `Backend/`, `Frontend/`, `Data/`, and `.env` into the executable
- Console-less (`console=False`) for a clean user experience
- UPX compression enabled for smaller file size

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        main.py (Orchestrator)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │ WakeWord     │  │ FirstThread  │  │ SecondThread          │  │
│  │ Listener     │  │ (Main Loop)  │  │ (PyQt5 GUI)           │  │
│  │ (daemon)     │  │ (daemon)     │  │ (blocking)            │  │
│  └──────┬───────┘  └──────┬───────┘  └───────────────────────┘  │
│         │                 │                                      │
│         ▼                 ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              SpeechRecognition (STT)                     │    │
│  │         Selenium + Chrome WebSpeech API                  │    │
│  └──────────────────────┬──────────────────────────────────┘    │
│                         │ User Query                             │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │           FirstLayerDMM (Cohere Command Model)           │    │
│  │         Intent Classification & Command Parsing          │    │
│  └──┬──────┬──────┬──────┬──────┬──────┬──────┬───────────┘    │
│     │      │      │      │      │      │      │                  │
│     ▼      ▼      ▼      ▼      ▼      ▼      ▼                  │
│  general realtime open  close  play  image  system               │
│     │      │      │      │      │      │      │                  │
│     ▼      ▼      ▼      │      │      │      │                  │
│  Chatbot  Search  App    App   YouTube HF     Keyboard           │
│  (Groq)  (Serp)  Opener Closer PyWhtKt SDXL   Sim               │
│     │      │                                                     │
│     ▼      ▼                                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │             TextToSpeech (Edge-TTS + Pygame)             │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

**Threading Model:**
| Thread | Role | Type |
|---|---|---|
| `WakeWordListener` | Listens for "Jarvis" wake word | Daemon |
| `FirstThread` | Runs `MainExecution()` loop — processes commands | Daemon |
| `SecondThread` | Runs PyQt5 GUI (blocks main thread) | Main |
| `ImageGeneration.py` | Runs as a separate subprocess for image creation | Subprocess |

---

## 🧰 Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.10+ | Core runtime |
| **Intent Classification** | Cohere `command-a-03-2025` | Query categorization (DMM) |
| **Conversational AI** | Groq `llama-3.3-70b-versatile` | Chatbot & content generation |
| **Image Generation** | Hugging Face Stable Diffusion XL | Text-to-image synthesis |
| **Web Search** | SerpAPI (Google) | Real-time information retrieval |
| **Speech-to-Text** | Chrome WebSpeech API (via Selenium) | Voice recognition |
| **Text-to-Speech** | Microsoft Edge-TTS + Pygame | Voice output |
| **Desktop GUI** | PyQt5 | Frameless, animated interface |
| **App Automation** | AppOpener | Open/close desktop applications |
| **YouTube** | PyWhatKit | Play videos & perform searches |
| **Volume Control** | Keyboard (Python) | System volume mute/unmute/up/down |
| **Translation** | mtranslate | Multi-language input support |
| **Web Scraping** | BeautifulSoup4 | Fallback HTML parsing |
| **Browser Control** | Selenium + ChromeDriver | Headless speech recognition |
| **Packaging** | PyInstaller | Standalone `.exe` build |

---

## 📂 Project Structure

```
📦 Advanced-AI-Voice-Assistant/
├── 📄 main.py                    # Entry point — orchestrator, threading, wake word
├── 📄 Requirements.txt           # All Python dependencies
├── 📄 main.spec                  # PyInstaller build configuration
├── 📄 .env                       # API keys & configuration (not committed)
├── 📄 .gitignore                 # Git ignore rules
│
├── 🗂️ Backend/
│   ├── Model.py                  # Cohere DMM — intent classification
│   ├── Chatbot.py                # Groq conversational engine
│   ├── RealtimeSearchEngine.py   # SerpAPI search + Groq synthesis
│   ├── Automation.py             # App/web/system automation
│   ├── ImageGeneration.py        # Stable Diffusion XL image generator
│   ├── SpeechToText.py           # Selenium-based speech recognition
│   ├── TextToSpeech.py           # Edge-TTS voice output
│   ├── path_helper.py            # Centralized path resolution utility
│   ├── clean_chatlog.py          # Chat log maintenance utility
│   └── __init__.py
│
├── 🗂️ Frontend/
│   ├── GUI.py                    # PyQt5 full GUI — responsive, animated
│   ├── __init__.py
│   ├── 🗂️ Files/                 # Runtime IPC data files
│   │   ├── Mic.data              # Microphone on/off state
│   │   ├── Status.data           # Assistant status text
│   │   ├── Responses.data        # Chat display content
│   │   ├── Database.data         # Formatted chat history
│   │   └── ImageGeneration.data  # Image generation trigger
│   └── 🗂️ Graphics/             # UI assets
│       ├── Jarvis.gif            # Main animated visualization (6MB)
│       ├── Mic.png / Mic_on.png / Mic_off.png
│       ├── Home.png / Chats.png
│       ├── Close.png / Maximize.png / Minimize2.png
│       └── voice.png
│
└── 🗂️ Data/                     # Runtime data (gitignored)
    ├── ChatLog.json              # Persistent conversation history
    ├── Voice.html                # Auto-generated STT page
    └── *.mp3 / *.jpg / *.txt     # Generated speech, images, content
```

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.10+** installed
- **Google Chrome** installed (required for speech recognition)
- **Microphone** connected and working
- API keys for: **Cohere**, **Groq**, **SerpAPI**, **Hugging Face**

### Step 1: Clone the Repository
```bash
git clone https://github.com/hiteshraj786/Advanced-AI-Voice-Assistant.git
cd Advanced-AI-Voice-Assistant
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r Requirements.txt
```

### Step 4: Create `.env` File
Create a `.env` file in the project root:
```env
# User Identity
Username=YourName
Assistantname=Jarvis

# AI API Keys
CohereAPIKey=your_cohere_api_key
GroqAPIKey=your_groq_api_key
SerpAPIKey=your_serpapi_key
HuggingFaceAPIKey=your_huggingface_api_key

# Voice Configuration
InputLanguage=en
AssistantVoice=en-CA-LiamNeural
```

### Step 5: Launch Jarvis
```bash
python main.py
```

---

## 🔧 Configuration

| Variable | Description | Default |
|---|---|---|
| `Username` | Your name (used in conversations) | — |
| `Assistantname` | Assistant's name | `Jarvis` |
| `CohereAPIKey` | Cohere API key for DMM | — |
| `GroqAPIKey` | Groq API key for chatbot | — |
| `SerpAPIKey` | SerpAPI key for real-time search | — |
| `HuggingFaceAPIKey` | HF key for image generation | — |
| `InputLanguage` | Speech input language code | `en` |
| `AssistantVoice` | Edge-TTS voice name | `en-CA-LiamNeural` |

**Popular Voice Options:**
- `en-US-JennyNeural` (Female, US)
- `en-CA-LiamNeural` (Male, Canadian)
- `en-CA-ClaraNeural` (Female, Canadian)
- `en-GB-SoniaNeural` (Female, British)
- `en-IN-NeerjaNeural` (Female, Indian)

---

## 🎤 Usage Guide

### Starting a Session
1. Launch `python main.py` — the GUI opens maximized
2. Say **"Jarvis"** to activate (or click the microphone button)
3. Once activated, Jarvis enters **continuous listening mode** — no need to say "Jarvis" again

### Example Commands

| What You Say | What Jarvis Does |
|---|---|
| *"Jarvis"* | 🔓 Activates and starts listening |
| *"What is machine learning?"* | 💬 Answers via Groq AI chatbot |
| *"Who won the IPL 2024?"* | 🌐 Searches Google via SerpAPI → synthesizes answer |
| *"Open Chrome and Spotify"* | 🖥️ Opens both apps simultaneously |
| *"Close Notepad"* | ❌ Closes the application |
| *"Play Shape of You"* | 🎵 Plays on YouTube |
| *"Generate image of a sunset over mountains"* | 🖼️ Creates 2 AI images via Stable Diffusion |
| *"Write a sick leave application"* | ✍️ Generates text → saves to file → opens in Notepad |
| *"Volume up" / "Mute"* | 🔊 Controls system volume |
| *"Search Python tutorial on YouTube"* | 🔍 Opens YouTube search results |
| *"Bye Jarvis"* | 👋 Says goodbye and exits |

### Multi-Command Example
```
"Open Facebook, play Believer by Imagine Dragons, and write an email to my boss"
```
Jarvis will: open Facebook + play Believer on YouTube + generate the email — all concurrently!

---

## 🔍 How It Works — Under the Hood

### Query Flow (from voice to response):

```
🎤 User speaks
    │
    ▼
📋 SpeechRecognition() — Selenium polls Chrome WebSpeech API
    │
    ▼
📝 QueryModifier() — Capitalizes, adds punctuation
    │
    ▼
🧠 FirstLayerDMM() — Cohere classifies intent
    │
    ├─ "general ..." ────► ChatBot() ──► Groq streams answer
    ├─ "realtime ..." ──► RealtimeSearchEngine() ──► SerpAPI + Groq
    ├─ "open ..." ──────► Automation() ──► AppOpener / webbrowser
    ├─ "play ..." ──────► PlayYoutube() ──► pywhatkit
    ├─ "generate image" ► ImageGeneration subprocess ──► HuggingFace
    ├─ "content ..." ───► Content() ──► Groq writes + opens Notepad
    ├─ "system ..." ────► System() ──► keyboard module
    └─ "exit" ──────────► Farewell + os._exit()
    │
    ▼
🔊 TextToSpeech() — Edge-TTS generates audio → Pygame plays it
    │
    ▼
📺 GUI updates — Status, chat messages refresh via QTimer (100ms)
```

### Inter-Process Communication (IPC):
The GUI and backend communicate through lightweight **file-based IPC**:
- `Mic.data` — microphone on/off toggle
- `Status.data` — current status label text
- `Responses.data` — latest chat message to display
- `ImageGeneration.data` — image prompt + trigger flag

---

## 🗺️ Roadmap

- [ ] Add reminder/alarm functionality with system notifications
- [ ] Integrate Whisper model for offline speech recognition
- [ ] Add support for smart home device control (IoT)
- [ ] Implement plugin system for extensibility
- [ ] Add voice authentication for personalized access
- [ ] Build a web-based interface alongside the desktop GUI
- [ ] Add screen reading / OCR capabilities

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. **Fork** this repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  <strong>Built with ❤️ by <a href="https://github.com/hiteshraj786">Hitesh Purohit</a></strong>
</p>

<p align="center">
  ⭐ If you like this project, give it a star! ⭐
</p>
