import sys
from tkinter import ttk
import tkinter
from AddNew import AddNew
sys.path.append('../Patient.py')
import Patient

class Main(tkinter.Frame):
    '''
    classdocs
    '''
    def __init__(self, parent):
        '''
        Constructor
        '''
        tkinter.Frame.__init__(self, parent)
        self.parent=parent

        self.initialize_user_interface()

    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type
        items and insert them into the treeview
        """
        self.parent.title("Canvas Test")
        self.parent.grid_rowconfigure(0,weight=1)
        self.parent.grid_columnconfigure(0,weight=1)
        self.parent.config(background="lavender")


        # Define the different GUI widgets
        self.dose_label = tkinter.Label(self.parent, text = "Dose:")
        self.dose_entry = tkinter.Entry(self.parent)
        self.dose_label.grid(row = 0, column = 0, sticky = tkinter.W)
        self.dose_entry.grid(row = 0, column = 1)

        self.modified_label = tkinter.Label(self.parent, text = "Date Modified:")
        self.modified_entry = tkinter.Entry(self.parent)
        self.modified_label.grid(row = 1, column = 0, sticky = tkinter.W)
        self.modified_entry.grid(row = 1, column = 1)

        self.submit_button = tkinter.Button(self.parent, text = "Insert", command = self.showInsert)
        self.submit_button.grid(row = 2, column = 1, sticky = tkinter.W)
        self.exit_button = tkinter.Button(self.parent, text = "Exit", command = self.parent.quit)
        self.exit_button.grid(row = 0, column = 3)

        # Set the treeview
        self.tree = ttk.Treeview( self.parent, columns=('Dose', 'Modification date'))
        self.tree.heading('#0', text='Ime')
        self.tree.heading('#1', text='Prezime')
        self.tree.heading('#2', text='LBO')
        self.tree.column('#1', stretch=tkinter.YES)
        self.tree.column('#2', stretch=tkinter.YES)
        self.tree.column('#0', stretch=tkinter.YES)
        self.tree.grid(row=4, columnspan=4, sticky='nsew')
        self.treeview = self.tree
        # Initialize the counter
        self.i = 0



    def showInsert(self):
        self.parent.withdraw()
        self.newWindow = tkinter.Toplevel(self.parent)
        bb = AddNew(self.newWindow, Main)


    def insert_data(self):
        """
        Insertion method.
        """
        self.treeview.insert('', 'end', text="Item_"+str(self.i), values=(self.dose_entry.get()+" mg", self.modified_entry.get()))
        # Increment counter
        self.i = self.i + 1



def main():
    root=tkinter.Tk()
    d=Main(root)
    root.mainloop()

if __name__=="__main__":
    main()
