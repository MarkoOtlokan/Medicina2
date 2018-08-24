from tkinter import ttk
from tkinter import messagebox
import tkinter
from MedicalExamination import MedicalExamination
from tkinter import filedialog
import calendar
import datetime
from AddNew import Dicom


class ChangeMed(tkinter.Frame):

    def __init__(self, parent, otac, med, pat,ot):
        self.ot = ot
        self.med = med
        self.pat = pat
        self.otac = otac
        self.parent=parent
        self.patient = pat
        self.frame = tkinter.Frame(self.parent)
        self.initialize_insert_interface()

    def initialize_insert_interface(self):
        self.parent.title("Canvas Test")
        self.parent.grid_rowconfigure(0,weight=1)
        self.parent.grid_columnconfigure(0,weight=1)
        self.parent.config(background="lavender")
        self.Current_label = tkinter.Label(self.parent, text = "Trenutne vrednosti:")
        self.Current_label.grid(row = 1, column = 1, sticky = tkinter.W)
        self.New_label = tkinter.Label(self.parent, text = "Nove/izmenjene vrednosti")
        self.New_label.grid(row = 1, column = 2, sticky = tkinter.W)

        self.date_label = tkinter.Label(self.parent, text = self.med.date)
        self.date_of_birth_podaci = tkinter.Label(self.parent, text = "Datum pregleda:")
        self.date_of_birth_podaci.grid(row = 2, column = 0, sticky = tkinter.W)
        self.date_label.grid(row = 2, column = 1, sticky = tkinter.W)
        self.date_Button = ttk.Button(self.parent, text='Izaberi',command=self.calCal)
        self.date_Button.grid(row = 2, column = 3)

        self.option_label = tkinter.Label(self.parent, text = self.med.type)
        self.var = tkinter.StringVar()
        self.var.set("Izaberi") # initial value
        self.optionList = ['CT', 'MR','XA','RF', 'US','ECG']
        self.option = tkinter.OptionMenu(self.parent,self.var, *self.optionList)
        self.option_podaci = tkinter.Label(self.parent, text = "Tip pregleda:")
        self.option_podaci.grid(row = 3, column = 0, sticky = tkinter.W)
        self.option.grid(row = 3, column = 2)
        self.option_label.grid(row = 3, column = 1, sticky = tkinter.W)


        self.report_label = tkinter.Label(self.parent, text = self.med.report)
        self.report_entry = tkinter.Entry(self.parent)
        self.report_podaci = tkinter.Label(self.parent, text = "Izvestaj:")
        self.report_podaci.grid(row = 4, column = 0, sticky = tkinter.W)
        self.report_label.grid(row = 4, column = 1, sticky = tkinter.W)
        self.report_entry.grid(row = 4, column = 2)

        self.doctor_label = tkinter.Label(self.parent, text = self.med.doctor)
        self.doctor_entry = tkinter.Entry(self.parent)
        self.doctor_podaci = tkinter.Label(self.parent, text = "Doktor:")
        self.doctor_podaci.grid(row = 5, column = 0, sticky = tkinter.W)
        self.doctor_label.grid(row = 5, column = 1, sticky = tkinter.W)
        self.doctor_entry.grid(row = 5, column = 2)

        self.dicom_label = tkinter.Label(self.parent, text = self.med.dicom)
        self.dicom_label.grid(row = 6, column = 1, sticky = tkinter.W)
        self.dicom_podaci = tkinter.Label(self.parent, text = "Dicom putanja:")
        self.dicom_podaci.grid(row = 6, column = 0, sticky = tkinter.W)

        self.dicom_entry = tkinter.Entry(self.parent)
        self.dicom_entry.grid(row = 6, column = 2)
        self.odabirSnimka = tkinter.Button(self.parent,text = '...', width = 5, command = self.klikNaodabir_snimkaDugme)
        self.odabirSnimka.grid(row = 6, column = 3)
        self.goDic_button = tkinter.Button(self.parent, text = "Otvori", command = self.otvori, state=tkinter.DISABLED)
        self.goDic_button.grid(row = 6, column = 4, sticky = tkinter.W)


        self.submit_button = tkinter.Button(self.parent, text = "Potvrdi", command = self.check)
        self.submit_button.grid(row = 3, column = 4, sticky = tkinter.W)
        self.exit_button = tkinter.Button(self.parent, text = "Nazad", command = self.goBack)
        self.exit_button.grid(row = 4, column = 4)

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
        self.dicom_entry.delete(0, tkinter.END)
        self.dicom_entry.insert(tkinter.END,self.route)
        self.goDic_button.configure(state=tkinter.NORMAL)

    def otvori(self):
        child = tkinter.Toplevel()
        dic = Dicom(child,self.otac,self.dicom_entry.get(),self.patient, self.med)

    def check(self):
    #    tmpDate = self.date
        tmpDoctor = self.doctor_entry.get()
        tmpReport = self.report_entry.get()
        tmpDicom = self.dicom_entry.get()
        tmpType = self.var.get()
        try :
            self.date
            tmpDate = self.date.cget("text")
        except:
            tmpDate = self.med.date
        if not tmpDoctor:
            tmpDoctor = self.med.doctor
        if not tmpReport:
            tmpReport = self.med.report
        if not tmpDicom:
            tmpDicom = self.med.dicom
        if tmpType == "Izaberi":
            tmpType = self.med.type

        meds = MedicalExamination.xmlToList()
        del meds[int(self.med.id)]
        MedicalExamination.saveXML(meds)
        newMed = MedicalExamination(self.med.id,self.med.patient_LBO, tmpDate, tmpType, tmpReport, tmpDoctor, tmpDicom)
        MedicalExamination.addNewMed(newMed)
        messagebox.showinfo("Uspeh", "Uspesno ste izmenili")
        self.goBack()


    def goBack(self):
        self.parent.withdraw()
        self.newWindow = tkinter.Toplevel(self.parent)
        bb = self.otac(self.newWindow, self.ot,self.pat)

    def calCal(self):
                child = tkinter.Toplevel()
                cal = Calendar(child, ChangeMed, self)

    def fillDate(self):
            if self.data == {}:
                return
            self.date = tkinter.Label(self.parent, text=str(self.data['year_selected'])+"-"+str(self.data['month_selected'])+"-"+str(self.data['day_selected']))
            self.date.grid(row = 2, column = 2)

    def setDate(self,data):
            self.data = data
            self.fillDate()

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
