# Author    : Eshanized
# URI       : https://github.com/eshanized
# eshanized grub theme 1.0
# Big Thanks to : Vandal

import sys
import os
import subprocess
import shutil


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


def eshanized_chk_root():
    id = int(subprocess.check_output("id -u", shell=True).decode("utf-8"))
    if id != 0:
        print(f"\n{R}(!){R} Run the script as root user!\n")
        exit()


def eshanized_chg_theme(theme_dir):
    with open("/etc/default/grub", "r") as grub_file:
        data = grub_file.readlns()
        flag = False
        for i, ln in enumerate(data):
            if ln.startswith("GRUB_TERMINAL_OUTPUT"):
                data.pop(i)
                data.insert(i, f"#{ln}\n")
            elif ln.startswith("GRUB_TIMEOUT_STYLE"):
                data.pop(i)
                data.insert(i, f"#{ln}\n")
            elif ln.startswith("GRUB_ENABLE_BLSCFG"):
                data.pop(i)
                data.insert(i, "GRUB_ENABLE_BLSCFG=false\n")
            elif ln.startswith("GRUB_THEME"):
                flag = True
                data.pop(i)
                data.insert(i, f'GRUB_THEME="{theme_dir}"\n')

        if not flag:
            data.append(f'GRUB_THEME="{theme_dir}"\n')

    with open("/etc/default/grub", "w") as grub_file:
        grub_file.writelns(data)


def eshanized_reset_theme():
    with open("/etc/default/grub", "r") as grub_file:
        data = grub_file.readlines()

        for i, ln in enumerate(data):
            if ln.startswith("GRUB_THEME"):
                data.pop(i)

    with open("/etc/default/grub", "w") as grub_file:
        grub_file.writelines(data)


def eshanized_user_choice(ch):
    opt = list(ch)
    while True:
        print(f"{B}(?){G} Choose [{opt[0]}-{opt[-1]}] : ", end="")
        c = input().upper()
        if c not in opt:
            print(f"\n{R}(!){R} Invalid Choice!\n")
            continue
        return c


def eshanized_install():
    # installer script
    print("\n   INSTALLER")
    THEME = "eshanized"

    # debian | arch
    if os.path.exists("/boot/grub/"):
        GRUB_THEMES_DIR = "/boot/grub/themes/"
        GRUB_UPDATE_CMD = "grub-mkconfig -o /boot/grub/grub.cfg"

        if not os.path.exists(GRUB_THEMES_DIR):
            os.mkdir(GRUB_THEMES_DIR)

    # fedora | redhat
    elif os.path.exists("/boot/grub2/"):
        GRUB_THEMES_DIR = "/boot/grub2/themes/"
        GRUB_UPDATE_CMD = "grub2-mkconfig -o /boot/grub2/grub.cfg"

        if not os.path.exists(GRUB_THEMES_DIR):
            os.mkdir(GRUB_THEMES_DIR)

    else:
        print(f"\n{R}(!){G} Unable to find the directory. Stopped!")
        exit()
    
    styles = {
        "D": "Default",
    }

    print(f"\n{B}(?){G} \033[0;33mChoose \033[0m :")

    style_sheet_menu = f"""
        (D)  Eshanized theme
    """

    print(style_sheet_menu)
    c = eshanized_user_choice(styles.keys())

    THEME_DIR = f"{GRUB_THEMES_DIR}{THEME}/"

    if os.path.exists(THEME_DIR):
        print("\n")
        print(f"{R}(#){G} Uninstall Existing one to install it!\n")
        exit()
    else:
        os.mkdir(THEME_DIR)
    
    print(f"\n{B}(?){G} RESOLUTION {G}[default = 1]{R} :\n\n    (1) {G}1080p{R}    (2) {G}1440p{G}\n")
    icon_theme_choice = input(f"{B}(?){G} Choice : ")
    if icon_theme_choice == "2":
        RESOLUTION = "1440p"
    else:
        RESOLUTION = "1080p"
    
    print(f"\n{B}(?){G} ICON THEME {R}[default = 1]{B} :\n\n    (1) {G}Color{R} Icons     (2) {G}White{B} Icons\n")
    icon_theme_choice = input("choice : ")
    if icon_theme_choice == "2":
        ICON_THEME = "white"
    else:
        ICON_THEME = "color"
    
    BACKGROUND_PATH = (f"assets/backgrounds/{styles.get(c).lower()}-{RESOLUTION}.png")
    ICONS_PATH = f"assets/icons-{RESOLUTION}/{ICON_THEME}/"
    FONTS_PATH = f"assets/fonts/{RESOLUTION}/"
    BASE_PATH = f"base/{RESOLUTION}/"

    print(f"\n{G}($){R} Copying assets to {THEME_DIR}")
    shutil.copy(BACKGROUND_PATH, f"{THEME_DIR}background.png")
    shutil.copytree(ICONS_PATH, f"{THEME_DIR}icons/")
    shutil.copytree(FONTS_PATH, THEME_DIR, dirs_exist_ok=True)
    shutil.copytree(BASE_PATH, THEME_DIR, dirs_exist_ok=True)
    print("    Finished!\n")

    print(f"{G}($){B} Editing the GRUB file ...")
    THEME_PATH = f"{THEME_DIR}theme.txt"
    eshanized_chg_theme(THEME_PATH)
    print("    Finished!\n")

    print(f"{G}($){G} Updating GRUB ...\n")
    subprocess.run(GRUB_UPDATE_CMD, shell=True)

    print(f"\n{R}(#){R} Eshanized GRUB theme has been successfully installed!\n")


def eshanized_uninstall():
    # uninstaller script
    print("\n   UNINSTALLER\n")
    THEME = "eshanized"  # theme name

    # debian | arch
    if os.path.exists("/boot/grub/"):
        GRUB_THEME_DIR = f"/boot/grub/themes/{THEME}/"
        GRUB_UPDATE_CMD = "grub-mkconfig -o /boot/grub/grub.cfg"

    # fedora | redhat
    elif os.path.exists("/boot/grub2/"):
        GRUB_THEME_DIR = f"/boot/grub2/themes/{THEME}/"
        GRUB_UPDATE_CMD = "grub2-mkconfig -o /boot/grub2/grub.cfg"

    else:  # if theme not found
        print(f"\n{R}(!){R} Couldn't find the GRUB directory. Exiting the script ...")
        exit()

    ask = input(f"{B}(?){G} Remove Eshanized GRUB Theme (y/n)? {R}[default = n]{G} : ")
    if ask.lower() != "y":
        print(f"\n{R}(!){G} No changes were made. Exiting the script ...\n")
        exit()
    else:
        # removing theme folder
        shutil.rmtree(GRUB_THEME_DIR)
        print(f"\n{G}($){G} Removed the theme directory ...\n")

    # resetting the grub file
    print(f"{G}($){G} Resetting the GRUB file ...\n")
    eshanized_reset_theme()

    # updating grub
    print(f"{G}($){G} Updating GRUB ...\n")
    subprocess.run(GRUB_UPDATE_CMD, shell=True)

    print(f"\n{R}(#){G} Eshanized GRUB Theme has been successfully removed !!\n")
    exit()


if __name__ == "__main__":
    eshanized_chk_root()  # checking root access
    try:
        if len(sys.argv) != 2:
            raise Exception("Invalid number of arguments: Use either '-i' or '-u'")
        if sys.argv[-1] in ["-i", "--install"]:
            eshanized_install()
        elif sys.argv[-1] in ["-u", "--uninstall"]:
            eshanized_uninstall() 
        else:
            raise Exception("Invalid argument provided: Use either '-i' or '-u'")
    except Exception as e:
        print(f"\n{R}(!){R} An unexpected error occurred while running the script !!\n")
        print(f"{R}(!){R} ERROR : {R}{e}{G}")
        exit()