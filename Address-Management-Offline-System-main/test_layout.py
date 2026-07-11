import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTextEdit, QLabel, QGridLayout, QSizePolicy

app = QApplication(sys.argv)
w = QWidget()
root = QVBoxLayout(w)

top_layout = QHBoxLayout()

# Left Widget
left = QWidget()
left_layout = QVBoxLayout(left)
left.setStyleSheet("background-color: yellow;")

grid = QGridLayout()
grid.addWidget(QPushButton("Add"), 0, 0)
grid.addWidget(QPushButton("Edit"), 0, 1)
grid.addWidget(QPushButton("Delete"), 0, 2)
grid.addWidget(QPushButton("View"), 1, 0)
grid.addWidget(QPushButton("Clear"), 1, 1)
grid.addWidget(QPushButton("Print"), 1, 2)
left_layout.addLayout(grid)

h = QHBoxLayout()
h.addWidget(QLabel("Dept:"))
h.addWidget(QComboBox())
h.addWidget(QLabel("PARA:"))
h.addWidget(QComboBox())
left_layout.addLayout(h)
left_layout.addStretch(1) # Extra space is here right now!

# Right Widget
right = QWidget()
right.setStyleSheet("background-color: lightgreen;")
right_layout = QVBoxLayout(right)
right_layout.addWidget(QLabel("Envelope Preview"))

preview = QTextEdit()
preview.setPlainText("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nLine 8\nLine 9\nLine 10\nLine 11\nLine 12\nLine 13\nLine 14\nLine 15")
# The QTextEdit will dictate a large height hint!
# Let's fix it by setting its vertical size policy to Ignored
preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
right_layout.addWidget(preview, stretch=1)

top_layout.addWidget(left, stretch=1)
top_layout.addWidget(right, stretch=1)

root.addLayout(top_layout)

# Bottom Widget
bottom = QTextEdit()
bottom.setPlainText("Table goes here")
root.addWidget(bottom, stretch=1)

w.resize(800, 600)
w.show()
sys.exit(app.exec())
