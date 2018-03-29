# stdlib
import uuid
from logger import logger

# pyqt5
from PyQt5.QtWidgets import QLabel, QLineEdit, QDialog, QComboBox, \
    QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout, QPushButton


class QDisplayDialog(QDialog):

    def __init__(self, display_names):
        QDialog.__init__(self)

        self.display_name = ""
        self.display_names = display_names

        self.session_line = QLineEdit(self)
        self.session_queue_combo = QComboBox(self)
        self.session_vnc_combo = QComboBox(self)
        self.display_combo = QComboBox(self)

        self.setWindowTitle("New display")
        self.init_ui()

    def init_ui(self):
        """
        Initialize the interface
        :return:
        """

        # create the grid layout
        grid_layout = QGridLayout()

        # Create session layout
        session_name = QLabel(self)
        session_name.setText('session name:')

        grid_layout.addWidget(session_name, 1, 0)
        grid_layout.addWidget(self.session_line, 1, 1)

        session_queue = QLabel(self)
        session_queue.setText('Select queue:')
        self.session_queue_combo.addItems(["12core_40gb_3h_slurm",
                                           "4core_18gb_1h_slurm",
                                           "4core_18gb_3h_slurm"])
        grid_layout.addWidget(session_queue, 2, 0)
        grid_layout.addWidget(self.session_queue_combo, 2, 1)

        session_vnc = QLabel(self)
        session_vnc.setText('Select wm+vnc:')
        self.session_vnc_combo.addItems(["fluxbox_turbovnc",
                                         "xfce_singularity_turbovnc"])
        grid_layout.addWidget(session_vnc, 3, 0)
        grid_layout.addWidget(self.session_vnc_combo, 3, 1)

        display_label = QLabel(self)
        display_label.setText('Display size:')
        self.display_combo.addItems(["1920x1080",
                                     "full_screen"])

        grid_layout.addWidget(display_label, 4, 0)
        grid_layout.addWidget(self.display_combo, 4, 1)

        # Ok button
        hor_layout = QHBoxLayout()
        ok_button = QPushButton('Ok', self)
        ok_button.clicked.connect(self.on_ok)
        ok_button.setFixedHeight(20)
        ok_button.setFixedWidth(100)
        hor_layout.addStretch(1)
        hor_layout.addWidget(ok_button)

        # Cancel button
        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.reject)
        cancel_button.setFixedHeight(20)
        cancel_button.setFixedWidth(100)
        hor_layout.addWidget(cancel_button)
        hor_layout.addStretch(1)

        group_box = QGroupBox()
        group_box.setLayout(grid_layout)

        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(group_box)
        dialog_layout.addSpacing(10)
        dialog_layout.addLayout(hor_layout)
        dialog_layout.addSpacing(20)
        self.setLayout(dialog_layout)

    def on_ok(self):
        """
        :return: Return accept signal if the display name is unique
        """

        display_name = str(self.session_line.text())

        # if the display_name is empty, it is set to a random uuid
        if display_name == "":
            self.display_name = uuid.uuid4().hex
        else:
            self.display_name = display_name

        # if the display name already exists, it returns
        if self.display_name in self.display_names:
            logger.error("session " + str(self.display_name) + " already exists")
            return

        self.accept()
