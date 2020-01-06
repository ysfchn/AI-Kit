import ruamel.std.zipfile as zipfile
import sys, getopt
import os

from ruamel.std.zipfile import delete_from_zip_file

# Command line argument parser
# -----
fullCmdArguments = sys.argv
argumentList = fullCmdArguments[1:]

unixOptions = "f:rc"
gnuOptions = ["file=", "repair", "cleanup"]

try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    print ("[!] - " + str(err))
    sys.exit(2)
# ----

# Stores AIA file path.
aiapath = ""

# A list which contains file paths of files which will be deleted in .aia file.
willDeleted = []

clean = False
repair = False

print ("AIA-Kit by Yusuf Cihan")
print ("Command line tool for App Inventor projects")
print ("")

for currentArgument, currentValue in arguments:
    if currentArgument in ("-c", "--cleanup"):
        clean = True
    elif currentArgument in ("-r", "--repair"):
        repair = True
    elif (currentArgument in ("-f", "--file")) and aiapath == "":
        # If .aia file is not an archive or/and doesn't exist, stop the application.
        if os.path.isfile(currentValue) and zipfile.is_zipfile(currentValue):
            aiapath = currentValue
        else:
            print ("[!] - Project file is not exist or in the valid format!")
            sys.exit(1)

if aiapath == "":
    print ("[!] - Project file is not specified!")
    sys.exit(1)

# --------------
#  Repair .aia
#   - Fixes "project in project" error.
# --------------
def repairaia():
    willDeleted.clear()
    print ("Repairing project...")
    zf = zipfile.ZipFile(aiapath, 'r')

    # Checks the "project in project" situation and adds the all unwanted file names to a list.
    # ...for example Screen files in the assets folder are unexpected.
    for fileName in zf.namelist():
        if fileName.startswith(("assets/external_comps/assets/external_comps/", "assets/external_comps/src/", "assets/external_comps/youngandroidproject/")):
            willDeleted.append(fileName)
            print ("[-] - DELETED: " + fileName)
        # It is not needed to store .aia files as assets too.
        elif fileName.endswith(".aia"):
            willDeleted.append(fileName)
            print ("[-] - DELETED: " + fileName)

    # Delete unwanted files from the .aia file.
    delete_from_zip_file(aiapath, file_names=willDeleted)

    # If willDeleted list is empty, this means there is nothing to edit.
    if willDeleted == []:
        print ("Nothing found to repair.")

    print ("")
    print ("[#] Repair finished. Affected files: " + str(len(willDeleted)))
    zf.close()
    pass

# --------------
#  Clean-up the .aia
#   - Scans the .bky and .scm files, and deletes all assets which is not referenced in these files.
# --------------
def cleanaia():
    willDeleted.clear()
    print ("Cleaning the project...")
    zf = zipfile.ZipFile(aiapath, 'r')
    
    # Content of all .bky files in project.
    bky = []

    # Content of all .scm files in project.
    scm = []

    # Content of the project.properties file.
    prop = ""

    # Reads .bky, .scm and project.properties files from project and saves into a variable.
    for fileName in zf.namelist():
        if fileName.endswith(".bky"):
            bky.append(zf.read(fileName).decode(sys.stdout.encoding))
        elif fileName.endswith(".scm"):
            scm.append(zf.read(fileName).decode(sys.stdout.encoding))
        elif "project.properties" in fileName:
            prop = prop + zf.read(fileName).decode(sys.stdout.encoding)

    # Converts list to string for checking the references.
    filebky = "".join(bky)
    filescm = "".join(scm)

    for fileName in zf.namelist():
        # Gets the name of the file by deleting the path piece.
        name = fileName.split("/")[-1]
        if fileName.startswith("assets/") and (not "external_comps/" in fileName):
            # Checks if the name is already used in project files.
            if name in filebky:
                pass
            elif name in filescm:
                pass
            elif name in prop:
                pass
            else:
                willDeleted.append(fileName)
                print ("[-] - DELETED: " + fileName)

    # Delete unwanted files from the .aia file.
    delete_from_zip_file(aiapath, file_names=willDeleted)

    # If willDeleted list is empty, this means there is nothing to edit.
    if willDeleted == []:
        print ("Nothing found to cleanup.")

    print ("")
    print ("[#] Cleanup finished. Affected files: " + str(len(willDeleted)))
    zf.close()
    pass

if repair:
    repairaia()

if clean:
    cleanaia()





