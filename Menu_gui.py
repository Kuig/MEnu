import MEnu as me
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageGrab
import ctypes

# This helps tkinter and the image grabber to be aware of OS display scaling (under Windows)
# Feel free to remove these lines if the "save" function produces weird pictures.
ctypes.windll.shcore.SetProcessDpiAwareness(2)
#ctypes.windll.user32.SetProcessDPIAware()

# Some layout parameters
_padx = 10
_pady = 2
_ckPadXMul = 2.1
_tabPady = 20
_wrapLen = 80
_boldFont = 'Arial 9 bold'

# Init dataframes
[me.portate, me.piatti, me.settings] = me.loadData(dbFile = 'Menu.xlsx')

# GUI mainproperties
window = tk.Tk()
window.geometry("750x330")
window.title(me.settings.Dedication[0] + " MEnu! - Ver. " + me.__version__)
window.resizable(False, False)

lunchIdVar = tk.StringVar(window)
lunchIdVar.set(str(me.weekId))

# A class containing a matrix of checkboxes
class Checkbar(tk.Frame):
    def __init__(self, parent=None, picks=[], r=0, c=0):
        tk.Frame.__init__(self, parent)
        self.vars = []
        for p, pick in enumerate(picks):
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=pick, variable=var, command=inputTableChanged)
            chk.grid(row=r+p%2, column=c+p//2, padx=_padx*_ckPadXMul, pady=_pady)
            self.vars.append(var)
    def state(self):
        return [m for m in map((lambda var: var.get()), self.vars)]
    def setState(self, newState):
        for v, var in enumerate(self.vars):
            var.set(newState[v])

# A class containing a matrix of labels (for menù output)
class PasTable(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.cells = [[tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self)],
             [tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self)],
             [tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self),tk.Label(self)]]
        day_row = ['Lunedì','Martedì','Mercoledì','Giovedì','Venerdì','Sabato','Domenica']
        for d in range(7):
            self.cells[0][d+1].config(text=day_row[d],font=_boldFont)
            self.cells[0][d+1].grid(row=0, column=d+1, padx=_padx, pady=_tabPady)
    
        self.cells[1][0].config(text='Pranzo',font=_boldFont)
        self.cells[2][0].config(text='Cena',font=_boldFont)
        self.cells[1][0].grid(row=1, column=0, padx=_padx, pady=_pady, sticky='E')
        self.cells[2][0].grid(row=2, column=0, padx=_padx, pady=_pady, sticky='E')

    def displayMenu(self):
        piatti = me.outputTable['piatto']
        for p in range(14):
            cr = 1 + p % 2
            cc = 1 + p // 2
            self.cells[cr][cc].config(text=piatti[p], wraplength=_wrapLen, justify='center')
            self.cells[cr][cc].grid(row=cr, column=cc, padx=_padx, pady=_pady)

# Update menù based on settings 
#(reloads data every time... slow, but effective when live editing the excel file)
def updateWeekMenu(*args):
    me.stagione = seasonCombo.current() * 2 - 1
    me.weekId = int(lunchIdVar.get(), base=10)
    [me.portate, me.piatti, me.settings] = me.loadData(dbFile = 'Menu.xlsx')
    me.outputTable = me.getWeek(me.portate, me.piatti, me.inputTable, me.stagione, me.weekId)
    menuTab.displayMenu()

# Checkbox matrix callback
def inputTableChanged():
    me.inputTable['Name_0'] = p0PresCheck.state()
    me.inputTable['Name_1'] = p1PresCheck.state()
    updateWeekMenu()

# Helper function that print static text around the GUI
def genStaticText():
    text = "ID settimana:"
    text_output1 = tk.Label(window, text=text)
    text_output1.grid(row=1, column=0, padx=_padx, sticky="W")
    #, fg="red", font=("Helvetica", 16)

    text = "Stagione:"
    text_output2 = tk.Label(window, text=text)
    text_output2.grid(row=3, column=0, padx=_padx, sticky="W")

    text = "Presenze:"
    text_output3 = tk.Label(window, text=text)
    text_output3.grid(row=0, column=1, padx=_padx, pady=_pady, sticky="E")

    text = me.settings.Name_0[0] + " Pranzo:"
    text_output4 = tk.Label(window, text=text)
    text_output4.grid(row=1, column=1, padx=_padx, pady=_pady, sticky="E")

    text = me.settings.Name_0[0] + " Cena:"
    text_output5 = tk.Label(window, text=text)
    text_output5.grid(row=2, column=1, padx=_padx, pady=_pady, sticky="E")

    text = me.settings.Name_1[0] + " Pranzo:"
    text_output6 = tk.Label(window, text=text)
    text_output6.grid(row=3, column=1, padx=_padx, pady=_pady, sticky="E")

    text = me.settings.Name_1[0] + " Cena:"
    text_output6 = tk.Label(window, text=text)
    text_output6.grid(row=4, column=1, padx=_padx, pady=_pady, sticky="E")

    day = ['LUN','MAR','MER','GIO','VEN','SAB','DOM']
    day_t = [tk.Label(window),tk.Label(window),tk.Label(window),tk.Label(window),tk.Label(window),tk.Label(window),tk.Label(window)]

    for l in range(7):
        day_t[l].config(text=day[l])
        day_t[l].grid(row=0, column=2+l, padx=_padx*2, pady=_pady)

# Takes a snapshot of the window and saves it as PNG
# Default filename includes current WeekID
def capture_window():
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    width = window.winfo_width()
    height = window.winfo_height()
    takescreenshot = ImageGrab.grab(bbox=(x, y, x+width, y+height))
    f = fd.asksaveasfile(initialfile = 'Menu_'+str(me.weekId)+'.png',
                         defaultextension=".png",filetypes=[("Portable Network Graphics","*.png")])
    if f:
        f.close()
        takescreenshot.save(f.name)

# Week ID
lunchIdSpin = tk.Spinbox(
    window,
    textvariable=lunchIdVar,
    from_= 1,
    to= 9999,
    wrap=True,
    command=updateWeekMenu
)

# Season
seasonCombo = ttk.Combobox(
    state="readonly",
    values=["Fa freddo", "Fa caldo"]
)

# Other GUI elements
p0PresCheck = Checkbar(window, ['', '', '', '', '', '', '', '', '', '', '', '', '', ''])
p0PresCheck.setState(me.inputTable['Name_0'])
p1PresCheck = Checkbar(window, ['', '', '', '', '', '', '', '', '', '', '', '', '', ''])
p1PresCheck.setState(me.inputTable['Name_1'])
menuTab = PasTable(window)

# Layout
genStaticText()
saveBtn = tk.Button(window, text="Salva...", command=capture_window)
saveBtn.grid(row=0, column=0, padx=_padx, pady=_pady, sticky="EW")
lunchIdSpin.grid(row=2, column=0, padx=_padx, pady=_pady, sticky="W")
seasonCombo.grid(row=4, column=0, padx=_padx, pady=_pady, sticky="W")
seasonCombo.bind("<<ComboboxSelected>>", updateWeekMenu)
seasonCombo.current((me.stagione + 1) // 2)
p0PresCheck.grid(row=1, column=2, rowspan=2, columnspan=7)
p1PresCheck.grid(row=3, column=2, rowspan=2, columnspan=7)
menuTab.grid(row=5, column=0, rowspan=4, columnspan=9)

# Init the main thing
updateWeekMenu()

# Hello, I'm the GUI
if __name__ == "__main__":
    window.mainloop()