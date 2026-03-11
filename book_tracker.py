import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton, QLineEdit,
    QLabel, QGridLayout, QFileDialog, QRadioButton, QMessageBox,
    QButtonGroup, QScrollArea, QVBoxLayout, QHBoxLayout, QGroupBox,
    QTextEdit
)
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtCore import Qt, QSize
import os
import pandas as pd
import books_list
import time

books_counter = 0


# Window for viewing and editing book information
class BookInfoWindow(QWidget):

    def __init__(self, book_data, book_index, main_window):
        super().__init__()
        self.book_data = book_data
        self.book_index = book_index
        self.main_window = main_window
        self.new_image_path = None
        self.image = None
        
        self.setWindowTitle('Book Information')
        self.setWindowIcon(QIcon('app_icon.png'))
        self.setFixedSize(600, 700)
        self.setStyleSheet("background-color: #f5f5f5;")
        
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Title
        title_label = QLabel("‧₊˚✧[Book Details]✧˚₊‧")
        title_label.setStyleSheet('font-size: 24px; font-family: Georgia; color: #333; padding: 10px;')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Content layout (horizontal)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # Left side - Cover
        left_layout = QVBoxLayout()
        content_layout.addLayout(left_layout)
        
        # Cover display
        cover_group = QGroupBox("Cover")
        cover_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        cover_layout = QVBoxLayout(cover_group)
        
        self.cover_label = QLabel(self)
        self.cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover_label.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; background-color: white; padding: 5px;")
        cover_layout.addWidget(self.cover_label)
        
        self.change_cover_button = QPushButton('📷 Change Cover', self)
        self.change_cover_button.setStyleSheet('''
            QPushButton {
                font-size: 12px; 
                font-family: Georgia;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        self.change_cover_button.clicked.connect(self.change_cover)
        cover_layout.addWidget(self.change_cover_button)
        
        left_layout.addWidget(cover_group)
        
        # Right side - Book details
        right_layout = QVBoxLayout()
        content_layout.addLayout(right_layout)
        
        # Author
        author_group = QGroupBox("Author")
        author_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        author_layout = QVBoxLayout(author_group)
        
        self.author_input = QLineEdit()
        self.author_input.setText(str(self.book_data.get('author', '')))
        self.author_input.setStyleSheet('''
            QLineEdit {
                font-size: 14px; 
                font-family: Georgia;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        ''')
        author_layout.addWidget(self.author_input)
        right_layout.addWidget(author_group)
        
        # Title of a Book
        title_group = QGroupBox("Title")
        title_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        title_layout = QVBoxLayout(title_group)
        
        self.title_input = QLineEdit()
        self.title_input.setText(str(self.book_data.get('title', '')))
        self.title_input.setStyleSheet('''
            QLineEdit {
                font-size: 14px; 
                font-family: Georgia;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        ''')
        title_layout.addWidget(self.title_input)
        right_layout.addWidget(title_group)
        
        # Pages
        pages_group = QGroupBox("Pages")
        pages_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        pages_layout = QVBoxLayout(pages_group)
        
        self.pages_input = QLineEdit()
        pages_value = self.book_data.get('pages', '')
        self.pages_input.setText(str(pages_value))
        self.pages_input.setStyleSheet('''
            QLineEdit {
                font-size: 14px; 
                font-family: Georgia;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        ''')
        pages_layout.addWidget(self.pages_input)
        right_layout.addWidget(pages_group)
        
        # Status
        status_group = QGroupBox("Status")
        status_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        status_layout = QGridLayout(status_group)
        
        self.status_radio_read = QRadioButton('Read')
        self.status_radio_read.setStyleSheet('''
            QRadioButton {
                font-size: 14px; 
                font-family: Georgia;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
        ''')
        status_layout.addWidget(self.status_radio_read, 0, 0)
        
        self.status_radio_reading = QRadioButton('Reading')
        self.status_radio_reading.setStyleSheet('''
            QRadioButton {
                font-size: 14px; 
                font-family: Georgia;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
        ''')
        status_layout.addWidget(self.status_radio_reading, 0, 1)
        
        self.status_radio_aband = QRadioButton('Abandoned')
        self.status_radio_aband.setStyleSheet('''
            QRadioButton {
                font-size: 14px; 
                font-family: Georgia;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
        ''')
        status_layout.addWidget(self.status_radio_aband, 1, 0)
        
        self.status_radio_plan = QRadioButton('Planned')
        self.status_radio_plan.setStyleSheet('''
            QRadioButton {
                font-size: 14px; 
                font-family: Georgia;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
        ''')
        status_layout.addWidget(self.status_radio_plan, 1, 1)
        
        # Set current status
        read_val = str(self.book_data.get('read', 'False'))
        reading_val = str(self.book_data.get('reading', 'False'))
        aband_val = str(self.book_data.get('abandoned', 'False'))
        plan_val = str(self.book_data.get('planned', 'False'))
        
        if read_val == 'True':
            self.status_radio_read.setChecked(True)
        elif reading_val == 'True':
            self.status_radio_reading.setChecked(True)
        elif aband_val == 'True':
            self.status_radio_aband.setChecked(True)
        elif plan_val == 'True':
            self.status_radio_plan.setChecked(True)
        
        # Group radio buttons
        self.status_group = QButtonGroup()
        self.status_group.addButton(self.status_radio_read)
        self.status_group.addButton(self.status_radio_reading)
        self.status_group.addButton(self.status_radio_aband)
        self.status_group.addButton(self.status_radio_plan)
        
        right_layout.addWidget(status_group)
        
        # Notes
        notes_group = QGroupBox("Notes")
        notes_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        notes_layout = QVBoxLayout(notes_group)
        
        self.notes_input = QTextEdit()
        notes_value = self.book_data.get('notes', '')
        self.notes_input.setText(str(notes_value))
        self.notes_input.setPlaceholderText("Add your notes here...")
        self.notes_input.setMaximumHeight(100)
        self.notes_input.setStyleSheet('''
            QTextEdit {
                font-size: 12px; 
                font-family: Georgia;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QTextEdit:focus {
                border: 2px solid #2196F3;
            }
        ''')
        notes_layout.addWidget(self.notes_input)
        right_layout.addWidget(notes_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.save_button = QPushButton('💾 Save Changes', self)
        self.save_button.setFixedSize(150, 45)
        self.save_button.setStyleSheet('''
            QPushButton {
                font-size: 14px; 
                font-family: Georgia;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        ''')
        self.save_button.clicked.connect(self.save_changes)
        buttons_layout.addWidget(self.save_button)
        
        self.delete_button = QPushButton('🗑️ Delete Book', self)
        self.delete_button.setFixedSize(150, 45)
        self.delete_button.setStyleSheet('''
            QPushButton {
                font-size: 14px; 
                font-family: Georgia;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        ''')
        self.delete_button.clicked.connect(self.delete_book)
        buttons_layout.addWidget(self.delete_button)
        
        self.close_button = QPushButton('❌ Close', self)
        self.close_button.setFixedSize(150, 45)
        self.close_button.setStyleSheet('''
            QPushButton {
                font-size: 14px; 
                font-family: Georgia;
                background-color: #9e9e9e;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #757575;
            }
        ''')
        self.close_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.close_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Load cover image
        self.load_cover()
    
    
    # Load and display the cover image
    def load_cover(self):
        cover_path = self.book_data.get('cover', '')
        if cover_path and os.path.exists(cover_path):
            pixmap = QPixmap(cover_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    QSize(200, 250),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.cover_label.setPixmap(scaled_pixmap)
                self.cover_label.setFixedSize(scaled_pixmap.width(), scaled_pixmap.height())
        else:
            self.cover_label.setText("No cover image")
            self.cover_label.setFixedSize(200, 250)
            self.cover_label.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; background-color: white; padding: 20px; color: #999;")
    
    # Change the book cover
    def change_cover(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter('Images (*.png *.jpg *.jpeg *.bmp)')
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                image_path = selected_files[0]
                image = QImage(image_path)
                if not image.isNull():
                    # Save new cover
                    timestamp = int(time.time())
                    new_image_path = f"image_{timestamp}.jpg"
                    
                    if image.save(new_image_path, 'JPEG', quality=95):
                        # Delete old cover if it exists and is different
                        old_cover = self.book_data.get('cover', '')
                        if old_cover and os.path.exists(old_cover) and old_cover != new_image_path:
                            try:
                                os.remove(old_cover)
                            except:
                                pass
                        
                        self.new_image_path = new_image_path
                        self.image = image
                        
                        # Display new cover
                        preview_image = image.scaled(
                            QSize(200, 250),
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                        pixmap = QPixmap.fromImage(preview_image)
                        self.cover_label.setPixmap(pixmap)
                        self.cover_label.setFixedSize(preview_image.width(), preview_image.height())
    
    # Save changes to the book
    def save_changes(self):
        # Validation
        if not self.author_input.text().strip():
            QMessageBox.warning(self, "Error", "Please enter author name!")
            return
        
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Error", "Please enter book title!")
            return
        
        if not self.pages_input.text().strip():
            QMessageBox.warning(self, "Error", "Please enter number of pages!")
            return
        
        try:
            int(self.pages_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Pages must be a number!")
            return
        
        if not self.status_group.checkedButton():
            QMessageBox.warning(self, "Error", "Please select a status!")
            return
        
        # Get updated values
        cover = self.new_image_path if self.new_image_path else self.book_data.get('cover', '')
        author = self.author_input.text().strip()
        title = self.title_input.text().strip()
        pages = self.pages_input.text().strip()
        status_read = self.status_radio_read.isChecked()
        status_reading = self.status_radio_reading.isChecked()
        status_aband = self.status_radio_aband.isChecked()
        status_plan = self.status_radio_plan.isChecked()
        notes = self.notes_input.toPlainText()
        
        # Update book in database
        books_list.update_book(self.book_index, [
            str(cover), 
            str(author), 
            str(title), 
            str(pages), 
            str(status_read), 
            str(status_reading), 
            str(status_aband), 
            str(status_plan),
            str(notes)
        ])
        
        QMessageBox.information(self, 'Success', 'Book information updated successfully!')
        
        # Refresh main window
        if self.main_window:
            self.main_window.refresh_books()
    
    # Delete the book
    def delete_book(self):
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Are you sure you want to delete "{self.book_data.get("title", "this book")}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Delete cover image
            cover_path = self.book_data.get('cover', '')
            if cover_path and os.path.exists(cover_path):
                try:
                    os.remove(cover_path)
                except:
                    pass
            
            # Delete from database
            books_list.delete_book(self.book_index)
            
            QMessageBox.information(self, 'Success', 'Book deleted successfully!')
            
            # Refresh main window and close
            if self.main_window:
                self.main_window.refresh_books()
            self.close()

    
# Window for adding new books
class AnotherWindow(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.new_image_path = None
        self.image = None
        self.original_image = None
        
        self.setWindowTitle('Adding New Bookie')
        self.setWindowIcon(QIcon('app_icon.png'))
        self.setFixedSize(600, 700)
        self.setStyleSheet("background-color: #f5f5f5;")
        
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Title of the window
        title_label = QLabel("‧₊˚✧[Let's add new book!]✧˚₊‧")
        title_label.setStyleSheet('font-size: 24px; font-family: Georgia; color: #333; padding: 10px;')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Content layout (horizontal)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # Left side - Cover
        left_layout = QVBoxLayout()
        content_layout.addLayout(left_layout)
        
        # Cover display
        cover_group = QGroupBox("Cover")
        cover_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        cover_layout = QVBoxLayout(cover_group)
        
        self.cover_label = QLabel(self)
        self.cover_label.setMinimumSize(200, 200)
        self.cover_label.setText("No cover selected")
        self.cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover_label.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; background-color: white; padding: 20px; color: #999;")
        cover_layout.addWidget(self.cover_label)
        
        self.cover_button = QPushButton('📷 Choose Cover', self)
        self.cover_button.setStyleSheet('''
            QPushButton {
                font-size: 12px; 
                font-family: Georgia;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        self.cover_button.clicked.connect(self.upload_cover)
        cover_layout.addWidget(self.cover_button)
        
        left_layout.addWidget(cover_group)
        
        # Right side - Book details
        right_layout = QVBoxLayout()
        content_layout.addLayout(right_layout)
        
        # Author
        author_group = QGroupBox("Author")
        author_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        author_layout = QVBoxLayout(author_group)
        
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Enter author name")
        self.author_input.setStyleSheet('''
            QLineEdit {
                font-size: 14px; 
                font-family: Georgia;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        ''')
        author_layout.addWidget(self.author_input)
        right_layout.addWidget(author_group)
        
        # Title of a book
        title_group = QGroupBox("Title")
        title_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        title_layout = QVBoxLayout(title_group)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter book title")
        self.title_input.setStyleSheet('''
            QLineEdit {
                font-size: 14px; 
                font-family: Georgia;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        ''')
        title_layout.addWidget(self.title_input)
        right_layout.addWidget(title_group)
        
        # Pages
        pages_group = QGroupBox("Pages")
        pages_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        pages_layout = QVBoxLayout(pages_group)
        
        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("Enter number of pages")
        self.pages_input.setStyleSheet('''
            QLineEdit {
                font-size: 14px; 
                font-family: Georgia;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        ''')
        pages_layout.addWidget(self.pages_input)
        right_layout.addWidget(pages_group)
        
        # Status
        status_group = QGroupBox("Status")
        status_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        status_layout = QGridLayout(status_group)
        
        self.status_radio_read = QRadioButton('Read')
        self.status_radio_read.setStyleSheet('''
            QRadioButton {
                font-size: 14px; 
                font-family: Georgia;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
        ''')
        status_layout.addWidget(self.status_radio_read, 0, 0)
        
        self.status_radio_reading = QRadioButton('Reading')
        self.status_radio_reading.setStyleSheet('''
            QRadioButton {
                font-size: 14px; 
                font-family: Georgia;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
        ''')
        status_layout.addWidget(self.status_radio_reading, 0, 1)
        
        self.status_radio_aband = QRadioButton('Abandoned')
        self.status_radio_aband.setStyleSheet('''
            QRadioButton {
                font-size: 14px; 
                font-family: Georgia;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
        ''')
        status_layout.addWidget(self.status_radio_aband, 1, 0)
        
        self.status_radio_plan = QRadioButton('Planned')
        self.status_radio_plan.setStyleSheet('''
            QRadioButton {
                font-size: 14px; 
                font-family: Georgia;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
        ''')
        status_layout.addWidget(self.status_radio_plan, 1, 1)
        
        # Group radio buttons
        self.status_group = QButtonGroup()
        self.status_group.addButton(self.status_radio_read)
        self.status_group.addButton(self.status_radio_reading)
        self.status_group.addButton(self.status_radio_aband)
        self.status_group.addButton(self.status_radio_plan)
        
        right_layout.addWidget(status_group)
        
        # Notes
        notes_group = QGroupBox("Notes")
        notes_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px; 
                font-family: Georgia;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        ''')
        notes_layout = QVBoxLayout(notes_group)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Add your notes here...")
        self.notes_input.setMaximumHeight(100)
        self.notes_input.setStyleSheet('''
            QTextEdit {
                font-size: 12px; 
                font-family: Georgia;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QTextEdit:focus {
                border: 2px solid #2196F3;
            }
        ''')
        notes_layout.addWidget(self.notes_input)
        right_layout.addWidget(notes_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.save_button = QPushButton('💾 SAVE BOOK', self)
        self.save_button.setFixedSize(180, 50)
        self.save_button.setStyleSheet('''
            QPushButton {
                font-size: 16px; 
                font-family: Georgia;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        self.save_button.clicked.connect(self.save_book)
        buttons_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton('❌ CANCEL', self)
        self.cancel_button.setFixedSize(150, 50)
        self.cancel_button.setStyleSheet('''
            QPushButton {
                font-size: 16px; 
                font-family: Georgia;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        ''')
        self.cancel_button.clicked.connect(self.cancel_adding)
        buttons_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(buttons_layout)
    
    # Upload the cover of a book  
    def upload_cover(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter('Images (*.png *.jpg *.jpeg *.bmp)')
        if file_dialog.exec():
            image_path = file_dialog.selectedFiles()[0]
            self.original_image = QImage(image_path)
            if not self.original_image.isNull():
                # Save original images without changing
                timestamp = int(time.time())
                new_image_path = "image_{}.jpg".format(timestamp)
                
                if self.original_image.save(new_image_path, 'JPEG', quality=95):
                    self.new_image_path = new_image_path
                    
                    preview_image = self.original_image.scaled(
                        QSize(200, 250), 
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    pixmap = QPixmap.fromImage(preview_image)
                    self.cover_label.setPixmap(pixmap)
                    self.cover_label.setText("")
                    self.cover_label.setFixedSize(preview_image.width(), preview_image.height())
                    self.cover_label.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; background-color: white; padding: 5px;")
    
    # Save info about an added book
    def save_book(self):
        global books_counter
        
        # Validation
        if not self.new_image_path:
            QMessageBox.warning(self, "Error", "Please select a cover image!")
            return
        
        if not self.author_input.text():
            QMessageBox.warning(self, "Error", "Please enter author name!")
            return
            
        if not self.title_input.text():
            QMessageBox.warning(self, "Error", "Please enter book title!")
            return
            
        if not self.pages_input.text():
            QMessageBox.warning(self, "Error", "Please enter number of pages!")
            return
            
        try:
            int(self.pages_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Pages must be a number!")
            return
        
        if not self.status_group.checkedButton():
            QMessageBox.warning(self, "Error", "Please select a status!")
            return
        
        books_counter += 1
        
        cover = self.new_image_path
        author = self.author_input.text()
        title = self.title_input.text()
        pages = self.pages_input.text()
        status_read = self.status_radio_read.isChecked()
        status_reading = self.status_radio_reading.isChecked()
        status_aband = self.status_radio_aband.isChecked()
        status_plan = self.status_radio_plan.isChecked()
        notes = self.notes_input.toPlainText()
        
        # Add the info about a book into DataFrame
        books_list.books_add([
            str(cover), 
            str(author), 
            str(title), 
            str(pages), 
            str(status_read), 
            str(status_reading), 
            str(status_aband), 
            str(status_plan), 
            str(notes)
        ])
        
        QMessageBox.information(self, 'Success', 'YOUR BOOK IS ADDED!^^')
        
        # Update main window before closing
        if self.main_window:
            self.main_window.refresh_books()
        
        self.close()
    
    def cancel_adding(self):
        reply = QMessageBox.question(
            self, 'Confirm Cancel',
            'Are you sure you want to cancel adding this book?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Delete the cover image if it was saved
            if self.new_image_path and os.path.exists(self.new_image_path):
                try:
                    os.remove(self.new_image_path)
                except:
                    pass
            self.close()


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.books_data = []
        self.book_buttons = []
        self.book_containers = []
        self.info_windows = []
        
        # Create scroll area for books
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Create widget for scroll area
        scroll_widget = QWidget()
        self.layout = QGridLayout(scroll_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(30)
        
        scroll.setWidget(scroll_widget)
        self.setCentralWidget(scroll)
        
        self.resize(900, 700)
        self.setWindowTitle('My Bookies')
        self.setWindowIcon(QIcon('app_icon.png'))
        
        # Title of the window
        self.title = QLabel('‧₊˚✧[Welcome back, Reader!]✧˚₊‧')
        self.title.setStyleSheet('font-size: 30px; font-family: Georgia')
        self.layout.addWidget(self.title, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        
        # Books count label
        self.books_count_label = QLabel('Books: 0')
        self.books_count_label.setStyleSheet('font-size: 18px; font-family: Georgia')
        self.layout.addWidget(self.books_count_label, 1, 1, Qt.AlignmentFlag.AlignCenter)
        
        # Add Book button
        self.btn_add_book = QPushButton('Add Book', self)
        self.btn_add_book.setStyleSheet('font-size: 14px; font-family: Georgia')
        self.btn_add_book.clicked.connect(self.show_new_window)
        self.layout.addWidget(self.btn_add_book, 2, 1, Qt.AlignmentFlag.AlignCenter)
        
        # Load existing books
        self.load_books()
        self.update_book_display()
    
    # Load books from the database
    def load_books(self):
        try:
            self.books_data = books_list.get_books()
            print(f"Loaded {len(self.books_data)} books")
        except Exception as e:
            print(f"Error loading books: {e}")
            self.books_data = []
    
    # Create a container widget for a book with cover and text
    def create_book_container(self, book, index):
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(8)
        container_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create button for cover image
        btn = QPushButton()
        btn.setStyleSheet("border: none; background-color: transparent;")
        
        # Try to load cover image
        cover_path = book.get('cover', '')
        original_width = 200
        original_height = 0
        
        if cover_path and os.path.exists(cover_path):
            pixmap = QPixmap(cover_path)
            if not pixmap.isNull():
                original_width = pixmap.width()
                original_height = pixmap.height()
                
                if original_width > 200:
                    scale_factor = 200 / original_width
                    new_width = 200
                    new_height = int(original_height * scale_factor)
                else:
                    new_width = original_width
                    new_height = original_height
                
                scaled_pixmap = pixmap.scaled(
                    QSize(new_width, new_height),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                btn.setIcon(QIcon(scaled_pixmap))
                btn.setIconSize(QSize(new_width, new_height))
                btn.setFixedSize(new_width, new_height)
        
        btn.clicked.connect(lambda checked, idx=index: self.show_book_info_window(idx))
        
        title = book.get('title', 'Unknown')
        author = book.get('author', 'Unknown')
        
        title_label = QLabel(str(title))
        title_label.setStyleSheet('font-size: 14px; font-family: Georgia; font-weight: bold;')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        title_label.setFixedWidth(200)
        
        author_label = QLabel(f"by {str(author)}")
        author_label.setStyleSheet('font-size: 12px; font-family: Georgia; color: gray;')
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author_label.setWordWrap(True)
        author_label.setFixedWidth(200)
        
        container_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title_label)
        container_layout.addWidget(author_label)
        
        return container
    
    # Update the grid with book covers
    def update_book_display(self):
        for container in self.book_containers:
            container.deleteLater()
        self.book_containers.clear()
        
        for i, book in enumerate(self.books_data):
            row = 3 + (i // 3)
            col = i % 3
            
            container = self.create_book_container(book, i)
            
            self.layout.addWidget(container, row, col, Qt.AlignmentFlag.AlignCenter)
            self.book_containers.append(container)
        
        self.books_count_label.setText(f'Books: {len(self.books_data)}')
    
    # Refresh the book display
    def refresh_books(self):
        self.load_books()
        self.update_book_display()
    
    # Open window with full book info
    def show_book_info_window(self, index):
        if 0 <= index < len(self.books_data):
            book = self.books_data[index]
            info_window = BookInfoWindow(book, index, self)
            self.info_windows.append(info_window)
            info_window.show()
    
    # Open window to add a new book
    def show_new_window(self):
        self.new_window = AnotherWindow(self)
        self.new_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Global styling for all QMessageBox
    app.setStyleSheet("""
        QMessageBox {
            background-color: #f5f5f5;
        }
        QMessageBox QLabel {
            color: #333;
            font-size: 14px;
            font-family: Georgia;
        }
        QMessageBox QPushButton {
            font-size: 12px;
            font-family: Georgia;
            
        }
        QMessageBox QPushButton:hover {
            background-color: #1976D2;
        }
    """)
    
    window = MainWindow()
    window.show()
    app.exec()