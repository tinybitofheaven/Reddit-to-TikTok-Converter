import sys
import reddit_scraper, settings
from final_video_creation import create_final_video

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QLineEdit, QVBoxLayout,QWidget, QRadioButton, QPushButton, QInputDialog,QFileDialog
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt,QRect
from utils import create_folders, clear_folders

class MainWindow(QMainWindow):

    def setupUi(self,Form):
        super(MainWindow, self).__init__()

        Form.setObjectName("Form")
        Form.resize(519, 344)

        self.setWindowTitle("RedditScraper")
        window_width, window_height = 230, 200
        self.setMinimumSize(window_width, window_height)

        #Changes scraping selection to user-submitted subreddit
        self.option_hot = QRadioButton()
        self.option_hot.setText("Hot Subreddit")
        self.option_hot.setChecked(True)
        
        #Changes scraping selection to user-submitted URL
        self.option_url = QRadioButton()
        self.option_url.setText("Post URL")
        self.option_url.setChecked(False)

        #Textbox for submitting specific subreddits
        self.subreddit_name = QLineEdit()
        self.subreddit_name.setPlaceholderText("Enter Subreddit Name Here")

        #TextBox for Url
        self.post_url = QLineEdit()
        self.post_url.setPlaceholderText("Enter Post URL Here")
        self.post_url.setDisabled(True)

        #Connections for radio buttons & respective text boxes
        self.option_hot.toggled.connect(self.on_check)

        #TextBox for download directory
        self.download_directory = QLineEdit()
        self.download_directory.setPlaceholderText("Enter Download Directory Here")

        #TextBox for file name
        self.file_name = QLineEdit()
        self.file_name.setPlaceholderText("Enter file Name Here")
        
        #Push Button for opening Video file
        self.file_button = QPushButton()
        self.file_button.setText("File Upload")
        self.file_button.setGeometry(QRect(80, 130, 113, 32))
        self.file_button.setStyleSheet("background-color:blue;\n"
                                       "color: white;\n"
                                       "border-style: outset;\n"
                                       "border-width:2px;\n"
                                       "border-radius:10px;\n"
                                       "border-color:black;\n"
                                       "font:bold 14px;\n"
                                       "padding :6px;\n"
                                       "min-width:10px;\n"
                                       "\n"
                                       "\n"
                                       ""
        )

        #Submission Button
        self.submit_button = QPushButton()
        self.submit_button.setText("Submit")
        self.submit_button.setGeometry(QRect(80, 130, 113, 32))
        self.submit_button.setStyleSheet("background-color:gray;\n"
                                         "color: white;\n"
                                         "border-style: outset;\n"
                                         "border-width:2px;\n"
                                         "border-radius:10px;\n"
                                         "border-color:black;\n"
                                         "font:bold 14px;\n"
                                         "padding :6px;\n"
                                         "min-width:10px;\n"
                                         "\n"
                                         "\n"
                                         "")

        #Submission Button Connections
        self.submit_button.released.connect(self.submit_scrape)

        #Linear Vertical Layout for widgets
        layout = QVBoxLayout() 
        layout.addWidget(self.option_hot)
        layout.addWidget(self.option_url)
        layout.addWidget(self.subreddit_name)
        layout.addWidget(self.post_url)
        layout.addWidget(self.download_directory)
        layout.addWidget(self.file_name)
        layout.addWidget(self.file_button)
        layout.addWidget(self.submit_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, form): #Main File Button Handler
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.file_button.setText(_translate("Form", "Browse File"))
        self.file_button.clicked.connect(self.pushButton_handler)

    def pushButton_handler(self): #Calls File Retrieval
        self.open_dialog_box()

    def open_dialog_box(self): #Handles Opening the dialogue box for retrieving path of selected object.
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        settings.BACKGROUND_VIDEO_PATH = path

    def show_state(self, s):
        print(s == Qt.CheckState.Checked)
        print(s)

    #disable the secondary url textbox if subreddit option is selected
    def on_check(self, is_toggle):
        if is_toggle:
            self.subreddit_name.setDisabled(False)
            self.post_url.setDisabled(True)
        else:
            self.post_url.setDisabled(False)
            self.subreddit_name.setDisabled(True)

    #Submission Button Resolved
    def submit_scrape(self):
        if(self.option_hot.isChecked): #If User selects the 'subreddit' option, it will generate the video(s) from the subreddit's 'hot' list.
            if(self.subreddit_name.text() != ""): #If the User provides their own subreddit
                reddit_scraper.SUBREDDIT = self.subreddit_name.text()
                if(reddit_scraper.check_subreddit_valid()):
                    self.threads = reddit_scraper.get_threads_from_subreddit(reddit_scraper.SUBREDDIT, reddit_scraper.POST_LIMIT)
                    self.call_video_creation()
            else:
                    self.threads = reddit_scraper.get_threads_from_subreddit(reddit_scraper.SUBREDDIT,reddit_scraper.POST_LIMIT) #If User leaves the text blank, default to AmITheAsshole
                    self.call_video_creation()
        elif(self.option_url.isChecked): #User chose to submit their own url
            reddit_scraper.SUBREDDIT = self.option_url.text()
            self.threads = reddit_scraper.get_thread_from_url(reddit_scraper.SUBREDDIT)
            self.call_video_creation()
        app.exit()

    #Calls for creation of video
    def call_video_creation(self):
        clear_folders(self.threads[0])
        create_folders(self.threads[0])
        if(self.download_directory.text()!= ''): #Sets download directory
            settings.FINAL_VIDEOS_PATH = self.download_directory.text()
        #if(self.file_name.text()!= ''):= 
        create_final_video(self.threads[0])

app = QApplication(sys.argv)
Form = QtWidgets.QWidget()
ui = MainWindow()
ui.setupUi(Form)
ui.show()
app.exec()