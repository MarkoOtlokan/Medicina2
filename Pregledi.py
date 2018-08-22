from tkinter import ttk
from tkinter import messagebox
import tkinter
from Patient import Patient
from MedicalExamination import MedicalExamination
from AddNew import DodajPregled
from AddNew import Dicom
from ChangeMed import ChangeMed

class Pregledi(tkinter.Frame):

	def __init__(self, parent, otac, patient):
		self.patient = patient

		self.otac = otac
		self.parent=parent
		self.frame = tkinter.Frame(self.parent)
		self.initialize_insert_interface()

	def initialize_insert_interface(self):
		self.parent.title("Canvas Test")
		self.parent.grid_rowconfigure(0,weight=1)
		self.parent.grid_columnconfigure(0,weight=1)
		self.parent.config(background="lavender")
		self.LBO_label = tkinter.Label(self.parent, text = "Ime:   " + self.patient.name)

		self.LBO_label.grid(row = 1, column = 0, sticky = tkinter.W)

		self.name_label = tkinter.Label(self.parent, text = "Prezime:   " +self.patient.surname)

		self.name_label.grid(row = 2, column = 0, sticky = tkinter.W)

		self.surname_label = tkinter.Label(self.parent, text = "LBO:   " + self.patient.LBO)

		self.surname_label.grid(row = 3, column = 0, sticky = tkinter.W)

		self.exit_button = tkinter.Button(self.parent, text = "Dodaj pregled", command = self.addExamination)
		self.exit_button.grid(row = 4, column = 1)

		self.exit_button = tkinter.Button(self.parent, text = "Nazad", command = self.goBack)
		self.exit_button.grid(row = 9, column = 1, sticky = tkinter.W)

		self.tree = ttk.Treeview(self.parent, columns=('date', 'type','id'))
		self.tree.heading('date', text='Datum')
		self.tree.heading('type', text='Tip pregleda')
		self.tree.heading('id', text='ID')
		self.tree.column('date')
		self.tree.column('type')
		self.tree.column('id')
		self.tree.grid(row=4, column=0, sticky='nsew')

		self.tree['show'] = 'headings'

		self.writeMedicalExamination(self.patient.LBO)

	def addExamination(self):
		self.parent.withdraw()
		self.newWindow = tkinter.Toplevel(self.parent)
		bb = DodajPregled(self.newWindow, Pregledi,self.patient.LBO,self.otac,self.patient)

	def writeMedicalExamination(self,LBO):
		self.medL = MedicalExamination.readXML()
		for med in self.medL:
			if(med.patient_LBO == self.patient.LBO): #spajanje pacijenata i pregleda
				self.tree.insert('', '0', values=(med.date,med.type,med.id))
				self.tree.bind('<<TreeviewSelect>>', lambda x: self.writeDataOfMed(med.id))


	def writeDataOfMed(self,id):
		item = self.tree.selection()[0]
		tmp = self.tree.item(item)
		list = tmp.get('values')
		tmpId = list[2]
		for med in self.medL:
			if str(tmpId) == str(med.id):
				self.id_label = tkinter.Label(self.parent, text = "ID:   " + med.id)
				self.id_label.grid(row = 5, column = 0, sticky = tkinter.W)
				self.LBO_label = tkinter.Label(self.parent, text = "LBO pacijenta:   " + med.patient_LBO)
				self.LBO_label.grid(row = 6, column = 0, sticky = tkinter.W)
				self.date_label = tkinter.Label(self.parent, text = "Datum pregleda:   " + med.date)
				self.date_label.grid(row = 7, column = 0, sticky = tkinter.W)
				self.report_label = tkinter.Label(self.parent, text = "Izvestaj:   "+ med.report)
				self.report_label.grid(row = 8, column = 0, sticky = tkinter.W)
				self.doctor_label = tkinter.Label(self.parent, text = "Doktor:   "+ med.doctor)
				self.doctor_label.grid(row = 9, column = 0, sticky = tkinter.W)
				self.dicom_label = tkinter.Label(self.parent, text = "Dicom putanja:   "+ med.dicom)
				self.dicom_label.grid(row = 10, column = 0, sticky = tkinter.W)
				self.dicom_button = tkinter.Button(self.parent, text = "Prikazi dicom", command = lambda: self.goToDicom(med.dicom))
				self.dicom_button.grid(row = 6, column = 1, sticky = tkinter.W)
				self.delete_button = tkinter.Button(self.parent, text = "Obrisi pregled", command = lambda: self.dMed(med.id))
				self.delete_button.grid(row = 7, column = 1, sticky = tkinter.W)
				self.change_button = tkinter.Button(self.parent, text = "Izmeni", command = lambda: self.showChange(med))
				self.change_button.grid(row = 8, column = 1, sticky = tkinter.W)

	def goToDicom(self, path):
		self.newWindow = tkinter.Toplevel(self.parent)
		bb = Dicom(self.newWindow, Pregledi, path)

	def dMed(self,id):
		self.win = tkinter.Toplevel()
		self.win.title('warning')
		message = "Da li ste sigurni da zelite da obrisete pregled ?"
		tkinter.Label(self.win, text=message).pack()
		tkinter.Button(self.win, text='Obrisi', command=lambda:self.deleteMed(id)).pack()
		tkinter.Button(self.win, text='Odustani', command=self.win.destroy).pack()

	def deleteMed(self, id):
		self.win.destroy()
		med = MedicalExamination.xmlToList()
		print(med[int(id)])
		del med[int(id)]
		MedicalExamination.saveXML(med)
		self.initialize_insert_interface()
		messagebox.showinfo("Uspeh", "Uspesno ste obrisali pregled")

	def showChange(self,med):
		self.parent.withdraw()
		self.newWindow = tkinter.Toplevel(self.parent)
		bb = ChangeMed(self.newWindow, Pregledi, med,self.patient,self.otac)


	def goBack(self):
		self.parent.withdraw()
		self.newWindow = tkinter.Toplevel(self.parent)
		bb = self.otac(self.newWindow)
