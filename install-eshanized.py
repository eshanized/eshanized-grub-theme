# Author    : Eshanized
# URI       : https://github.com/eshanized
# eshanized grub theme 1.0


import sys
import os
import subprocess


R = "\033[0;31m"  
G = "\033[0;32m"  
B = "\033[0;36m"  

def eshanized_chk_distro():
    try:
        lsb_id = subprocess.check_output("lsb_release -i", shell=True).decode("utf-8")
        id = lsb_id.split(":")[-1].lower().strip()
    except Exception:
        id = ""
    return id

