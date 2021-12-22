# Calculator 

A simple python calculator


```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
```
Arithmetic operations are performed via `eval`
```python
def _result(self):
    try:
        res = eval(self.input.text())
        if res % 1 == 0:
            self.input.setText(str(int(res)))
        else:
            self.input.setText(str(res))
    except:
        self.input.setText(str('Нельзя делить на ноль/ошибка в написании'))
```
Result:

![Снимок экрана от 2021-12-22 10-22-27](https://user-images.githubusercontent.com/92020672/147052041-3911ab87-4dbf-466f-b12b-3c0398fc57e7.png)



## Conclusion

Using PyQt5, you can write simple UI applications, such as a calculator
