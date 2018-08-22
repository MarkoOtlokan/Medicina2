from tkinter import ttk
import tkinter
from AddNew import AddNew
from Change import Change
from Patient import Patient
from Pregledi import Pregledi
from tkinter import messagebox

class Main(tkinter.Frame):
    
    def __init__(self, parent):
        self.patiente = []
        self.patienteKeys=[]
        tkinter.Frame.__init__(self, parent)
        self.parent=parent

        self.initialize_user_interface()

    def initialize_user_interface(self):
        self.patiente = Patient.readXML() # zbog update
        self.parent.title("Canvas Test")
        self.parent.grid_rowconfigure(0,weight=1)
        self.parent.grid_columnconfigure(0,weight=1)
        self.parent.config(background="lavender")


        # Define the different GUI widgets

        self.submit_button = tkinter.Button(self.parent, text = "Dodaj pacijenta", command = self.showInsert)
        self.submit_button.grid(row = 1, column = 1, sticky = tkinter.W)

        # Set the treeview
        self.tree = ttk.Treeview(self.parent, columns=('surname', 'name','LBO'))
        self.tree.heading('surname', text='Prezime')
        self.tree.heading('name', text='Ime')
        self.tree.heading('LBO', text='LBO')
        self.tree.column('surname')
        self.tree.column('name')
        self.tree.column('LBO')
        self.tree.grid(row=1, column=0, sticky='nsew')
        self.tree['show'] = 'headings'

        # Initialize the counter

        self.insert_data()



    def showInsert(self):
        self.parent.withdraw()
        self.newWindow = tkinter.Toplevel(self.parent)
        bb = AddNew(self.newWindow, Main, self.patienteKeys)

    def showChange(self,patient):
        self.parent.withdraw()
        self.newWindow = tkinter.Toplevel(self.parent)
        bb = Change(self.newWindow, Main, patient)

    def insert_data(self):
        
        for patientElement in self.patiente:
            self.patienteKeys.append(patientElement.LBO)
            self.tree.insert('', '0', values=(patientElement.surname,patientElement.name,patientElement.LBO))
        self.tree.bind('<<TreeviewSelect>>', self.OnClick)

    def OnClick(self, event):
        item = self.tree.selection()[0]
        tmp = self.tree.item(item)
        list = tmp.get('values')
        tmpLBO = list[2]
        for patient in self.patiente:
            if str(tmpLBO) == str(patient.LBO):
                self.writeDataOfPatient(patient)
                return

    def writeDataOfPatient(self,patientC):
        self.dose_label = tkinter.Label(self.parent, text = "Prezime:" + patientC.surname)
        self.dose_label.grid(row = 2, column = 0, sticky = tkinter.W)
        self.dose_label = tkinter.Label(self.parent, text = "Ime:" + patientC.name)
        self.dose_label.grid(row = 3, column = 0, sticky = tkinter.W)
        self.dose_label = tkinter.Label(self.parent, text = "LBO:" + patientC.LBO)
        self.dose_label.grid(row = 4, column = 0, sticky = tkinter.W)
        self.dose_label = tkinter.Label(self.parent, text = "Datum rodjenja:" + str(patientC.date_of_birth))
        self.dose_label.grid(row = 5, column = 0, sticky = tkinter.W)
        self.submit_button = tkinter.Button(self.parent, text = "Obrisi pacijeta", command = lambda: self.dPatient(patientC.LBO))
        self.submit_button.grid(row = 2, column = 1, sticky = tkinter.W)
        self.submit_button = tkinter.Button(self.parent, text = "Izmeni", command = lambda: self.showChange(patientC))
        self.submit_button.grid(row = 3, column = 1, sticky = tkinter.W)
        self.submit_button = tkinter.Button(self.parent, text = "Pregledi", command = lambda: self.goToPregledi(patientC))
        self.submit_button.grid(row = 4, column = 1, sticky = tkinter.W)


    def goToPregledi(self, patientC):
        self.parent.withdraw()
        self.newWindow = tkinter.Toplevel(self.parent)
        bb = Pregledi(self.newWindow, Main, patientC)

    def dPatient(self,lbo):
        self.win = tkinter.Toplevel()
        self.win.title('warning')
        message = "Da li ste sigurni da zelite da obrisete pacijenta ?"
        tkinter.Label(self.win, text=message).pack()
        tkinter.Button(self.win, text='Obrisi', command=lambda:self.deletePatient(lbo)).pack()
        tkinter.Button(self.win, text='Odustani', command=self.win.destroy).pack()

    def deletePatient(self, LBO):
        self.win.destroy()
        patiente = Patient.xmlToList()
        del patiente[int(LBO)]
        Patient.saveXML(patiente)
        self.initialize_user_interface()
        messagebox.showinfo("Uspeh", "Uspesno ste obrisali pacijenta")

def main():
    root=tkinter.Tk()
    d=Main(root)
    root.mainloop()

if __name__=="__main__":
    main()
