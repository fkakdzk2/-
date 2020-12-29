from pywinauto import application
from pywinauto import timings
import time
import os

app = application.Application()
app.start("C:/Kiwoom/KiwoomFlash2/khministarter.exe")

title = "번개 Login"
dlg = timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))