
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QStackedWidget, QHBoxLayout,
                             QWidget, QFrame, QLabel, QPushButton, QSizePolicy)
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QFont, QTextCharFormat, QTextBlockFormat, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os
from Backend.path_helper import graphics_path, frontend_files
from dotenv import load_dotenv

mic_icon = graphics_path("Mic.png")
mic_data = frontend_files("Mic.data")

# ------------------- High DPI + Utility Scaling -------------------
# (ye attributes QApplication banne se pehle lagte hain)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

def _get_screen_metrics():
    # safer than deprecated QApplication.desktop()
    app = QApplication.instance()
    screen = app.primaryScreen()
    size = screen.size()
    w, h = size.width(), size.height()
    # 14-inch laptops commonly 1366x768 or 1920x1080
    # base ko 1920x1080 maana, scale = min(w/1920, h/1080)
    scale = min(w / 1920.0, h / 1080.0)
    # clamp taaki bahut chhote/bohot bade screens par bhi theek lage
    scale = max(0.75, min(1.25, scale))
    return w, h, scale

def dp(px):
    # device independent pixels
    _, _, s = _get_screen_metrics()
    return max(1, int(px * s))

def get_scaled_size(screen_width, fraction, min_size=24, max_size=120):
    # tumhara original helper; min/max ko dp se pass karo
    return max(dp(min_size), min(int(screen_width * fraction), dp(max_size)))

# ------------------- Safe Image Loader -------------------
def safe_load_icon(path, width=60, height=60):
    print("Trying to load image:", path)
    if os.path.exists(path):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"Loaded pixmap is null for {path}. Using blank pixmap instead.")
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.transparent)
        else:
            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap
    else:
        print(f"Image missing: {path}")
        blank_pixmap = QPixmap(width, height)
        blank_pixmap.fill(Qt.transparent)
        return blank_pixmap

# ------------------- Paths / Env -------------------
# env_vars = dotenv_values(".env")
# Assistantname = env_vars.get("Assistantname")
load_dotenv()

Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Fronted\Files"
GraphicsDirPath = rf"{current_dir}\Fronted\Graphics"
# TempDirPath = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Files"
# GraphicsDirPath = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Graphics"


def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

def ensure_file_exists(filepath, default_text=""):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(default_text)

# os.makedirs(TempDirPath, exist_ok=True)
# os.makedirs(GraphicsDirPath, exist_ok=True)

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you",
                      "what's", "where's", "how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

# def graphics_path(Filename):
#     Path = rf'{GraphicsDirPath}\{Filename}'
#     return Path

# def frontend_files(Filename):
#     Path = rf'{TempDirPath}\{Filename}'
#     return Path

def SetMicrophoneStatus(Command):
    # ensure_file_exists(frontend_files('mic_data'))
    ensure_file_exists(frontend_files('Mic.data'))
    with open(frontend_files("Mic.data"), "w", encoding="utf-8") as file:
        file.write(Command)

def GetMicrophoneStatus():
    ensure_file_exists(frontend_files('Mic.data'))
    with open(frontend_files("Mic.data"), "r", encoding='utf-8') as file:
        Status = file.read()
        return Status

def SetAssistantStatus(Status):
    ensure_file_exists(frontend_files('Status.data'))
    with open(frontend_files("Status.data"), "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    ensure_file_exists(frontend_files('Status.data'))
    with open(frontend_files("Status.data"), "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def ShowTextToScreen(Text):
    ensure_file_exists(frontend_files('Responses.data'))
    with open(frontend_files("Responses.data"), "w", encoding='utf-8') as file:
        file.write(Text)

# ------------------- Widgets -------------------
class ChatSection(QWidget):
    def loadMessages(self):
        global old_chat_message
        ensure_file_exists(frontend_files('Responses.data'))
        with open(frontend_files('Responses.data'), "r", encoding='utf-8') as file:
            messages = file.read()

        if not messages:
            return
        if len(messages) <= 1:
            return
        if str(old_chat_message) == str(messages):
            return

        self.addMessage(message=messages, color='white')
        old_chat_message = messages

    def SpeechRecogText(self):
        ensure_file_exists(frontend_files('Status.data'))
        with open(frontend_files('Status.data'), "r", encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        new_pixmap = safe_load_icon(path, width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(graphics_path('voice.png'), dp(60), dp(60))
            MicButtonInitialed()
        else:
            self.load_icon(graphics_path('Mic.png'), dp(60), dp(60))
            MicButtonClosed()
        self.toggled = not self.toggled

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(dp(10))
        formatm.setLeftMargin(dp(10))
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        w, h, _ = _get_screen_metrics()

        # margins & spacing responsive
        layout.setContentsMargins(dp(0), dp(0), dp(0), get_scaled_size(h, 0.07, 30, 120))
        layout.setSpacing(get_scaled_size(h, 0.02, 8, 24))

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        self.chat_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # font responsive
        font = QFont()
        font.setPointSize(max(10, dp(12)))
        self.chat_text_edit.setFont(font)

        layout.addWidget(self.chat_text_edit, 1)

        # # GIF (no fixed sizes; scaled)
        # self.gif_label = QLabel()
        # self.gif_label.setStyleSheet("border: none;")
        # movie = QMovie(graphics_path('Jarvis.gif'))
        # max_gif_size_W = dp(550)
        # max_gif_size_H = dp(360)
        # movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        # self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        # self.gif_label.setMovie(movie)
        # movie.start()
        # layout.addWidget(self.gif_label, 0, Qt.AlignRight | Qt.AlignBottom)

        # self.label = QLabel("")
       

  

        # 1) GIF
        self.gif_label = QLabel()
        movie = QMovie(graphics_path('Jarvis.gif'))
        movie.setScaledSize(QSize(550, 375))   # tumhara GIF size
        self.gif_label.setMovie(movie)
        movie.start()

        gif_w = movie.scaledSize().width()     # GIF width
        self.gif_label.setFixedWidth(gif_w)
        self.gif_label.setAlignment(Qt.AlignCenter)

        # 2) LISTENING label (GIF ke exactly neeche center)
        self.label = QLabel("")
        self.label.setText("")                 # runtime me update hota h
        self.label.setStyleSheet("color: cyan; font-size:18px;")
        self.label.setAlignment(Qt.AlignCenter)

        # same width as GIF so always center exactly below it
        self.label.setFixedWidth(gif_w)

        # 3) Vertical container (GIF upar, Listening neeche)
        self.media_container = QWidget()
        v = QVBoxLayout(self.media_container)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(5)

        v.addWidget(self.gif_label, 0, Qt.AlignCenter)
        v.addWidget(self.label, 0, Qt.AlignCenter)

        # 4) Ye container ko ChatSection ke bottom-right me laga do
        layout.addWidget(self.media_container, 0, Qt.AlignBottom | Qt.AlignRight)


        # Event filter + Scrollbar style
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
            QWidget { background-color: black; }
            QScrollBar:vertical { border: none; background: black; width: 10px; margin: 0; }
            QScrollBar::handle:vertical { background: white; min-height: 20px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { background: black; height: 10px; }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { border: none; background: none; color: none; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        """)

        # Icon (optional use)
        self.icon_label = QLabel()
        self.toggled = True

        # Timer throttled (100ms instead of 5ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(100)

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        w, h, _ = _get_screen_metrics()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(dp(0), dp(0), dp(0), get_scaled_size(h, 0.07, 30, 120))
        content_layout.setSpacing(get_scaled_size(h, 0.015, 8, 24))

        gif_label = QLabel()
        movie = QMovie(graphics_path('Jarvis.gif'))
        gif_width = int(w * 0.60)     
        gif_height = int(h * 0.65)   
        movie.setScaledSize(QSize(gif_width, gif_height))


        
       
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()

        self.icon_label = QLabel()
        mic_icon_size = get_scaled_size(w, 0.08, 60, 120)




        pixmap = safe_load_icon(graphics_path('Mic_on.png'), mic_icon_size, mic_icon_size)
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setFixedSize(mic_icon_size, mic_icon_size)  # icon clickable area
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon

        # self.label = QLabel("")
        # self.label.setStyleSheet(f"color: cyan; font-size:{max(14, dp(18))}px; margin-bottom:0;")
        self.label = QLabel("")
        self.label.setStyleSheet("""
            color: cyan;
            font-size: 20px;      /* size badha diya */
            font-weight: bold;    /* bold kar diya */
            margin-bottom: 0;
        """)
        self.label.setAlignment(Qt.AlignCenter)



        content_layout.addStretch(1)
        content_layout.addWidget(gif_label, 0, Qt.AlignCenter)
        content_layout.addSpacing(dp(5))
        content_layout.addWidget(self.label, 0, Qt.AlignCenter)
        content_layout.addSpacing(dp(5))
        content_layout.addWidget(self.icon_label, 0, Qt.AlignCenter)
        content_layout.addStretch(1)

        self.setLayout(content_layout)
        # ❌ Fixed size hataya; responsive banane ke liye policies:
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("background-color: black;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(100)  # throttled

    def SpeechRecogText(self):
        ensure_file_exists(frontend_files('Status.data'))
        with open(frontend_files('Status.data'), "r", encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        new_pixmap = safe_load_icon(path, width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(graphics_path('Mic_on.png'), dp(60), dp(60))
            MicButtonInitialed()
        else:
            self.load_icon(graphics_path('Mic_off.png'), dp(60), dp(60))
            MicButtonClosed()
        self.toggled = not self.toggled

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.initUI()
        self.current_screen = None

    def initUI(self):
        w, h, _ = _get_screen_metrics()
        topbar_icon_size = get_scaled_size(w, 0.03, 24, 40)

        self.setFixedHeight(dp(50))
        layout = QHBoxLayout(self)
        layout.setContentsMargins(dp(8), dp(4), dp(8), dp(4))
        layout.setAlignment(Qt.AlignRight)

        def mk_btn(icon_name, text=None):
            btn = QPushButton()
            icon = QIcon(graphics_path(icon_name))
            btn.setIcon(icon)
            btn.setIconSize(QSize(topbar_icon_size, topbar_icon_size))
            if text:
                btn.setText(f"  {text}")
            btn.setStyleSheet("height:40px; line-height:40px; background-color:white;font-weight: bold ; color:black;")
            btn.setCursor(Qt.PointingHandCursor)
            return btn

        home_button = mk_btn("Home.png", "Home")
        message_button = mk_btn("Chats.png", "Chat")

        minimize_button = mk_btn("Minimize2.png")
        minimize_button.clicked.connect(self.minimizeWindow)

        self.maximize_button = mk_btn("Maximize.png")
        self.maximize_icon = QIcon(graphics_path('Maximize.png'))
        self.restore_icon = QIcon(graphics_path('Minimize.png'))
        self.maximize_button.clicked.connect(self.maximizeWindow)

        close_button = mk_btn("Close.png")
        close_button.clicked.connect(self.closeWindow)

        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: black;")

        title_label = QLabel(f"{(Assistantname or 'Assistant').capitalize()} AI  ")
        title_label.setStyleSheet(f"color: black;font-weight: bold ; font-size:{max(18, dp(20))}px; background-color:white")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable = True
        self.offset = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset and not self.parent().isMaximized():
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        initial_screen = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)
        self.current_screen = initial_screen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        w, h, _ = _get_screen_metrics()

        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)

        # start maximized for 14-inch laptops; avoids fixed geometry
        self.resize(int(w * 0.9), int(h * 0.9))
        self.setStyleSheet("background-color: black;")

        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    # optionally set app-wide default font scaling
    _, _, s = _get_screen_metrics()
    base_font = QFont()
    base_font.setPointSizeF(9 * s + 2)  # thoda sa bump for readability
    app.setFont(base_font)

    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
      ensure_file_exists(frontend_files("Mic.data"))
      ensure_file_exists(frontend_files("Status.data"))
      ensure_file_exists(frontend_files("Responses.data"))

      GraphicalUserInterface()

