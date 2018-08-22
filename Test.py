import sys
sys.path.append('./MedicalExamination')
sys.path.append('./Patient.py')
from MedicalExamination import MedicalExamination
from Patient import Patient


def Test():
    med2 = MedicalExamination(12346,17162739481,"2015-04-29","CT","ne uspesan","pocek","neka putanja")

    meds = {}
    meds[med2.id] = med2
    MedicalExamination.saveXML(meds)
    natasa = Patient(17162739481,'s','ss','sd')

    medL = MedicalExamination.readXML()
    Patient.pronadjiPreglede(natasa)

if __name__ == '__main__':
    Test()
