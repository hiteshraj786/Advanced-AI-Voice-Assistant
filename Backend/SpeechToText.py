






from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager 
from dotenv import dotenv_values
import os 
import mtranslate as mt
import time
from Backend.path_helper import data_path, frontend_files

#  Load environment variables from the .env file. 
env_vars = dotenv_values(".env")
#  Get the input language setting from the environment variables. 
# InputLanguage = env_vars.get("InputLanguage")
InputLanguage = (env_vars.get("InputLanguage") or "en").strip()


# Define the HTML code for the speech recognition interface. 
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with the input language from the environment variables.
HtmlCode  = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# # write the modified HTML code to a file. 
# with open(r"Data\Voice.html","w") as f:
#     f.write(HtmlCode)

# ensure folder exists, then write HTML
voice_html = data_path("Voice.html")
os.makedirs(os.path.dirname(voice_html), exist_ok=True)

with open(voice_html, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# #  Get the current working directory. 
# current_dir = os.getcwd()
# #  Generate the file path for HTML file. 
# Link = f"{current_dir}/Data/Voice.html"


Link = voice_html

#  Set Chrome options for the WebDriver 
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")



#  Initialize the Chrome WebDriver using the ChromeDriverManager. 
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options= chrome_options)

#  Define the path for temporary files. 
# TempDirPath = rf"{current_dir}/Frontend/Files"

#  Function to set the assistant's status by writing it to a file. 
# def SetAssistantStatus(Status):
#     with open(rf'{TempDirPath}/Status.data',"w",encoding = 'utf-8') as file:
#         file.write(Status)
def SetAssistantStatus(Status):
    path = frontend_files("Status.data")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w",encoding="utf-8") as file:
        file.write(Status)

#  Function to modify a query to ensure proper punctuation and formatting. 
# def QueryModifier(Query):
#     new_query = Query.lower().strip()
#     query_words = new_query.split()
#     question_words = ["how","what","who","where","why","which","whose","whom","can you","what's","how's","can you"]

#     #  Check if the query is a question and add a question mark if necessary. 
#     if any(word + "" in new_query for word in question_words):
#         if query_words[-1][-1] + ['.','?','!']:
#             new_query = new_query[:-1] + "?"

#         else:
#             new_query += "?"
#     else:
#         #  Add a period if the query is not a question. 
#         if query_words[-1][-1] in ['.','?','!']:
#             new_query = new_query[:-1] + "."
#         else: 
#             new_query += '.'

#     return new_query.capitalize()

def QueryModifier(Query):
    if not Query:
        return ""
    new_query = Query.strip()
    qwords = ("how","what","who","where","why","which","whose","whom","can","could","would","is","are","do","does")
    first = new_query.split()[0].lower()
    last = new_query[-1]
    if first in qwords:
        if last not in ".?!":
            new_query += "?"
    else:
        if last not in ".?!":
            new_query += "."
    return new_query[0].upper() + new_query[1:]


#  Function to translate text into English using the mtranslate library. 
def UniversalTranslator(Text):
    english_transition = mt.translate(Text,"en","auto")
    return english_transition.capitalize()

#  Function to perform speech recognition using the WebDriver. 
# def SpeechRecognition():
#     #  Open the HTML file in the browser. 
#     driver.get("file:///" + Link)
#     #  Start speech recognition by clicking the start button. 
#     driver.find_element(by=By.ID,value = "start").click()
    
#     while True:
#         try:
#             #  Get the recognized text form the HTML output element. 
#             Text = driver.find_element(by=By.ID, value="end").click()

#             if Text:
#                 #  Stop recognition by clicking the stop button. 
#                 driver.find_element(by=By.ID, value="end").click()

#                 #  If the input language is English, return the modified query. 
#                 if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
#                     return QueryModifier(Text)
#                 else:
#                     #  If the input language is not English, translate the text and return it. 
#                     SetAssistantStatus("Translating...")
#                     return QueryModifier(UniversalTranslator(Text))
                
#         except Exception as e:
#             pass

def SpeechRecognition(timeout=8, poll_interval=0.15):     # you also use for better recognition --> timout= 20 and poll_interval = 0.4
    # Open the HTML file in the browser.
    driver.get("file:///" + Link.replace("\\", "/"))
    time.sleep(0.5)  # let page load

    # Click start
    try:
        driver.find_element(By.ID, "start").click()
    except Exception as e:
        print("Could not click start:", e)
        return None

    start_time = time.time()
    recognized = ""
    # poll the output element until non-empty or timeout
    while time.time() - start_time < timeout:
        try:
            out = driver.find_element(By.ID, "output").text.strip()
            if out:
                recognized = out
                break
        except Exception:
            pass
        time.sleep(poll_interval)

    # try to stop recognition gracefully
    try:
        driver.find_element(By.ID, "end").click()
    except Exception:
        pass

    if not recognized:
        return None

    # translate if needed
    if "en" not in InputLanguage.lower():
        SetAssistantStatus("Translating...")
        return QueryModifier(UniversalTranslator(recognized))
    else:
        return QueryModifier(recognized)


#  Main execution block. 
if __name__ == "__main__":
    while True:
        #  Continuously perform speech recognition and print the recognized text. 
        Text = SpeechRecognition()
        print(Text)


