

from Frontend.GUI import (
GraphicalUserInterface,
SetAssistantStatus,
ShowTextToScreen,
# TempDirectoryPath,
SetMicrophoneStatus,
AnswerModifier,
QueryModifier,
GetMicrophoneStatus,
GetAssistantStatus )
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
import sys
PYTHON_EXE = sys.executable
from Backend.path_helper import data_path
import os

os.makedirs(data_path(), exist_ok=True)


# from Backend.path_helper import data_path, frontend_files, backend_path
from dotenv import load_dotenv
# from path_helper import data_path, frontend_files, backend_path
from Backend.path_helper import data_path, frontend_files, backend_path



import re
# global flag: set True once wakeword heard; stays True until app closed or you manually clear it
WakeUnlocked = False


WAKEWORD = "jarvis"
WAKE_REG = re.compile(rf"\b{re.escape(WAKEWORD)}\b", flags=re.IGNORECASE)
WAKE_LISTENING_PAUSE = 0.25


# env_vars = dotenv_values(".env")
# Username = env_vars.get("Username")
# Assistantname = env_vars.get("Assistantname")
load_dotenv()

Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")

DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may I assist you today?'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# def ShowDefaultChatIfNoChats():
#     File = open(data_path("ChatLog.json"),"r", encoding='utf-8')
#     if len(File.read())<5:
#         with open(data_path("Database.data"), 'w', encoding='utf-8') as file:
#             file.write("")

#         with open(data_path("Responses.data"), 'w', encoding='utf-8') as file:
#             file.write("DefaultMessage")


def ShowDefaultChatIfNoChats():
    chatlog = data_path("ChatLog.json")

    if not os.path.exists(chatlog):
        with open(chatlog, "w", encoding="utf-8") as f:
            f.write("[]")

    with open(chatlog, "r", encoding="utf-8") as File:
        if len(File.read()) < 5:
            with open(data_path("Database.data"), 'w', encoding='utf-8') as file:
                file.write("")

            with open(data_path("Responses.data"), 'w', encoding='utf-8') as file:
                file.write(DefaultMessage)


def ReadChatLogJson():
    with open(data_path("ChatLog.json"), 'r', encoding='utf-8') as file:
        chatlog_data = json.load(file)
    return chatlog_data

# def ReadChatLogJson():
#     try:
#         with open(data_path("ChatLog.json"), 'r', encoding='utf-8') as file:
#             return json.load(file)
#     except:
#         return []


def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n" 
    formatted_chatlog = formatted_chatlog.replace("User",Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant",Assistantname + " ")

    with open(data_path("Database.data"), "w", encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    File = open(data_path("Database.data"),"r", encoding='utf-8')
    Data = File.read()
    if len(str(Data))>0:
        lines = Data.split('\n')
        result = '\n'.join(lines)
        File.close()
        File = open(data_path("Responses.data"),"w", encoding='utf-8')
        File.write(result)
        File.close()
def WakeWordListener():
    """
    Minimal wake-word loop.
    - Only listens when microphone is not active (GetMicrophoneStatus() == "False")
    - Uses existing SpeechRecognition() function to capture short audio and checks for WAKEWORD.
    - If WAKEWORD found -> SetMicrophoneStatus("True") and show short text on GUI.
    """

    while True:
        try:
            # only listen for wakeword when mic is off / assistant available
            if GetMicrophoneStatus() == "False":
                # quick listen (SpeechRecognition may block until it gets something)
                # It must be safe: if SpeechRecognition returns None/"" it simply continues
                text = SpeechRecognition()
                if text:
                    txt = str(text).lower()
                    # check if wakeword is present as a whole word
                    # if WAKEWORD in txt.split():
                    #     print("Wakeword detected:", txt)
                    #     ShowTextToScreen(f"{Username} : {WAKEWORD} (wakeword detected)")
                    #     SetAssistantStatus("Listening...")
                    #     SetMicrophoneStatus("True")
                    #     # give FirstThread/MainExecution time to take over
                    #     # do not keep listening until helper resets mic
                    #     # small sleep to avoid immediate re-trigger
                    #     sleep(0.5)
                    # if WAKEWORD in txt.split():
                    #     print("Wakeword detected:", txt)
                    #     ShowTextToScreen(f"{Username} : {WAKEWORD} (wakeword detected)")
                    #     SetAssistantStatus("Listening...")
                    #     SetMicrophoneStatus("True")

                    #     # ==== ADD THESE LINES ====
                    #     global WakeUnlocked
                    #     WakeUnlocked = True
                    #     # ==========================

                    #     # small debounce so main captures actual command next
                    #     sleep(0.6)
                    if WAKEWORD in txt.split():
                        print("Wakeword detected:", txt)
                        ShowTextToScreen(f"{Username} : {WAKEWORD} (wakeword detected)")
                        SetAssistantStatus("Listening...")
                        SetMicrophoneStatus("True")

                        # ==== KEEP ASSISTANT UNLOCKED FOR CONTINUOUS LISTENING ====
                        global WakeUnlocked
                        WakeUnlocked = True
                        SetMicrophoneStatus("True")
                        # =========================================================

                        # ===== START MAINEXECUTION IMMEDIATELY IN BACKGROUND =====
                        # threading.Thread(target=MainExecution, daemon=True).start()
                        # =========================================================

                        # small debounce so main captures actual command next
                        sleep(0.6)


                    else:
                        # optional: very short sleep to avoid busy-looping
                        sleep(WAKE_LISTENING_PAUSE)
                else:
                    # nothing heard — wait a tiny bit
                    sleep(WAKE_LISTENING_PAUSE)
            else:
                # mic already True -> do not compete with MainExecution
                sleep(0.2)
        except Exception as e:
            # don't kill thread on transient errors; print for debugging
            print("WakeWordListener error:", e)
            sleep(0.5)


def InitializeExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitializeExecution()


# def MainExecution(initial_query=None):
#     """
#     If initial_query provided (string), use it directly instead of calling SpeechRecognition().
#     This allows WakeWordListener to pass the immediate command captured right after wakeword.
#     """


#     # SetAssistantStatus("Listening...")
#     # Query = SpeechRecognition()
#     # ShowTextToScreen(f"{Username} : {Query}")
#     # SetAssistantStatus("Thinking...")
#     # Decision = FirstLayerDMM(Query)


#     # SetAssistantStatus("Listening...")
#     # Query = SpeechRecognition()
#     # # show whatever came (None will be shown as 'None' but we'll handle below)
#     # ShowTextToScreen(f"{Username} : {Query}")
#     SetAssistantStatus("Listening...")
#     if initial_query is not None:
#         Query = initial_query
#     else:
#         Query = SpeechRecognition()

#     ShowTextToScreen(f"{Username} : {Query}")



#     # If speech recog failed or returned nothing, reset status & return early
#     # if not Query:
#     #     print("SpeechRecognition returned empty/None. Resetting status.")
#     #     SetAssistantStatus("Available...")
#     #     SetMicrophoneStatus("False")
#     #     return False

def MainExecution(initial_query=None):
    """
    If initial_query is provided, use it instead of calling SpeechRecognition().
    """

    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening...")
    if initial_query is not None:
        Query = initial_query
    else:
        Query = SpeechRecognition()

    # show whatever came (None will be shown as 'None' but we'll handle below)
    ShowTextToScreen(f"{Username} : {Query}")

    # If speech recog failed or returned nothing, reset status & return early
    if not Query:
        print("SpeechRecognition returned empty/None.")
        # if unlocked, keep listening (do not turn mic off) — just return
        if WakeUnlocked:
            SetAssistantStatus("Listening...")
            return False
        # else behave as before
        SetAssistantStatus("Available...")
        SetMicrophoneStatus("False")
        return False


#     if not Query:
#         print("SpeechRecognition returned empty/None.")
#         # if unlocked, keep listening (do not turn mic off) — just return
#         if WakeUnlocked:
#             SetAssistantStatus("Listening...")
#             return False
#         # else behave as before
#         SetAssistantStatus("Available...")
#         SetMicrophoneStatus("False")
#         return False


    SetAssistantStatus("Thinking...")
    # Protect the DMM call with try/except so a crash doesn't hang the GUI
    try:
        Decision = FirstLayerDMM(Query)
    except Exception as e:
        print("FirstLayerDMM raised exception:", e)
        SetAssistantStatus("Available...")
        SetMicrophoneStatus("False")
        # Optionally show a friendly message on UI
        ShowTextToScreen(f"{Assistantname} : Sorry, I couldn't process that. Try again.")
        return False


    print("")
    print(f"Decision : {Decision}")
    print("")

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])

    Merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    for queries in Decision:
        if "generate " in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True

    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True

    # if ImageExecution == True:

    #     with open(r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Fronted\Files\ImageGeneration.data", "w") as file:
    #         file.write(f"{ImageGenerationQuery},True")

    #     try:
    #         p1 = subprocess.Popen(['python', r'C:\Users\hites\OneDrive\Desktop\Voice Assistent\Backend\ImageGeneration.py'],
    #                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    #                                stdin=subprocess.PIPE, shell=False)
    #         subprocesses.append(p1)

    #     except Exception as e:
    #         print(f"Error starting ImageGeneration.py: {e}")
    if ImageExecution == True:
    # Clean ImageGenerationQuery to a prompt-only string
        raw = ImageGenerationQuery.strip()
        # remove leading keyword like "generate image" or "create image"
        lowered = raw.lower()
        if lowered.startswith("generate image"):
            prompt_to_write = raw[len("generate image"):].strip()
        elif lowered.startswith("create image"):
            prompt_to_write = raw[len("create image"):].strip()
        else:
            prompt_to_write = raw

        # remove trailing punctuation (dot) and extra commas
        prompt_to_write = prompt_to_write.rstrip(" .,")

        # if user only said a name like "Akshay Kumar", you may want to map to a lookalike descriptive prompt
        if "akshay" in prompt_to_write.lower():
            prompt_to_write = ("portrait of a South-Asian male film actor in his 40s, "
                            "short black hair, confident smile, cinematic studio lighting, photorealistic, high detail")

        # write the cleaned prompt (only) to file
        # data_path = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Fronted\Files\ImageGeneration.data"
        image_file = frontend_files("ImageGeneration.data")

        try:
            with open(image_file, "w", encoding="utf-8") as file:
                file.write(f"{prompt_to_write},True")
            print("Wrote ImageGeneration.data:", prompt_to_write)
        except Exception as e:
            print("Failed writing ImageGeneration.data:", e)

        # start image generator subprocess and show its stderr for debug
        try:
            p1 = subprocess.Popen(
                ['python', backend_path("ImageGeneration.py")]
,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=False
            )
            # debug: read a short stderr if it fails quickly (non-blocking attempt)
            try:
                out, err = p1.communicate(timeout=8)  # waits up to 8s
                if out:
                    print("ImageGen stdout:", out.decode(errors='ignore'))
                if err:
                    print("ImageGen stderr:", err.decode(errors='ignore'))
            except Exception:
                # if child takes longer, do not block; append to list so main can continue
                subprocesses.append(p1)
                print("ImageGeneration.py started (background).")
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    if G and R or R:

        SetAssistantStatus("Searching ...")
        Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(Answer)
        return True
    
    else:
        for Queries in Decision:

            if "general" in Queries:
                SetAssistantStatus("Thinking ...")
                QueryFinal = Queries.replace("general ","")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                return True
            
            elif "realtime" in Queries:
                SetAssistantStatus("Searching ...")
                QueryFinal = Queries.replace("realtime ","")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                return True
            
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                SetAssistantStatus("Answering ...")
                os._exit(1)

# def FirstThread():

#     while True:

#         CurrentStatus = GetMicrophoneStatus()

#         if CurrentStatus == "True":
#             MainExecution()

#         else:
#             AIStatus = GetAssistantStatus()

#             if "Available..." in AIStatus:
#                 sleep(0.1)

#             else:
#                 SetAssistantStatus("Available...")







def FirstThread():
    global WakeUnlocked
    while True:
        if WakeUnlocked:
            # keep microphone active for continuous conversation
            # ensure GUI shows Listening and let MainExecution handle each utterance
            try:
                SetAssistantStatus("Listening...")
                SetMicrophoneStatus("True")
                MainExecution()
            except Exception as e:
                print("Error in MainExecution (FirstThread):", e)
                # small sleep to avoid busy-looping on errors
                sleep(0.2)
        else:
            # existing behavior when locked
            CurrentStatus = GetMicrophoneStatus()
            if CurrentStatus == "True":
                MainExecution()
            else:
                AIStatus = GetAssistantStatus()
                if "Available..." in AIStatus:
                    sleep(0.1)
                else:
                    SetAssistantStatus("Available...")
sleep(0.05)


def SecondThread():

    GraphicalUserInterface()

# if __name__ == "__main__":
#     thread2 = threading.Thread(target=FirstThread, daemon=True)
#     thread2.start()
#     SecondThread()

if __name__ == "__main__":
    # Start wakeword listener thread (daemon)
    wake_thread = threading.Thread(target=WakeWordListener, daemon=True)
    wake_thread.start()

    # Start background FirstThread that runs MainExecution when mic is True
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()

    # Launch GUI (blocks)
    SecondThread()

