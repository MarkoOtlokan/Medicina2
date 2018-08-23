from tkinter import ttk
from tkinter import messagebox
import tkinter
from Patient import Patient
import calendar
import datetime
from datetime import date

class Change(tkinter.Frame):

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


                self.Current_label = tkinter.Label(self.parent, text = "Trenutne vrednosti:")
                self.Current_label.grid(row = 1, column = 1, sticky = tkinter.W)

                self.New_label = tkinter.Label(self.parent, text = "Nove/izmenjene vrednosti:")
                self.New_label.grid(row = 1, column = 2, sticky = tkinter.W)

                self.LBO_label = tkinter.Label(self.parent, text = self.patient.LBO)
                self.LBO_podaci = tkinter.Label(self.parent, text = "LBO:")
                self.LBO_podaci.grid(row = 2, column = 0, sticky = tkinter.W)
                self.LBO_label.grid(row = 2, column = 1, sticky = tkinter.W)

                self.name_label = tkinter.Label(self.parent, text = self.patient.name)
                self.name_entry = tkinter.Entry(self.parent)
                self.name_podaci = tkinter.Label(self.parent, text = "Ime:")
                self.name_podaci.grid(row = 3, column = 0, sticky = tkinter.W)
                self.name_label.grid(row = 3, column = 1, sticky = tkinter.W)
                self.name_entry.grid(row = 3, column = 2)

                self.surname_label = tkinter.Label(self.parent, text = self.patient.surname)
                self.surname_entry = tkinter.Entry(self.parent)
                self.surname_podaci = tkinter.Label(self.parent, text = "Prezime:")
                self.surname_podaci.grid(row = 4, column = 0, sticky = tkinter.W)
                self.surname_label.grid(row = 4, column = 1, sticky = tkinter.W)
                self.surname_entry.grid(row = 4, column = 2)

                self.date_of_birth_label = tkinter.Label(self.parent, text = self.patient.date_of_birth)
                self.date_of_birth_podaci = tkinter.Label(self.parent, text = "Datum rodjenja:")
                self.date_of_birth_podaci.grid(row = 5, column = 0, sticky = tkinter.W)
                self.date_of_birth_label.grid(row = 5, column = 1, sticky = tkinter.W)
                self.date_Button = ttk.Button(self.parent, text='Izaberi',command=self.calCal)
                self.date_Button.grid(row = 5, column = 3)

                self.submit_button = tkinter.Button(self.parent, text = "Potvrdi", command = self.check)
                self.submit_button.grid(row = 3, column = 4, sticky = tkinter.W)
                self.exit_button = tkinter.Button(self.parent, text = "Nazad", command = self.goBack)
                self.exit_button.grid(row = 4, column = 4)

        def check(self):
                tmpName = self.name_entry.get()
                tmpSurname = self.surname_entry.get()
                try :
                    self.date
                    tmpDate_of_birth = self.date.cget("text")
                except:
                    tmpDate_of_birth = self.patient.date_of_birth
                print(tmpName,tmpSurname,tmpDate_of_birth)
                if not tmpName:
                        tmpName = self.patient.name
                if not tmpSurname:
                        tmpSurname = self.patient.surname

                patiente = Patient.xmlToList()
                del patiente[int(self.patient.LBO)]
                Patient.saveXML(patiente)
                newPatient = Patient(self.patient.LBO, tmpName, tmpSurname, tmpDate_of_birth)
                Patient.addNewPatient(newPatient)
                messagebox.showinfo("Uspeh", "Uspesno ste izmenili")
                self.goBack()


        def calCal(self):
                child = tkinter.Toplevel()
                cal = Calendar(child, Change, self)

        def fillDate(self):
                if self.data == {}:
                    return
                self.date = tkinter.Label(self.parent, text=str(self.data['year_selected'])+"-"+str(self.data['month_selected'])+"-"+str(self.data['day_selected']))
                self.date.grid(row = 5, column = 2)

        def setDate(self,data):
                self.data = data
                self.fillDate()


        def goBack(self):
                self.parent.withdraw()
                self.newWindow = tkinter.Toplevel(self.parent)
                bb = self.otac(self.newWindow)


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

		ok = tkinter.Button(self.parent, width=5, text='OK', command=self.check)# i ovde postoji izmena command=self.check
		self.wid.append(ok)															# takodje treba da se from datetime import date
		ok.grid(row=9, column=2, columnspan=3, pady=10)

	def check(self): ############## novi deo koda $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
		print(self.values)
		today = date.today()
		print(today)
		if(today.year < int(self.values['year_selected'])):
			messagebox.showinfo("Greska", "Mora biti bar danasnji datum")
			return
		if(today.year == int(self.values['year_selected'])):
			if(today.month < int(self.values['month_selected'])):
				messagebox.showinfo("Greska", "Mora biti bar danasnji datum")
				return
			if(today.month == int(self.values['month_selected'])):
				if(today.day < int(self.values['day_selected'])):
					messagebox.showinfo("Greska", "Mora biti bar danasnji datum")
					return
		self.kill_and_save()

	def kill_and_save(self):
		self.otac.setDate(self.selfP,self.values)
		self.parent.destroy()
