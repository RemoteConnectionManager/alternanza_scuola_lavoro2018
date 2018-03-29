# std lib
import sys
import collections

# pyqt5
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QWidget, QTabWidget, QVBoxLayout, QPushButton, \
    QDesktopWidget, QAction, QFileDialog, \
    QTabBar, QStyle, QPlainTextEdit

# local includes
from session_widget import QSessionWidget
from pyinstaller_utils import resource_path
from logger import QTextEditLoggerHandler, logger


class RCMMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Remote Connection Manager - CINECA - v0.01_alpha")

        width = 1000
        height = 370

        screen_width = QDesktopWidget().width()
        screen_height = QDesktopWidget().height()

        self.setGeometry((screen_width / 2) - (width / 2),
                         (screen_height / 2) - (height / 2),
                         width, height)

        self.setFixedHeight(height)
        self.setFixedWidth(width)

        # Create new action
        new_action = QAction(QIcon(resource_path('icons/new.png')), '&New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('New VNC session')
        new_action.triggered.connect(self.new_vnc_session)

        # Create new action
        open_action = QAction(QIcon(resource_path('icons/open.png')), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open VNC session')
        open_action.triggered.connect(self.open_vnc_session)

        # Create exit action
        exit_action = QAction(QIcon(resource_path('icons/exit.png')), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.exit)

        # Create the settings action
        edit_settings_action = QAction('&Settings', self)
        edit_settings_action.setShortcut('Ctrl+S')
        edit_settings_action.setStatusTip('Custom the application settings')
        edit_settings_action.triggered.connect(self.edit_settings)

        # Create the about action
        about_action = QAction('&About', self)
        about_action.setShortcut('Ctrl+A')
        about_action.setStatusTip('About the application')
        about_action.triggered.connect(self.about)

        # Create the toolbar and add actions
        # tool_bar = self.addToolBar("File")
        # tool_bar.addAction(new_action)
        # tool_bar.addAction(open_action)

        # Create menu bar and add actions
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)
        edit_menu = menu_bar.addMenu('&Edit')
        edit_menu.addAction(edit_settings_action)
        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(about_action)

        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

        logger.info("Welcome in RCM!")

    def new_vnc_session(self):
        last_tab_id = self.main_widget.tabs.count() - 1
        last_tab_uuid = self.main_widget.tabs.widget(last_tab_id).uuid

        kill_btn = QPushButton()
        kill_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        kill_btn.clicked.connect(lambda: self.on_close(last_tab_uuid))
        kill_btn.setToolTip('Close session')

        self.main_widget.tabs.setTabText(last_tab_id, "Login...")
        self.main_widget.tabs.tabBar().setTabButton(last_tab_id,
                                                    QTabBar.RightSide,
                                                    kill_btn)
        self.main_widget.add_new_tab("", False)

    def open_vnc_session(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,
                                                  "Open...",
                                                  "",
                                                  "VNC Files (*.vnc);;All Files (*)",
                                                  options=options)

    def exit(self):
        self.close()

    def edit_settings(self):
        return

    def about(self):
        return

    @pyqtSlot()
    def on_close(self, uuid):
        # loop over the tabs and found the tab with the right uuid
        for tab_id in range(0, self.main_widget.tabs.count()):
            widget = self.main_widget.tabs.widget(tab_id)
            if widget.uuid == uuid:
                if self.main_widget.tabs.currentIndex() == self.main_widget.tabs.count() - 2:
                    self.main_widget.tabs.setCurrentIndex(tab_id - 1)
                self.main_widget.tabs.removeTab(tab_id)
                return


class MainWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.tabs = QTabWidget()

        self.init_ui()

    def init_ui(self):
        """
        Initialize the interface
        """

    # Initialize tab screen
        self.tabs.resize(600, 200)
        logger.debug("Initialized tab screen")

    # Add tabs
        self.add_new_tab("Login...")
        self.add_new_tab("", False)
        self.tabs.currentChanged.connect(self.on_change)
        logger.debug("Created tabs")

    # Add tabs to widget
        self.main_layout.addWidget(self.tabs)
        logger.debug("Added tabs to widget")

    # Add text log
        text_log_frame = QPlainTextEdit(self)
        text_log_frame.setFixedHeight(80)
        self.main_layout.addWidget(text_log_frame)

    # configure logging
        text_log_handler = QTextEditLoggerHandler(text_log_frame)
        logger.addHandler(text_log_handler)

    # Set main layout
        self.setLayout(self.main_layout)

    @pyqtSlot()
    def on_change(self):
        """
        Add a new "+" tab and substitute "+2" with "login" in the previous tab
        if the last tab is selected
        :return:
        """
        if self.tabs.currentIndex() == self.tabs.count() - 1:
            self.tabs.setTabText(self.tabs.currentIndex(), "Login...")

            uuid = self.tabs.currentWidget().uuid

            kill_btn = QPushButton()
            kill_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
            kill_btn.setToolTip('Close session')
            kill_btn.clicked.connect(lambda: self.on_close(uuid))
            self.tabs.tabBar().setTabButton(self.tabs.currentIndex(),
                                            QTabBar.RightSide,
                                            kill_btn)
            self.add_new_tab("", False)

    @pyqtSlot()
    def on_new(self):
        """
        Add a new "+" tab and substitute "+2" with "login" in the previous tab
        if the last tab button is pressed
        :return:
        """
        last_tab = self.tabs.count() - 1
        self.tabs.setTabText(last_tab, "Login...")

        kill_btn = QPushButton()
        kill_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        kill_btn.setToolTip('Close session')
        uuid = self.tabs.widget(last_tab).uuid
        kill_btn.clicked.connect(lambda: self.on_close(uuid))
        self.tabs.tabBar().setTabButton(last_tab,
                                        QTabBar.RightSide,
                                        kill_btn)
        self.add_new_tab("", False)

    def add_new_tab(self, session_name, show_close_btn=True):
        """
        Add a new tab in the tab widget
        :param session_name: name to be displayed
        :param show_close_btn: if true we add the close button
        :return:
        """
        new_tab = QSessionWidget(self.tabs)
        uuid = new_tab.uuid
        self.tabs.addTab(new_tab, session_name)

        if show_close_btn:
            kill_btn = QPushButton()
            kill_btn.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
            kill_btn.clicked.connect(lambda: self.on_close(uuid))
            kill_btn.setToolTip('Close session')
            self.tabs.tabBar().setTabButton(self.tabs.count() - 1,
                                            QTabBar.RightSide,
                                            kill_btn)
        else:
            kill_btn = QPushButton()
            ico = QIcon()
            ico.addFile(resource_path('icons/plus.png'))
            kill_btn.setIcon(ico)
            kill_btn.clicked.connect(self.on_new)
            kill_btn.setToolTip('New session')
            self.tabs.tabBar().setTabButton(self.tabs.count() - 1,
                                            QTabBar.RightSide,
                                            kill_btn)

        new_tab.logged_in.connect(self.on_login)
        new_tab.sessions_changed.connect(self.on_sessions_changed)
        logger.debug("Added new tab " + str(uuid))

    @pyqtSlot(str)
    def on_login(self, session_name):
        self.tabs.setTabText(self.tabs.currentIndex(), session_name)

    @pyqtSlot()
    def on_close(self, uuid):
        # loop over the tabs and found the tab with the right uuid
        for tab_id in range(0, self.tabs.count()):
            widget = self.tabs.widget(tab_id)
            if widget.uuid == uuid:
                if self.tabs.currentIndex() == self.tabs.count() - 2:
                    self.tabs.setCurrentIndex(tab_id - 1)
                self.tabs.removeTab(tab_id)
                return

    @pyqtSlot(collections.deque)
    def on_sessions_changed(self, sessions_list):
        for tab_id in range(0, self.tabs.count()):
            widget = self.tabs.widget(tab_id)
            widget.session_combo.clear()
            widget.session_combo.addItems(sessions_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rcm_win = RCMMainWindow()
    rcm_win.show()
    sys.exit(app.exec_())
