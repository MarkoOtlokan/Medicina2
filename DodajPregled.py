from tkinter import ttk
from tkinter import messagebox
import tkinter
from Patient import Patient
import calendar
import datetime
from Call import Calendar
import uuid
from tkinter import filedialog
from MedicalExamination import MedicalExamination
class DodajPregled(tkinter.Frame):

	def __init__(self, parent,otac, patientKey,first, second): #first i second sluze samo da bi se vratio na prosli nivo
		self.route = ""
		self.first = first
		self.second = second
		self.patientKey = patientKey
		self.otac = otac
		self.data = {}
		self.parent = parent
		self.id = str(uuid.uuid4().int & (1<<32)-1)
		self.frame = tkinter.Frame(self.parent)
		self.initialize_insert_interface()

	def initialize_insert_interface(self):
		self.parent.title("Canvas Test")
		self.parent.grid_rowconfigure(0,weight=1)
		self.parent.grid_columnconfigure(0,weight=1)
		self.parent.config(background="lavender")
		self.naslov_label = tkinter.Label(self.parent, text = "DODAJ NOVI PREGLED")
		self.naslov_label.grid(row = 0, column = 0, sticky = tkinter.W)
		self.id_label = tkinter.Label(self.parent, text = "ID: "+self.id)
		self.id_label.grid(row = 2, column = 0, sticky = tkinter.W)
		self.date_of_birth_label = tkinter.Label(self.parent, text = "Datum pregleda:")
		self.date_of_birth_entry = tkinter.Entry(self.parent)
		self.date_of_birth_label.grid(row = 4, column = 0, sticky = tkinter.W)
		self.date_of_birth_entry.grid(row = 4, column = 1)

		self.date_Button = ttk.Button(self.parent, text='Izaberi',command=self.calCal)
		self.date_Button.grid(row = 4, column = 2)

		self.option_label = tkinter.Label(self.parent, text = "Vrsta pregleda:")
		self.option_label.grid(row = 5, column = 0, sticky = tkinter.W)
		self.var = tkinter.StringVar()
		self.var.set("CT") # initial value
		self.optionList = ['CT', 'MR','XA','RF', 'US','ECG']
		self.option = tkinter.OptionMenu(self.parent,self.var, *self.optionList)
		self.option.grid(row = 5, column = 1)
		self.report_label = tkinter.Label(self.parent, text = "Izvestaj:")
		self.report_entry = tkinter.Entry(self.parent)
		self.report_label.grid(row = 6, column = 0, sticky = tkinter.W)
		self.report_entry.grid(row = 6, column = 1)
		self.doctor_label = tkinter.Label(self.parent, text = "Doktor:")
		self.doctor_entry = tkinter.Entry(self.parent)
		self.doctor_label.grid(row = 7, column = 0, sticky = tkinter.W)
		self.doctor_entry.grid(row = 7, column = 1)
		self.dicom_label = tkinter.Label(self.parent, text = "Snimak:")
		self.dicom_entry = tkinter.Entry(self.parent)
		self.dicom_label.grid(row = 8, column = 0, sticky = tkinter.W)
		self.dicom_entry.grid(row = 8, column = 1)
		self.odabirSnimka = tkinter.Button(self.parent,text = '...', width = 5, command = self.klikNaodabir_snimkaDugme)
		self.odabirSnimka.grid(row = 8, column = 2)
		self.submit_button = tkinter.Button(self.parent, text = "Dodaj pregled", command = self.check)
		self.submit_button.grid(row = 9, column = 0, sticky = tkinter.W)
		self.filename =  tkinter.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = [("all files","*.*")])
		self.exit_button = tkinter.Button(self.parent, text = "Nazad", command = self.goBack)
		self.exit_button.grid(row = 10, column = 0)

	def check(self):
                self.fillDate()
		tmpMed = MedicalExamination(self.id,self.patientKey,self.date_of_birth_entry.get(),  self.var.get(), self.report_entry.get(), self.doctor_entry.get(),self.dicom_entry.get() )
		MedicalExamination.addNewMed(tmpMed)
		messagebox.showinfo("Uspeh", "Uspesno ste uneli pacijenta")
		self.goBack()

	def goBack(self):
		self.parent.withdraw()
		self.newWindow = tkinter.Toplevel(self.parent)
		bb = self.otac(self.newWindow,self.first, self.second)

	def calCal(self):
		child = tkinter.Toplevel()
		cal = Calendar(child, self.data)

	def klikNaodabir_snimkaDugme(self):

		stazaDoDatoteke = filedialog.askopenfilename(
		initialdir = "./DICOM samples",
		title = "Otvaranje",
		filetypes = (("DICOM files", "*.dcm"),))

		try:
			s = stazaDoDatoteke.split('/')

			s1 = s[-1]
			s2 = s[-2]

			s= '/'.join(['.',s2,s1])
			stazaDoDatoteke = s
		except:
			return
		self.route = stazaDoDatoteke
		self.dicom_entry.insert(tkinter.END,self.route)

	def fillDate(self):
		self.date_of_birth_entry.insert(0, str(self.data['year_selected'])+"-"+str(self.data['month_selected'])+"-"+str(self.data['day_selected']))

class Calendar:
	def __init__(self, parent,otac,selfP):
		self.values = {}
		self.selfP = selfP
		self.parent = parent
		self.cal = calendar.TextCalendar(calendar.SUNDAY)
		self.year = datetime.date.today().year
		self.month = datetime.date.today().month
		self.otac = otac
		self.wid = []
		self.day_selected = 1
		self.month_selected = self.month
		self.year_selected = self.year
		self.day_name = ''

		self.setup(self.year, self.month)

	def clear(self):
		for w in self.wid[:]:
			w.grid_forget()
			self.wid.remove(w)

	def go_prev(self):
		if self.month > 1:
			self.month -= 1
		else:
			self.month = 12
			self.year -= 1
		self.clear()
		self.setup(self.year, self.month)

	def go_next(self):
		if self.month < 12:
			self.month += 1
		else:
			self.month = 1
			self.year += 1

		self.clear()
		self.setup(self.year, self.month)

	def selection(self, day, name):
		self.day_selected = day
		self.month_selected = self.month
		self.year_selected = self.year
		self.day_name = name

		if day > 9:
			self.values['day_selected'] = day
		else:
			self.values['day_selected'] = "0"+str(day)
		if self.month > 9:
			self.values['month_selected'] =  self.month
		else:
			self.values['month_selected'] = "0"+str(self.month)

		self.values['year_selected'] = self.year
		self.values['day_name'] = name
		self.values['month_name'] = calendar.month_name[self.month_selected]

		self.clear()
		self.setup(self.year, self.month)

	def setup(self, y, m):
		left = tkinter.Button(self.parent, text='<', command=self.go_prev)
		self.wid.append(left)
		left.grid(row=0, column=1)

		header = tkinter.Label(self.parent, height=2, text='{}   {}'.format(calendar.month_abbr[m], str(y)))
		self.wid.append(header)
		header.grid(row=0, column=2, columnspan=3)

		right = tkinter.Button(self.parent, text='>', command=self.go_next)
		self.wid.append(right)
		right.grid(row=0, column=5)

		days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
		for num, name in enumerate(days):
			t = tkinter.Label(self.parent, text=name[:3])
			self.wid.append(t)
			t.grid(row=1, column=num)

		for w, week in enumerate(self.cal.monthdayscalendar(y, m), 2):
			for d, day in enumerate(week):
				if day:
					b = tkinter.Button(self.parent, width=1, text=day, command=lambda day=day:self.selection(day, calendar.day_name[(day-1) % 7]))
					self.wid.append(b)
					b.grid(row=w, column=d)

		sel = tkinter.Label(self.parent, height=2, text='{} {} {} {}'.format(self.day_name, calendar.month_name[self.month_selected], self.day_selected, self.year_selected))
		self.wid.append(sel)
		sel.grid(row=8, column=0, columnspan=7)

		ok = tkinter.Button(self.parent, width=5, text='OK', command=self.kill_and_save)
		self.wid.append(ok)
		ok.grid(row=9, column=2, columnspan=3, pady=10)

	def kill_and_save(self):
		self.otac.setDate(self.selfP,self.values)
		self.parent.destroy()

	def goBack(self):
		self.parent.withdraw()
		self.newWindow = tkinter.Toplevel(self.parent)
		bb = self.otac(self.newWindow)
