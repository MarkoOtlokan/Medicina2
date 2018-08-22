from tkinter import ttk
from tkinter import messagebox
import tkinter
from Patient import Patient
from MedicalExamination import MedicalExamination
from AddNew import DodajPregled

class Dicom(tkinter.Frame):

	def __init__(self, parent, otac, path):
        self.parent = parent
        self.otac = otac
        self.path = path

		def klikNaOtvoriDugme(self):
		    try:
		    # otvaranje dijalog prozora za odabir datoteke
		        stazaDoDatoteke = filedialog.askopenfilename(
		            initialdir = "./DICOM samples",
		            title = "Otvaranje",
		            filetypes = [("DICOM files", "*.dcm"), ("All files", "*.*")])
		        if stazaDoDatoteke == "": # korisnik otkazao dijalog?
		            return
		        # otvaranje može da potraje; postaviti kursor miša na čekajući
		        #self["cursor"] = "wait"
		        self.update()

		        self.__stazaDoDatoteke = stazaDoDatoteke # pamćenje staze do datoteke radi čuvanja
		        self.__dataset = pydicom.read_file(self.__stazaDoDatoteke, force = True) # otvaranje DICOM datoteke; force parametar obezbeđuje čitanje nepotpunih datoteka
		        print(self.__dataset)

		        self.title(self.__stazaDoDatoteke)
		        # omogućavanje interfejsa za izmenu i čuvanje
		        self.__pacijentPrisutanCheckbutton["state"] = NORMAL
		        self.__polPrisutanCheckbutton["state"] = NORMAL
		        self.__starostPrisutnaCheckbutton["state"] = NORMAL
		        self.__ocistiDugme["state"] = NORMAL
		        self.__sacuvajDugme["state"] = NORMAL
		        self.__fileMeni.entryconfig(2, state = NORMAL)
		        self.__fileMeni.entryconfig(3, state = NORMAL)

		        # podaci DICOM datoteke ne moraju da postoje
		        if "PatientName" in self.__dataset: # da li podatak postoji u dataset-u?
		            self.__pacijent.set(self.__dataset.PatientName) # vrednost podatka
		            self.__pacijentPrisutan.set(True) # podatak pronađen?
		        else:
		            self.__pacijentPrisutan.set(False)

		        if "PatientSex" in self.__dataset:
		            for vrednost, tekst in [("M", "muški"), ("F", "ženski"), ("O", "drugi")]: # 3 moguće vrednosti: M, F, O
		                if vrednost == self.__dataset.PatientSex:
		                    self.__pol.set(tekst)
		                    break
		            self.__polPrisutan.set(True)
		        else:
		            self.__polPrisutan.set(False)

		        if "PatientAge" in self.__dataset:
		            try:
		                self.__starost.set(int(self.__dataset.PatientAge[:-1])) # sve do poslednjeg karaktera je vrednost
		                self.__starostJedinica.set(self.__dataset.PatientAge[-1]) # poslednji karakter je jedinica mere; Y, M, W, D
		                self.__starostPrisutna.set(True)
		            except ValueError: # možda podatak postoji, ali ne može da se parsira u int
		                pass
		        else:
		            self.__starostPrisutna.set(False)

		        self.azurirajStanja() # omogućavanje polja za izmenu na osnovu pročitanih podataka
		        print("ziv-1")
		        pilSlika = pydicom_PIL.get_PIL_image(self.__dataset) # pokušaj dekompresije i čitanja slike iz dataset objekta
		        print("ziv0")
		        sirina = pilSlika.width
		        visina = pilSlika.height
		        print("originalne dimenzije:", sirina, ",", visina)

		        maksDimenzija = 900
		        if sirina > maksDimenzija or visina > maksDimenzija:
		            if sirina > visina: # smanjiti sliku po većoj od 2 dimenzije
		                odnos = maksDimenzija/sirina
		                sirina = maksDimenzija
		                visina = int(odnos*visina) # manja dimenzija se smanjuje proporcionalno
		            else:
		                odnos = maksDimenzija/visina
		                sirina = int(odnos*sirina) # manja dimenzija se smanjuje proporcionalno
		                visina = maksDimenzija
		        print("ziv1")
		        print("nove dimenzije:", sirina, ",", visina)
		        pilSlika = pilSlika.resize((sirina, visina), Image.LANCZOS) # LANCZOS metoda je najbolja za smanjivanje slike
		        slika = ImageTk.PhotoImage(pilSlika) # PIL slika se mora prevesti u TkInter sliku (ImageTk)
		        self.__slikaLabela["image"] = slika
		        self.__slikaLabela.image = slika
		    except:
		        # PIL slika se mora prevesti u TkInter sliku (ImageTk)
		        #slika = ImageTk.PhotoImage(Image.new('L', (200, 200))) # crna slika dimenzija 200x200 piksela
		        slika = ImageTk.PhotoImage(Image.open("DICOM-Logo.jpg")) # bilo koja druga podrazumevana slika
		        self.__slikaLabela["image"] = slika  # labeli se dodeljuje slika
		        self.__slikaLabela.image = slika  # referenca na TkInter sliku se mora sačuvati, inače nece biti prikazana!
		        print("nesto2")
		    self["cursor"] = "" # reset-ovanje pokazivača miša na podrazumevani
		    print("nista")
