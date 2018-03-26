# pyqt5
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QFileDialog, QFrame, QLabel, QComboBox, \
    QGridLayout, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton

# paramiko
from paramiko.ssh_exception import AuthenticationException

# local includes
from ssh import sshCommando
from display_dialog import QDisplayDialog
from pyinstaller_utils import resource_path
from logger import logger


class QSessionWidget(QWidget):
    """
    Create a new session widget to be put inside a tab in the main window
    """

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.hosts = ["login.marconi.cineca.it", "login.pico.cineca.it"]
        self.user = ""
        self.sessions = {}

        self.init_ui()

    def init_ui(self):
        """
        Initialize the interface
        """

    # Create first tab
        new_tab_main_layout = QVBoxLayout()

    # Login Layout
        grid_login_layout = QGridLayout()
        login_layout = QVBoxLayout()

        host_label = QLabel(self)
        host_label.setText('Host:')
        self.host_combo = QComboBox(self)
        self.host_combo.addItems(["login.marconi.cineca.it", "login.pico.cineca.it"])
        grid_login_layout.addWidget(host_label, 0, 0)
        grid_login_layout.addWidget(self.host_combo, 0, 1)

        user_label = QLabel(self)
        user_label.setText('User:')
        self.user_line = QLineEdit(self)
        grid_login_layout.addWidget(user_label, 1, 0)
        grid_login_layout.addWidget(self.user_line, 1, 1)

        pssw_label = QLabel(self)
        pssw_label.setText('Password:')
        self.pssw_line = QLineEdit(self)
        self.pssw_line.setEchoMode(QLineEdit.Password)
        grid_login_layout.addWidget(pssw_label, 2, 0)
        grid_login_layout.addWidget(self.pssw_line, 2, 1)

        login_hor_layout = QHBoxLayout()
        pybutton = QPushButton('Login', self)
        pybutton.clicked.connect(self.login)
        pybutton.setShortcut("Return")

        openbtn = QPushButton('Open', self)
        openbtn.clicked.connect(self.open)

        login_hor_layout.addStretch(1)
        login_hor_layout.addWidget(openbtn)
        login_hor_layout.addWidget(pybutton)
        login_hor_layout.addStretch(1)

        self.error_label = QLabel(self)
        self.error_label.setText("Wrong username or password")
        self.error_label.setStyleSheet("color:red")
        grid_login_layout.addWidget(self.error_label, 3, 1)
        self.error_label.hide()

        login_layout.addLayout(grid_login_layout)
        login_layout.addLayout(login_hor_layout)
        self.containerLoginWidget = QWidget()
        self.containerLoginWidget.setLayout(login_layout)
        new_tab_main_layout.addWidget(self.containerLoginWidget)

    # Session Layout
        plusbutton_layout = QGridLayout()
        self.session_ver_layout = QVBoxLayout()
        self.rows_ver_layout = QVBoxLayout()
        self.rows_ver_layout.setContentsMargins(0,0,0,0)
        self.rows_ver_layout.setSpacing(0)

        self.session_ver_layout.addLayout(plusbutton_layout)
        self.session_ver_layout.addLayout(self.rows_ver_layout)
        self.session_ver_layout.addStretch(1)

        self.connect_ico = QIcon()
        self.connect_ico.addFile(resource_path('icons/connect.png'))

        self.kill_ico = QIcon()
        self.kill_ico.addFile(resource_path('icons/kill.png'))

        self.share_ico = QIcon()
        self.share_ico.addFile(resource_path('icons/share.png'))

        myFont = QFont()
        myFont.setBold(True)

        name = QLabel()
        name.setText("Name")
        name.setFont(myFont)
        plusbutton_layout.addWidget(name,0,0)

        status = QLabel()
        status.setText("Status")
        status.setFont(myFont)
        plusbutton_layout.addWidget(status,0,1)

        time = QLabel()
        time.setText("Time")
        time.setFont(myFont)
        plusbutton_layout.addWidget(time,0,2)

        resources = QLabel()
        resources.setText("Resources")
        resources.setFont(myFont)
        plusbutton_layout.addWidget(resources,0,3)

        x = QLabel()
        x.setText("")
        plusbutton_layout.addWidget(x,0,4)
        plusbutton_layout.addWidget(x, 0, 5)

        new_display_ico = QIcon()
        new_display_ico.addFile(resource_path('icons/plus.png'), QSize(16, 16))
        new_display = QPushButton()
        new_display.setIcon(new_display_ico)
        new_display.clicked.connect(self.add_new_display)
        new_display_layout = QHBoxLayout()
        new_display_layout.addSpacing(100)
        new_display_layout.addWidget(new_display)

        plusbutton_layout.addLayout(new_display_layout,0,6)

        self.containerSessionWidget = QWidget()
        self.containerSessionWidget.setLayout(self.session_ver_layout)
        new_tab_main_layout.addWidget(self.containerSessionWidget)
        self.containerSessionWidget.hide()

        self.setLayout(new_tab_main_layout)

    def login(self):
        try:
            logger.info("Log in" + str(self.user_line.text()) + "@" + str(self.host_combo.currentText()))
            sshCommando(self.host_combo.currentText(), 22,
                        self.user_line.text(),
                        self.pssw_line.text(), 'ls')
        except AuthenticationException:
            self.error_label.show()
            logger.info("")
            return
        logger.info("Logged in")
        self.user = self.user_line.text()
        self.containerLoginWidget.hide()
        self.containerSessionWidget.show()

    # file dialog
    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,
                                                  "Open...",
                                                  "",
                                                  "VNC Files (*.vnc);;All Files (*)",
                                                  options=options)

    def add_new_display(self):
        # cannot have more than 5 displays
        if len(self.sessions) >= 5:
            logger.info("You have already 5 displays")
            return

        displaywin = QDisplayDialog(list(self.sessions.keys()))
        displaywin.setModal(True)

        if displaywin.exec() != 1:
            return

        display_hor_layout = QHBoxLayout()
        display_hor_layout.setContentsMargins(0,2,0,2)
        display_hor_layout.setSpacing(2)

        display_ver_layout = QVBoxLayout()
        display_ver_layout.setContentsMargins(0, 0, 0, 0)
        display_ver_layout.setSpacing(0)

        display_ver_layout.addLayout(display_hor_layout)

        display_widget = QWidget()
        display_widget.setLayout(display_ver_layout)

        id = displaywin.session_name
        print(id)

        name = QLabel()
        name.setText(str(id)[:16])
        display_hor_layout.addWidget(name)

        status = QLabel()
        status.setText("Pending...")
        display_hor_layout.addWidget(status)

        time = QLabel()
        time.setText("24H")
        display_hor_layout.addWidget(time)

        resources = QLabel()
        resources.setText("1 Node")
        display_hor_layout.addWidget(resources)

        connect = QPushButton()
        connect.setIcon(self.connect_ico)
        connect.clicked.connect(lambda: self.connect_display(id))
        display_hor_layout.addWidget(connect)

        share = QPushButton()
        share.setIcon(self.share_ico)
        share.clicked.connect(lambda: self.share_display(id))
        display_hor_layout.addWidget(share)

        kill = QPushButton()
        kill.setIcon(self.kill_ico)
        kill.clicked.connect(lambda: self.kill_display(id))
        display_hor_layout.addWidget(kill)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        display_ver_layout.addWidget(separator)

        self.rows_ver_layout.addWidget(display_widget)

        self.sessions[id] = display_widget
        logger.info("Added new display")

    def connect_display(self, id):
        print(self.sessions[id])
        logger.info("Connected to "+str(id))

    def share_display(self, id):
        print(self.sessions[id])
        logger.info("Shared " + str(id))

    def kill_display(self, id):
        # first we hide the display
        logger.debug("Hiding the display")
        self.sessions[id].hide()

        # then we remove it from the layout and the dictionary
        self.rows_ver_layout.removeWidget(self.sessions[id])
        del self.sessions[id]

        logger.info("Killed session " + str(id))