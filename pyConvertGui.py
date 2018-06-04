import sys
import os

import converter

sep = os.sep

if sys.version_info[0] < 3: # For python 2.7/3.6 compatibility
    import Tkinter as tk
    import tkMessageBox as msgBox
    import tkFileDialog as fileDialog
    import ttk
else:
    import tkinter as tk
    from tkinter import messagebox as msgBox
    from tkinter import filedialog as fileDialog
    from tkinter import ttk

if "PYTHONPATH" in os.environ:
    PYTHONPATH = os.environ["PYTHONPATH"]

    if (PYTHONPATH[0] == "'" or PYTHONPATH[0] == '"') \
       and (PYTHONPATH[-1] == "'" or PYTHONPATH[-1] == '"'):
        PYTHONPATH = PYTHONPATH[1:]
        PYTHONPATH = PYTHONPATH[:-1]
else:
    PYTHONPATH = sys.path[-2]

def corrigPath(path):
    if sep == "\\":
        path = path.replace("/", "\\")
    elif sep == "/":
        path = path.replace("\\", "/")

    return path

PYTHONPATH = corrigPath(PYTHONPATH)

FILEDIR = os.path.dirname(__file__)


class GUIApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("pyConvert")
        self.iconbitmap("icon.ico")

        self.createWidgets()

        self.config(menu=self.mainMenu)

    def exit(self):
        self.destroy()

    def openError(self):
        msgBox.showerror("pyConvert", "The file does not exists.")

    def askOpen(self):
        path = fileDialog.askopenfilename(filetypes=[("Python files", "*.py"),
                                                      ("Python window files", "*.pyw")],
                                            initialdir=FILEDIR,
                                            parent=self)

        if path == "":
            return "abort"
        elif not os.path.isfile(path):
            self.openError()
            path = self.askOpen()

        return path

    def askSaveAs(self, initFile, initDir):
        path = fileDialog.asksaveasfilename(filetypes=[("Executable files", "*.exe")],
                                            initialdir=initDir,
                                            initialfile=initFile,
                                            parent=self)


        if path[-4:] == ".exe": return path
        elif path == "": return "abort"
        else: return path + ".exe"

    def searchFile(self, widget):
        path = fileDialog.askopenfilename(filetypes=[("Icon files", "*.ico")],
                                            initialdir=FILEDIR,
                                            parent=self)

        if not path == "":
            widget.delete(0, tk.END)
            widget.insert(tk.END, path)

    def askOs(self):
        x64 = not os.environ["PROCESSOR_ARCHITECTURE"] == "x86"
        
        root = tk.Toplevel(self)
        root.title("Choose operating system")
        root.iconbitmap("icon.ico")

        putZip = tk.BooleanVar()
        withWindow = tk.BooleanVar()
        upx = tk.BooleanVar()

        zipFile = ttk.Checkbutton(root, text="Put files into zip archive",
                                  variable=putZip)
        zipFile.grid(row=0, column=0)
        withWin = ttk.Checkbutton(root, text="Show shell window",
                                  variable=withWindow)
        withWin.grid(row=1, column=0)

        compression = ttk.Checkbutton(root, text="UPX Compression",
                                      variable=upx)
        compression.grid(row=2, column=0)

        iconLabel = ttk.Label(root, text="Icon:")
        iconLabel.grid(row=3, column=0)

        iconEntry = ttk.Entry(root)
        iconEntry.grid(row=3, column=1)

        iconBtn = ttk.Button(root, text="Search",
                             command=lambda: self.searchFile(iconEntry))
        iconBtn.grid(row=3, column=2)

        pwdLabel = ttk.Label(root, text="Password:")
        pwdLabel.grid(row=4, column=0)

        pwdEntry = ttk.Entry(root, show="\u25CF")
        pwdEntry.grid(row=4, column=1)

        applyBtn = ttk.Button(root, text="Apply",
                             command=lambda: converter.convert(self.inFile,
                                                               self.outFile,
                                                               putZip.get(),
                                                               withWindow.get(),
                                                               root,
                                                               iconEntry.get(),
                                                               pwdEntry.get(),
                                                               x64,
                                                               upx))
        applyBtn.grid(row=5)

    def convert(self):
        self.inFile = corrigPath(self.askOpen())

        if not self.inFile == "abort":
            self.outFile = corrigPath(self.askSaveAs(os.path.split(self.inFile)[1].split(".")[0] + ".exe",
                                                     os.path.split(self.inFile)[0]))

            if not self.outFile == "abort":
                self.askOs()

    def createWidgets(self):
        self.createMenu()

    def createMenu(self):
        self.mainMenu = tk.Menu(self, tearoff=False)
        
        self.fileMenu = tk.Menu(self.mainMenu, tearoff=False)
        self.fileMenu.add_command(label="Convert script", command=self.convert)
        self.fileMenu.add_command(label="Exit", command=self.exit)

        self.mainMenu.add_cascade(menu=self.fileMenu, label="File")


app = GUIApp()
app.mainloop()
