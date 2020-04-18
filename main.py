from tkinter import Tk, Label, Button, filedialog, Entry, Toplevel, messagebox
import csv
import re

tk = Tk()
tk.title('Python Grep')
tk.resizable(False, False)

selectedFilePath = ''
referenceIsOpen = False
searchWindow = None
labels = []

def chooseFile():
    global selectedFilePath
    selectedFilePath = filedialog.askopenfilename(initialdir='/', title='Select file', filetypes=(('Text files', '*.txt'), ('All files', '*.*')))
    if selectedFilePath != '':
        fileLabel.configure(text='Selected file: {}'.format(selectedFilePath))

def search():
    global selectedFilePath, searchWindow, labels            
    if selectedFilePath == '':
        messagebox.showinfo('Sorry', 'Please select a file.')
    else:
        if searchWindow is None:
            searchWindow = Toplevel(tk)
            searchWindow.resizable(False, False)
        else:
            for label in labels:
                label.destroy()
        with open(selectedFilePath) as file:
            lineNumber = 1
            matches = 0
            rows = 0
            for line in file:
                results = len(re.findall(regularExpressionBox.get(), line))
                if results > 0:
                    label = Label(searchWindow, text='Line {}: {}'.format(lineNumber, line))
                    label.grid(row=rows, column=0, sticky='w', padx=10)
                    labels.append(label)
                    rows += 1
                    matches += results
                lineNumber += 1
            label = Label(searchWindow, text='Total matches: {}'.format(matches))
            label.grid(row=rows, column=0, sticky='e', padx=10, pady=10)
            labels.append(label)
    

def closedReference(*args, **kwargs):
    global referenceIsOpen
    referenceIsOpen = False

def reference():
    global referenceIsOpen
    if not referenceIsOpen:
        window = Toplevel(tk)
        window.resizable(False, False)
        window.bind("<Destroy>", closedReference)
        referenceIsOpen = True
        with open('reference.csv') as file:
            reader = csv.reader(file)
            Label(window, text='Keyword', font=(16)).grid(row=0, column=0, pady=5, padx=5)
            Label(window, text='Description', font=(16)).grid(row=0, column=1, pady=5, padx=5)
            Label(window, text='Example', font=(16)).grid(row=0, column=2, pady=5, padx=5)
            i = 1
            for row in reader:
                Label(window, text=row[0], justify='left', anchor='w').grid(row=i, column=0)
                Label(window, text=row[1], wraplength=600, justify='left', anchor='w').grid(row=i, column=1, sticky='w')
                Label(window, text=row[2], justify='left', anchor='w').grid(row=i, column=2, sticky='w')
                i += 1

fileLabel = Label(tk, text='Selected file: No file chosen')
fileLabel.grid(column=0, row=0, padx=10, pady=10, sticky='w')
chooseButton = Button(tk, text='Choose file', command=chooseFile)
chooseButton.grid(column=1, row=0, padx=10, pady=10, sticky='e')

Label(tk, text='Enter regular expression:').grid(column=0, row=1, padx=10, pady=10, sticky='w')
regularExpressionBox = Entry(tk, width=20)
regularExpressionBox.grid(column=1, row=1, padx=10, pady=10, ipady=3, sticky='e')

searchButton = Button(tk, text='Search', command=search, width=10)
searchButton.grid(column=0, row=2, padx=10, pady=10, sticky='e')
referenceButton = Button(tk, text='Refer', command=reference, width=10)
referenceButton.grid(column=1, row=2, padx=10, pady=10, sticky='w')

tk.mainloop()
