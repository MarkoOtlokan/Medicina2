from lxml import etree


class MedicalExamination(object):
    """docstring for MedicalExamination."""

    __tipovi_pregleda = ['CT', 'MR','XA','RF', 'US','ECG']

    __nameSD = "MedicalExamination.xsd"
    __nameXML = "MedicalExamination.xml"

    @property
    def patient_LBO(self):
        return self.__patient_LBO

    @patient_LBO.setter
    def patient_LBO(self, patient_LBO):
        self.__patient_LBO = patient_LBO


    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def report(self):
        return self.__report

    @report.setter
    def report(self, report):
        self.__report = report

    @property
    def doctor(self):
        return self.__doctor

    @doctor.setter
    def doctor(self, doctor):
        self.__doctor = doctor

    @property
    def dicom(self):
        return self.__dicom

    @dicom.setter
    def dicom(self, dicom):
        self.__dicom = dicom


    def __init__(self, id,patient_LBO, date, type, report ,doctor,dicom):
        self.__id = id
        self.__patient_LBO = patient_LBO
        self.__date = date
        self.__type = type
        self.__report = report
        self.__doctor = doctor
        self.__dicom = dicom

    def __str__(self):
        return "\n".join([
            "{:>12}: {}".format("id", self.__id),
            "{:>12}: {}".format("lbo", self.__patient_LBO),
            "{:>12}: {}".format("date", self.__date),
            "{:>12}: {}".format("report", self.__report),
            "{:>12}: {}".format("type", self.__type),
            "{:>12}: {}".format("doctor", self.__doctor),
            "{:>12}: {}".format("dicom", self.__dicom)]
            )

    def makeEL(self):
        element = etree.Element("MedicalExamination") # novi Element objekat
        element.append(etree.Element("patient_LBO")) # dodavanje iza poslednjeg podelementa Element objekta
        element.append(etree.Element("date"))
        element.append(etree.Element("type"))
        element.append(etree.Element("report"))
        element.append(etree.Element("doctor"))
        element.append(etree.Element("dicom"))

        element.attrib["id"] = str(self.__id)
        element[0].text = str(self.__patient_LBO)
        element[1].text = str(self.__date)
        element[2].text = self.__type
        element[3].text = self.__report
        element[4].text = self.__doctor
        element[5].text = self.__dicom

        return element

    @classmethod
    def saveXML(_class, medical_examinations):
        namespaces = {"xsi" : "http://www.w3.org/2001/XMLSchema-instance"}
        # nazivi elemenata/atributa sa namespace prefiksom se moraju navesti u formatu: {staza}naziv
        # naziv ogovara nazivu elementa/atributa
        # Element automatski zamenjuje stazu odgovarajućim namespace prefiksom navedenim u rečniku namespace-ova
        attributes = {"{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation": _class.__nameSD}

        # Element se moze inicijalizovati nazivom i opciono rečnikom atributa i/ili rečnikom namespace-ova
        medSEL = etree.Element("MedicalExamination", attributes, namespaces)


        for id in medical_examinations.keys():
            med = medical_examinations[id]
            medEL = _class.makeEL(med)
            medSEL.append(medEL)


        xmlDoc = etree.ElementTree(medSEL) # novi ElementTree objekat sa zadatim korenom

        schemaDoc = etree.parse(_class.__nameSD)
        schema = etree.XMLSchema(schemaDoc)
        if not schema.validate(xmlDoc):
            print(schema.error_log)
            return

        datoteka = open(_class.__nameXML, "wb") # datoteka za čuvanje se otvara u wb (write-binary) režimu. Ukoliko ne postoji, biće kreirana
        # write metoda ElementTree objekta zapisuje XML dokument u otvorenu datoteku
        # encoding parametar govori u kom će encoding formatu biti zapisana datoteka
        # xml_declaration parametar govori da li je potrebno zapisati i XML deklaraciju u datoteku
        # pretty_print parametar govori da li je dokument potrebno čuvati tako da ga čovek može pročitati
        xmlDoc.write(datoteka, encoding = "UTF-8", xml_declaration = True, pretty_print = True)
        datoteka.close()

    @classmethod
    def elToClass(_class, element):
        id = element.attrib["id"] # attrib svojstvo obejkta tipa Element je rečnik koji sadrži sve atribute XML elementa
        #jmbg = element.xpath("./@jmbg")[0]
        # Element objekat je proširenje liste, pa njegovi podelementi mogu da se indeksiraju
        lbo = element[0].text # text svojstvo objekta tipa Element je string koji odgovara sadržaju XML elementa
        #ime = element.xpath("./ime")[0].text
        date = element[1].text
        type = element[2].text
        report = element[3].text
        doctor = element[4].text
        dicom = element[5].text
        med = _class(id,lbo,date,type,report,doctor,dicom)

        return med


    @classmethod
    def readXML(_class):
        try:
            xmlDoc = etree.parse(_class.__nameXML) # učitavanje XML dokumenta u ELTree objekat

            schemaDoc = etree.parse(_class.__nameSD) # učitavanje XMLSchema dokumenta u ELTree objekat
            schema = etree.XMLSchema(schemaDoc) # pretvaranje ELTree objekta u XMLSchema objekat
            if not schema.validate(xmlDoc): # validacija xml dokumenta naspram šeme
                print(schema.error_log) # prikaz svih grešaka nastalih pri poslednjoj validaciji
                return {}

            medsEL = xmlDoc.getroot() # pristup korenskom elementu ElementTree objekta


            meds= []
            for med in medsEL: # Element je proširenje liste, pa može da se iterira kroz njegove podelemente
                med = _class.elToClass(med)
                meds.append(med)

            return meds
        except OSError:
            return {}

    def element_class(element):
        tmp = MedicalExamination(element.id,element.patient_LBO,element.date,element.type,element.report,element.doctor,element.dicom)
        return (tmp)


    def xmlToList():
        meds = MedicalExamination.readXML()
        listOfMeds = {}
        for med in meds:
            tmp = MedicalExamination.element_class(med)
            listOfMeds[int(tmp.id)] = tmp

        return listOfMeds


    def addNewMed(med):
        meds =MedicalExamination.xmlToList()
        meds[med.id] = med
        for p in meds:
            print(p)
            print()
        MedicalExamination.saveXML(meds)
        return ("suc")
