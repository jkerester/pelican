import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QWidget, QPushButton,QInputDialog, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QMainWindow):
    text = ''
    def __init__(self):
        super().__init__()
        self.title = 'Pelican GUI'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 940
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Create boxes for entries
        self.titlelabel = QLabel('Where do you want to create your new website?',self)
        self.titlelabel.move(20, 50)
        self.titlelabel.resize(300,50)
        self.titletextbox = QLineEdit(self)
        self.titletextbox.move(330, 50)
        self.titletextbox.resize(280, 40)
        #------------
        self.authorlabel = QLabel('Who will be the author of this web site?', self)
        self.authorlabel.move(20, 100)
        self.authorlabel.resize(300, 50)
        self.authortextbox = QLineEdit(self)
        self.authortextbox.move(330, 100)
        self.authortextbox.resize(280, 40)
        #------------
        self.languagelabel = QLabel('What will be the default language of this web site?',self)
        self.languagelabel.move(20, 150)
        self.languagelabel.resize(300, 50)
        self.languagetextbox = QLineEdit(self)
        self.languagetextbox.move(330, 150)
        self.languagetextbox.resize(280, 40)
        #------------
        self.urllabel = QLabel('Do you want to specify a URL prefix? (y/n)', self)
        self.urllabel.move(20, 190)
        self.urllabel.resize(300, 50)
        self.egurllabel = QLabel(' e.g., https://example.com ', self)
        self.egurllabel.move(20, 220)
        self.egurllabel.resize(300, 50)
        self.urlyesbutton = QPushButton('Yes', self)
        self.urlyesbutton.move(330, 200)
        self.urlyesbutton.clicked.connect(self.yesquestion)

        #------------
        self.paglabel = QLabel(
            'Do you want to enable article pagination?',
            self)
        self.paglabel.move(20, 250)
        self.paglabel.resize(300, 50)
        self.helplabel = QLabel(
            '(If no move on)',
            self)
        self.helplabel.move(500, 190)
        self.helplabel.resize(120, 50)
        self.pagyesbutton = QPushButton('Yes', self)
        self.pagyesbutton.move(330, 250)
        self.pagyesbutton.clicked.connect(self.yesquestion)
        self.egurllabel = QLabel('How many?', self)
        self.egurllabel.move(20, 270)
        self.egurllabel.resize(300, 50)
        #------------
        self.autlabel = QLabel('Do you want to generate a tasks.py/Makefile to automate generation and publishing?', self)
        self.autlabel.move(20, 300)
        self.autlabel.resize(500, 50)
        self.autyesbutton = QPushButton('Yes', self)
        self.autyesbutton.move(560, 310)
        self.autyesbutton.clicked.connect(self.autyes)
        #----

        #------------
        # Create a button in the window
        self.button = QPushButton('Continue', self)
        self.button.move(550, 680)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def yesquestion(self):
        text, ok = QInputDialog.getText(self, 'Specify',
                                        'Specify')
        self.text = text
    def autyes(self):
        ftp, ftpok = QInputDialog.getText(self, 'FTP',
                                          'Do you want to upload your website using FTP?(y/n)')
        if ftp == 'y':
            ftp_host, ftp_hostok = QInputDialog.getText(self, 'FTP',
                                                        'What is the hostname of your FTP server?')
            ftp_user, ftp_userok = QInputDialog.getText(self, 'FTP',
                                                        'What is your username on that server?')
            ftp_target_dir, ftp_target_dirok = QInputDialog.getText(self,
                                                                    'FTP',
                                                                    'Where do you want to put your web site on that server?')

        ssh, ftpok = QInputDialog.getText(self, 'SSH',
                                          'Do you want to upload your website using SSH?(y/n)')
        if ssh == 'y':
            ssh_host, ssh_hostok = QInputDialog.getText(self, 'SSH',
                                                        'What is the hostname of your SSH server?')
            ssh_port, ssh_portok = QInputDialog.getText(self, 'SSH',
                                                        'What is the port of your SSH server?')
            ssh_user, ssh_userok = QInputDialog.getText(self, 'SSH',
                                                        'What is your username on that server?')
            ssh_target_dir, ssh_target_dirok = QInputDialog.getText(self,
                                                                    'SSH',
                                                                    'Where do you want to put your web site on that server?')

        drop, dropok = QInputDialog.getText(self, 'Drop Box',
                                          'Do you want to upload your website using Dropbox?(y/n)')
        if drop == 'y':
            dropbox_dir, dropbox_dirok = QInputDialog.getText(self, 'Drop Box',
                                                        'Where is your Dropbox directory?')

        s, dropok = QInputDialog.getText(self, 'S3',
                                        'Do you want to upload your website using S3?(y/n)')
        if s == 'y':
            s_bucket, s_bucketok = QInputDialog.getText(self, 'S3',
                                                        'What is the name of your S3 bucket?')

        cloud, cloudok = QInputDialog.getText(self, 'Cloud',
                                          'Do you want to upload your website using Rackspace Cloud Files?(y/n)')
        if cloud == 'y':
            cloudfiles_username, cloudfiles_usernameok = QInputDialog.getText(self, 'Cloud',
                                                        'What is your Rackspace Cloud username?')
            cloudfiles_api_key, cloudfiles_api_keyok = QInputDialog.getText(self, 'Cloud',
                                                        'What is your Rackspace '
                                             'Cloud API key?')
            cloudfiles_container, cloudfiles_containerok = QInputDialog.getText(self,
                                                                    'Cloud',
                                                                    'What is the name of your '
                                               'Cloud Files container?')

        git, gitok = QInputDialog.getText(self, 'GitHub',
                                            'Do you want to upload your website using GitHub Pages?(y/n)')
        if git == 'y':
            github_pages_branch, github_pages_branchok = QInputDialog.getText(self, 'GitHub',
                                                              'Is this your personal page (username.github.io)?')


    def on_click(self):
        titletext = self.titletextbox.text()
        authortext = self.authortextbox.text()
        languagetext = self.languagetextbox.text()
        urltext = self.urltextbox.text()

        print(self.text)
        # QMessageBox.question(self, 'Message - pythonspot.com',
        #                      "You typed: " + textboxValue, QMessageBox.Ok,
        #                      QMessageBox.Ok)
        # self.textbox.setText("")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
