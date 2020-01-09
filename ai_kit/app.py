"""
Command line tool for App Inventor project files.

AI-Kit allows doing several tasks to App Inventor project files, (also known as
AIA files) and written in Python.
Using AI-Kit on your project edits your .aia file instead of creating a new
edited one.
So please backup your project file first before using in AI-Kit.
Here is the list of available tasks in AI-Kit.
"""
import os
import sys
import getopt
import ruamel.std.zipfile as zipfile
from ruamel.std.zipfile import delete_from_zip_file


def repairaia(aia_path='../sample.aia'):
    """
    Repair .aia.

    - Fixes "project in project" error.
    """
    will_deleted = list()

    print("Repairing project...")
    zip_file = zipfile.ZipFile(aia_path, 'r')
    # Checks the "project in project" situation and adds the all unwanted file
    # names to a list.
    # ...for example Screen files in the assets folder are unexpected.
    for file_name in zip_file.namelist():
        if file_name.startswith(
                (
                    "assets/external_comps/assets/external_comps/",
                    "assets/external_comps/src/",
                    "assets/external_comps/youngandroidproject/")):

            will_deleted.append(file_name)
            print("[-] - DELETED: " + file_name)
        # It is not needed to store .aia files as assets too.
        elif file_name.endswith(".aia"):
            will_deleted.append(file_name)
            print("[-] - DELETED: " + file_name)

    # Delete unwanted files from the .aia file.
    delete_from_zip_file(aia_path, file_names=will_deleted)

    # If will_deleted list is empty, this means there is nothing to edit.
    if will_deleted == list():
        print("Nothing found to repair.")

    print("")
    print("[#] Repair finished. Affected files: " + str(len(will_deleted)))
    zip_file.close()
    return True


def cleanaia(aia_path='../sample.aia'):
    """
    Clean-up the .aia.

    - Scans the .bky and .scm files, and deletes all assets which is not refere
    nced in these files.
    """
    will_deleted = list()
    print("Cleaning the project...")
    zip_file = zipfile.ZipFile(aia_path, 'r')

    # Content of all .bky files in project.
    bky = list()

    # Content of all .scm files in project.
    scm = list()

    # Content of the project.properties file.
    prop = ""

    # Reads .bky, .scm and project.properties files from project and saves into
    # a variable.
    for file_name in zip_file.namelist():
        if file_name.endswith(".bky"):
            bky.append(zip_file.read(file_name).decode(sys.stdout.encoding))
        elif file_name.endswith(".scm"):
            scm.append(zip_file.read(file_name).decode(sys.stdout.encoding))
        elif "project.properties" in file_name:
            prop = prop + zip_file.read(file_name).decode(sys.stdout.encoding)

    # Converts list to string for checking the references.
    filebky = "".join(bky)
    filescm = "".join(scm)

    for file_name in zip_file.namelist():
        # Gets the name of the file by deleting the path piece.
        name = file_name.split("/")[-1]
        if file_name.startswith("assets/") and \
                "external_comps/" not in file_name:
            # Checks if the name is already used in project files.
            if name in filebky:
                pass
            elif name in filescm:
                pass
            elif name in prop:
                pass
            else:
                will_deleted.append(file_name)
                print("DELETED: " + file_name)

    # Delete unwanted files from the .aia file.
    delete_from_zip_file(aia_path, file_names=will_deleted)

    # If will_deleted list is empty, this means there is nothing to edit.
    if will_deleted == list():
        print("Nothing found to cleanup.")

    print("")
    print("[#] Cleanup finished. Affected files: " + str(len(will_deleted)))
    zip_file.close()
    return True


if __name__ == '__main__':
    # Command line argument parser
    # -----
    FULL_CMD_ARGUMENTS = sys.argv
    ARGUMENT_LIST = FULL_CMD_ARGUMENTS[1:]

    UNIX_OPTIONS = "f:rc"
    GUN_OPTIONS = ["file=", "repair", "cleanup"]

    try:
        ARGUMENTS, VALUES = getopt.getopt(
            ARGUMENT_LIST, UNIX_OPTIONS, GUN_OPTIONS)
    except getopt.error as err:
        print("[!] - " + str(err))
        sys.exit(2)
    # ----
    # Stores AIA file path.
    AIAPATH = ""

    CLEAN = False
    REPAIR = False

    print("AIA-Kit by Yusuf Cihan")
    print("Command line tool for App Inventor projects")
    print("")

    for currentArgument, current_value in ARGUMENTS:
        if currentArgument in ("-c", "--cleanup"):
            CLEAN = True
        elif currentArgument in ("-r", "--repair"):
            REPAIR = True
        elif (currentArgument in ("-f", "--file")) and AIAPATH == "":
            # If .aia file is not an archive or/and doesn't exist,
            # stop the application.
            if os.path.isfile(current_value) and zipfile.is_zipfile(
                    current_value):
                AIAPATH = current_value
            else:
                print("Project file is not exist or in the valid format!")
                sys.exit(1)

    if AIAPATH == "":
        print("Project file is not specified!")
        sys.exit(1)

    if REPAIR:
        repairaia(aia_path=AIAPATH)

    if CLEAN:
        cleanaia(aia_path=AIAPATH)
