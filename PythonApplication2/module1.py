import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, 
    QVBoxLayout, QWidget, QFileDialog, QCheckBox, QMessageBox, QInputDialog,QLineEdit
)
from PyQt5.QtCore import Qt
import pickle
from PyQt5.QtWidgets import QTextEdit
from datetime import datetime



class DatasetDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WFR - DataSet/Video Maker")

        # create dataset display
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Song Name", "WAV File", "Released Date"])
        self.table.verticalHeader().setVisible(False)

        # create buttons
        self.add_button = QPushButton("Add New Item", self)

        self.music_button = QPushButton("Make Music Video", self)
        self.save_button = QPushButton("Save Dataset", self)
        self.load_button = QPushButton("Load Dataset", self)
        self.remove_button = QPushButton("Remove Selected Rows", self)
        self.close_button = QPushButton("Close", self)

        # connect button signals to slots
        self.add_button.clicked.connect(self.add_item)
        self.music_button.clicked.connect(self.make_music_video)
        self.save_button.clicked.connect(self.save_dataset)
        self.load_button.clicked.connect(self.load_dataset)
        self.remove_button.clicked.connect(self.remove_selected_rows)
        self.close_button.clicked.connect(self.close)

        # add buttons to layout
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.music_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.close_button)

        # set layout for the window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def remove_selected_rows(self):
        
        song_name = QInputDialog.getText(self, "Remove Song", "Enter song name to remove:")
        if song_name[1]:
            for row in range(self.table.rowCount()):
                if self.table.item(row, 0).text() == song_name[0]:
                    self.table.removeRow(row)
                    return
        QMessageBox.warning(self, "Song not found", "The song you entered was not found in the table.")

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("Are you sure you want to delete the selected row(s)?")
        msg_box.setInformativeText("This action cannot be undone.")
        msg_box.setWindowTitle("Confirmation")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        if msg_box.exec_() != QMessageBox.Yes:
            return

        for row in song_name:
            self.table.removeRow(row.row())

    # rest of the methods remain the same...

    def add_item(self):
        row_count = self.table.rowCount()
        self.table.setRowCount(row_count + 1)

        audio_file_edit = QTableWidgetItem("Enter Files Path")
        self.table.setItem(row_count, 1, audio_file_edit)

        song_name_item = QTableWidgetItem("Enter song name")
        self.table.setItem(row_count, 0, song_name_item)

        release_date_edit = QTextEdit()
        release_date_edit.setPlainText(datetime.now().strftime('%Y-%m-%d'))
        self.table.setCellWidget(row_count, 2, release_date_edit)



        



    def make_music_video(self):
        import subprocess
        subprocess.Popen(["python", "PythonApplication2.py"])


    def save_dataset(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Dataset", "", "Dataset Files (*.dat)"
        )
        if not file_path:
            return

        # create a dictionary to hold the data from the table
        data = {
            "header_labels": [],
            "table_data": [],
        }

        # save the header labels
        for column in range(self.table.columnCount()):
            data["header_labels"].append(self.table.horizontalHeaderItem(column).text())

        # save the table data
        for row in range(self.table.rowCount()):
            row_data = []
            for column in range(self.table.columnCount()):
                cell = self.table.item(row, column)
                if cell is not None:
                    row_data.append(cell.text())
                else:
                    widget = self.table.cellWidget(row, column)
                    if isinstance(widget, QTextEdit):
                        if column == 2:
                            # try to convert the input to a valid date
                            date_str = widget.toPlainText()
                            try:
                                date = datetime.strptime(date_str, '%Y-%m-%d')
                            except ValueError:
                                # if the input is not a valid date, show an error message and return
                                msg_box = QMessageBox()
                                msg_box.setIcon(QMessageBox.Critical)
                                msg_box.setText("Invalid date format.")
                                msg_box.setInformativeText("Please enter a date in the format YYYY-MM-DD.")
                                msg_box.setWindowTitle("Error")
                                msg_box.exec_()
                                return
                            row_data.append(date.strftime('%Y-%m-%d'))
                        else:
                            row_data.append(widget.toPlainText())
                data["table_data"].append(row_data)

        # save the data to a file using pickle
        with open(file_path, "wb") as f:
            pickle.dump(data, f)

    def load_dataset(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Dataset", "", "Dataset Files (*.dat)"
        )
        if not file_path:
            return

        with open(file_path, "rb") as f:
            data = pickle.load(f)

        self.table.setRowCount(0)
        self.table.setColumnCount(len(data["header_labels"]))
        self.table.setHorizontalHeaderLabels(data["header_labels"])

        for row_data in data["table_data"]:
            row_count = self.table.rowCount()
            self.table.setRowCount(row_count + 1)
            for column, cell_data in enumerate(row_data):
                if column == 2:
                    date = datetime.strptime(cell_data, '%Y-%m-%d')
                    release_date_edit = QTextEdit()
                    release_date_edit.setPlainText(date.strftime('%Y-%m-%d'))
                    self.table.setCellWidget(row_count, column, release_date_edit)
                else:
                    item = QTableWidgetItem(cell_data)
                    self.table.setItem(row_count, column, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dataset_display = DatasetDisplay()
    dataset_display.show()
    sys.exit(app.exec_())
