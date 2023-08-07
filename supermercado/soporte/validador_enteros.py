from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp


class ValidadorEnteros(QRegExpValidator):

    def __init__(self, max_digits=5, negative=False):
        if negative:
            reg_ex = "-?"
        else:
            reg_ex = ""
        reg_ex += "[0-9]{1," + str(max_digits) + "}"
        QRegExpValidator.__init__(self, QRegExp(reg_ex))
