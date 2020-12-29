from pywinauto import application
from pywinauto import timings
import time
import os

app = application.Application()
app.start("C:\KiwoomFlash3\Bin\\NKMiniStarter.exe")

title = "번개3 Login"
dlg = timings.wait_until_passes(20, 0.5, lambda: app.window(title=title))


pass_ctrl = dlg.Edit2
pass_ctrl.set_focus()
pass_ctrl.type_keys('05soon09')

"""cert_ctrl = dlg.Edit3
cert_ctrl.SetFocus()
cert_ctrl.TypeKeys('yyyy')"""

btn_ctrl = dlg.Button0
btn_ctrl.click()

time.sleep(50)
os.system("taskkill /im khmini.exe")