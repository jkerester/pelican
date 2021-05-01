import sys
import argparse
import locale
import os
import re
import smtplib
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QWidget, QPushButton,QInputDialog, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from jinja2 import Environment, FileSystemLoader

import pytz

try:
    import readline  # NOQA
except ImportError:
    pass

try:
    import tzlocal
    _DEFAULT_TIMEZONE = tzlocal.get_localzone().zone
except ImportError:
    _DEFAULT_TIMEZONE = 'Europe/Paris'

from pelican import __version__

locale.setlocale(locale.LC_ALL, '')
try:
    _DEFAULT_LANGUAGE = locale.getlocale()[0]
except ValueError:
    # Don't fail on macosx: "unknown locale: UTF-8"
    _DEFAULT_LANGUAGE = None
if _DEFAULT_LANGUAGE is None:
    _DEFAULT_LANGUAGE = 'en'
else:
    _DEFAULT_LANGUAGE = _DEFAULT_LANGUAGE.split('_')[0]

_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "templates")
_jinja_env = Environment(
    loader=FileSystemLoader(_TEMPLATES_DIR),
    trim_blocks=True,
)


_GITHUB_PAGES_BRANCHES = {
    'personal': 'main',
    'project': 'gh-pages'
}

CONF = {
    'pelican': 'pelican',
    'pelicanopts': '',
    'basedir': os.curdir,
    'ftp_host': 'localhost',
    'ftp_user': 'anonymous',
    'ftp_target_dir': '/',
    'ssh_host': 'localhost',
    'ssh_port': 22,
    'ssh_user': 'root',
    'ssh_target_dir': '/var/www',
    's3_bucket': 'my_s3_bucket',
    'cloudfiles_username': 'my_rackspace_username',
    'cloudfiles_api_key': 'my_rackspace_api_key',
    'cloudfiles_container': 'my_cloudfiles_container',
    'dropbox_dir': '~/Dropbox/Public/',
    'github_pages_branch': _GITHUB_PAGES_BRANCHES['project'],
    'default_pagination': 10,
    'siteurl': '',
    'lang': _DEFAULT_LANGUAGE,
    'timezone': _DEFAULT_TIMEZONE
}

# url for list of valid timezones
_TZ_URL = 'https://en.wikipedia.org/wiki/List_of_tz_database_time_zones'
answerlist = []
text = ''
automation = False
class _DEFAULT_PATH_TYPE(str):
    is_default_path = True


_DEFAULT_PATH = _DEFAULT_PATH_TYPE(os.curdir)

class App(QMainWindow):
    #text = ''
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
        #CONF['siteurl'] =
        #Create boxes for entries
        self.wherelabel = QLabel(
            'Where do you want to create your new website?', self)
        self.wherelabel.move(20, 6)
        self.wherelabel.resize(300, 50)
        self.wheretextbox = QLineEdit(self)
        self.wheretextbox.move(330, 6)
        self.wheretextbox.resize(280, 40)
        #-------------
        self.titlelabel = QLabel(
            'What will be the title of this web site?', self)
        self.titlelabel.move(20, 50)
        self.titlelabel.resize(300, 50)
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
        if text != '':
            CONF['siteurl'] = text
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
        CONF['siteurl'] = text
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
        automation  = True

        ftp, ftpok = QInputDialog.getText(self, 'FTP',
                                          'Do you want to upload your website using FTP?(y/n)')
        if ftp == 'y':
            CONF['ftp'] = True
            ftp_host, ftp_hostok = QInputDialog.getText(self, 'FTP',
                                                        'What is the hostname of your FTP server?')
            CONF['ftp_host'] = ftp_host
            ftp_user, ftp_userok = QInputDialog.getText(self, 'FTP',
                                                        'What is your username on that server?')
            CONF['ftp_user'] =ftp_user
            ftp_target_dir, ftp_target_dirok = QInputDialog.getText(self,
                                                                    'FTP',
                                                                    'Where do you want to put your web site on that server?')
            CONF['ftp_target_dir'] =ftp_target_dir

        ssh, ftpok = QInputDialog.getText(self, 'SSH',
                                          'Do you want to upload your website using SSH?(y/n)')
        if ssh == 'y':
            CONF['ssh'] = True
            ssh_host, ssh_hostok = QInputDialog.getText(self, 'SSH',
                                                        'What is the hostname of your SSH server?')
            CONF['ssh_host'] = ssh_host
            ssh_port, ssh_portok = QInputDialog.getText(self, 'SSH',
                                                        'What is the port of your SSH server?')
            CONF['ssh_port'] =ssh_port
            ssh_user, ssh_userok = QInputDialog.getText(self, 'SSH',
                                                        'What is your username on that server?')
            CONF['ssh_user'] = ssh_user
            ssh_target_dir, ssh_target_dirok = QInputDialog.getText(self,
                                                                    'SSH',
                                                                    'Where do you want to put your web site on that server?')
            CONF['ssh_target_dir'] = ssh_target_dir

        drop, dropok = QInputDialog.getText(self, 'Drop Box',
                                          'Do you want to upload your website using Dropbox?(y/n)')
        if drop == 'y':
            CONF['dropbox'] = True

            dropbox_dir, dropbox_dirok = QInputDialog.getText(self, 'Drop Box',
                                                        'Where is your Dropbox directory?')
            CONF['dropbox_dir'] = dropbox_dir

        s, dropok = QInputDialog.getText(self, 'S3',
                                        'Do you want to upload your website using S3?(y/n)')
        if s == 'y':
            CONF['s3'] = True
            s_bucket, s_bucketok = QInputDialog.getText(self, 'S3',
                                                        'What is the name of your S3 bucket?')
            CONF['s3_bucket'] = s_bucket

        cloud, cloudok = QInputDialog.getText(self, 'Cloud',
                                          'Do you want to upload your website using Rackspace Cloud Files?(y/n)')
        if cloud == 'y':
            CONF['cloudfiles'] = True

            cloudfiles_username, cloudfiles_usernameok = QInputDialog.getText(self, 'Cloud',
                                                        'What is your Rackspace Cloud username?')
            CONF['cloudfiles_username'] = cloudfiles_username
            cloudfiles_api_key, cloudfiles_api_keyok = QInputDialog.getText(self, 'Cloud',
                                                        'What is your Rackspace '
                                             'Cloud API key?')
            CONF['cloudfiles_api_key'] = cloudfiles_api_key
            cloudfiles_container, cloudfiles_containerok = QInputDialog.getText(self,
                                                                    'Cloud',
                                                                    'What is the name of your '
                                               'Cloud Files container?')
            CONF['cloudfiles_container'] = cloudfiles_container

        git, gitok = QInputDialog.getText(self, 'GitHub',
                                            'Do you want to upload your website using GitHub Pages?(y/n)')
        if git == 'y':
            CONF['github'] = True
            github_pages_branch, github_pages_branchok = QInputDialog.getText(
                self, 'GitHub',
                'Is this your personal page (username.github.io)?(y/n)')
            if github_pages_branch == 'y':
                CONF['github_pages_branch'] = \
                    _GITHUB_PAGES_BRANCHES['personal']
            else:
                CONF['github_pages_branch'] = \
                    _GITHUB_PAGES_BRANCHES['project']



    def on_click(self):

        project = os.path.join(
            os.environ.get('VIRTUAL_ENV', os.curdir), '.project')

        no_path_was_specified = self.wheretextbox.text()

        if os.path.isfile(project) and no_path_was_specified == '':
            CONF['basedir'] = open(project).read().rstrip("\n")
            print('Using project associated with current virtual environment. '
                  'Will save to:\n%s\n' % CONF['basedir'])
        else:
            CONF['basedir'] = os.path.abspath(
                os.path.expanduser(self.wheretextbox.text()))
        CONF['sitename'] = self.titletextbox.text()
        CONF['author'] = self.authortextbox.text()
        if self.languagetextbox.text() != '':
            CONF['lang'] = self.languagetextbox.text()
        if text != '':
            CONF['with_pagination'] = True
            CONF['default_pagination'] = int(text)
        else:
            CONF['with_pagination'] = False
        CONF['timezone'] = "Europe"
        try:
            os.makedirs(os.path.join(CONF['basedir'], 'content'))
        except OSError as e:
            print('Error: {}'.format(e))

        try:
            os.makedirs(os.path.join(CONF['basedir'], 'output'))
        except OSError as e:
            print('Error: {}'.format(e))

        try:
            with open(os.path.join(CONF['basedir'], 'pelicanconf.py'),
                      'w', encoding='utf-8') as fd:
                conf_python = dict()
                for key, value in CONF.items():
                    conf_python[key] = repr(value)

                _template = _jinja_env.get_template('pelicanconf.py.jinja2')
                fd.write(_template.render(**conf_python))
                fd.close()
        except OSError as e:
            print('Error: {}'.format(e))
        try:
            with open(os.path.join(CONF['basedir'], 'publishconf.py'),
                      'w', encoding='utf-8') as fd:
                _template = _jinja_env.get_template('publishconf.py.jinja2')
                fd.write(_template.render(**CONF))
                fd.close()
        except OSError as e:
            print('Error: {}'.format(e))
        if automation:
            try:
                with open(os.path.join(CONF['basedir'], 'tasks.py'),
                          'w', encoding='utf-8') as fd:
                    _template = _jinja_env.get_template('tasks.py.jinja2')
                    fd.write(_template.render(**CONF))
                    fd.close()
            except OSError as e:
                print('Error: {}'.format(e))
            try:
                with open(os.path.join(CONF['basedir'], 'Makefile'),
                          'w', encoding='utf-8') as fd:
                    py_v = 'python3'
                    _template = _jinja_env.get_template('Makefile.jinja2')
                    fd.write(_template.render(py_v=py_v, **CONF))
                    fd.close()
            except OSError as e:
                print('Error: {}'.format(e))

        print('Done. Your new project is available at %s' % CONF['basedir'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
