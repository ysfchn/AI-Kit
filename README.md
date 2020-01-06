# AI-Kit
Command line tool for App Inventor project files.

AI-Kit allows doing several tasks to App Inventor project files, (also known as AIA files) and written in Python. Using AI-Kit on your project edits your .aia file instead of creating a new edited one. So please backup your project file first before using in AI-Kit. 

Here is the list of available tasks in AI-Kit.

* **Clean-up**
    It can find the non-referenced assets and can delete them. It scans .bky, .scm and project.properties files and checks if asset name is used already.

* **Repair**
    Sometimes project files can be corrupted due to several reasons. However, AI-Kit can fix the "project in project" error by deleting multiple files.

## How to use?
As AI-Kit is written in Python, you need to have Python in your computer. It is only tested on Python 3.8 yet.

1. Install Python to your OS, download the `app.py` file and open your favourite terminal.
2. Type `python app.py` and add one (or more) of these parameters:

### **`--file`** or `-f`
Specifies the file path of the project (.aia) file. **Required**
Example: `--file "project.aia"` 

### **`--repair`** or `-r`
Repairs the project by deleting unwanted files. Fixes the "project in project" situation.

### **`--cleanup`** or `-c`
Cleans the non-used assets from project by looking the references in Screen files.

## Examples
Repair a project file named `myproject.aia`:
```
python app.py -f "myproject.aia" -r
```

---

Commands may vary depending on your operating system. However you can use short forms of commands (example: `-r`) as it works under Windows and GNU/Linux very well. 
