from csv import excel_tab
import subprocess
import sys
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
except subprocess.CalledProcessError as error:
    print (error)
    import time
    time.sleep(100)