# UI-Schedule
UI for database which allows to change, delete or insert fields
```py
import PyQt5.QtWidgets
import psycopg2
import sys
import datetime

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)
```
![Снимок экрана от 2021-12-22 10-36-39](https://user-images.githubusercontent.com/92020672/147054101-9a79087a-898b-47eb-afb1-fc9eb76dd79a.png)

## Conclusion 
PyQt5, psycopg2 allow you to write a database management UI for people who do not know PostgreSQL.
