import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import numpy
from contextlib import suppress
import time
import random

class ColumnNames:
    column_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ']

class ColumnGoogleTable:
    server_address = "A"
    start_bot = "B"
    status_bot = "C"

    url_rca = "D"
    login_rca = "E"
    password_rca = "F"

    login_osk = "G"
    password_osk = "H"

    email_login = "I"
    email_password = "J"

    surname = "K"
    name = "L"
    otchestvo = "M"
    birthday = "N"
    pass_seriya = "O"
    pass_number = "P"
    pass_vidach = "Q"
    pass_address = "R"

    sobstv_yavl_strah = "S"
    sobstv_surname = "T"
    sobstv_name = "U"
    sobstv_otchestvo = "V"
    sobstv_birthday = "W"
    sobstv_pass_seriya = "X"
    sobstv_pass_number = "Y"
    sobstv_pass_vidach = "Z"
    sobstv_pass_address = "AA"

    target = "AB"
    mark = "AC"
    model = "AD"
    other_mark = "AE"
    year = "AF"
    powers = "AG"
    type_engine = "AH"
    type_cusov = "AI"
    transmission = "AJ"
    modification = "AK"

    max_mass = "AL"
    pricep = "AM"

    count_pass_mest = "AN"

    type_document_ptc = "AO"
    type_document_ctc = "AP"
    type_document_eptc = "AQ"

    ctc_ptc_seriya = "AR"
    ctc_ptc_number = "AS"
    ctc_ptc_vidach = "AT"
    ctc_ptc_reg_znak = "AU"
    ctc_ptc_vin = "AV"
    ctc_ptc_nomer_shassi = "AW"
    ctc_ptc_nomer_cusov = "AX"

    nomer_dk = "AY"
    data_TO = "AZ"
    zapr_photo = "BA"

    c_ogr_or_not = "BB"

    one_vod_surname = "BC"
    one_vod_name = "BD"
    one_vod_otchestvo = "BE"
    one_vod_birthday = "BF"
    one_vod_seria_vu = "BG"
    one_vod_nomer_vu = "BH"
    one_vod_data_vidachi_vu = "BI"
    one_vod_nachalo_staga = "BJ"

    two_vod_surname = "BK"
    two_vod_name = "BL"
    two_vod_otchestvo = "BM"
    two_vod_birthday = "BN"
    two_vod_seria_vu = "BO"
    two_vod_nomer_vu = "BP"
    two_vod_data_vidachi_vu = "BQ"
    two_vod_nachalo_staga = "BR"

    three_vod_surname = "BS"
    three_vod_name = "BT"
    three_vod_otchestvo = "BU"
    three_vod_birthday = "BV"
    three_vod_seria_vu = "BW"
    three_vod_nomer_vu = "BX"
    three_vod_data_vidachi_vu = "BY"
    three_vod_nachalo_staga = "BZ"

    four_vod_surname = "CA"
    four_vod_name = "CB"
    four_vod_otchestvo = "CC"
    four_vod_birthday = "CD"
    four_vod_seria_vu = "CE"
    four_vod_nomer_vu = "CF"
    four_vod_data_vidachi_vu = "CG"
    four_vod_nachalo_staga = "CH"

    OSAGO_start = "CI"
    OSAGO_count_mouth = "CJ"

    strah_comp = "CK"

    service_sms = "CL"

class GoogleTable:
    def __init__(self):
        self.data = []
        self.CREDENTIALS_FILE = 'modules/creds.json'  # Имя файла с закрытым ключом, вы должны подставить свое
        # Читаем ключи из файла
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        self.file = gspread.authorize(self.credentials)  # authenticate with Google
        self.sheet = self.file.open("Insurance_RCA").sheet1  # open sheet

        self.numpy_massiv_data = [self.e[:] for self.e in self.sheet.get_all_values()]
        self.dataframe = pandas.DataFrame(self.numpy_massiv_data, columns=ColumnNames.column_names[:len(self.numpy_massiv_data[0])])
        self.dataframe.index = numpy.arange(1, len(self.dataframe)+1)  # меняем начало индексации с 0 на 1

        for self.num_row in range(3, len(self.dataframe)+1):
            if self.dataframe.at[self.num_row, ColumnGoogleTable.surname] != "":
                self.data.append(OneRegData(
                    sheet=self.sheet,
                    row_data=self.num_row,
                    server_address=self.dataframe.at[self.num_row, ColumnGoogleTable.server_address],
                    start_bot=self.dataframe.at[self.num_row, ColumnGoogleTable.start_bot],
                    status_bot=self.dataframe.at[self.num_row, ColumnGoogleTable.status_bot],
                    url_rca=self.dataframe.at[self.num_row, ColumnGoogleTable.url_rca],
                    login_rca=self.dataframe.at[self.num_row, ColumnGoogleTable.login_rca],
                    password_rca=self.dataframe.at[self.num_row, ColumnGoogleTable.password_rca],
                    login_osk=self.dataframe.at[self.num_row, ColumnGoogleTable.login_osk],
                    password_osk=self.dataframe.at[self.num_row, ColumnGoogleTable.password_osk],
                    email_login=self.dataframe.at[self.num_row, ColumnGoogleTable.email_login],
                    email_password=self.dataframe.at[self.num_row, ColumnGoogleTable.email_password],
                    surname=self.dataframe.at[self.num_row, ColumnGoogleTable.surname],
                    name=self.dataframe.at[self.num_row, ColumnGoogleTable.name],
                    otchestvo=self.dataframe.at[self.num_row, ColumnGoogleTable.otchestvo],
                    birthday=self.dataframe.at[self.num_row, ColumnGoogleTable.birthday],
                    pass_seriya=self.dataframe.at[self.num_row, ColumnGoogleTable.pass_seriya],
                    pass_number=self.dataframe.at[self.num_row, ColumnGoogleTable.pass_number],
                    pass_vidach=self.dataframe.at[self.num_row, ColumnGoogleTable.pass_vidach],
                    pass_address=self.dataframe.at[self.num_row, ColumnGoogleTable.pass_address],
                    sobstv_yavl_strah=self.dataframe.at[self.num_row, ColumnGoogleTable.sobstv_yavl_strah],
                    sobstv_surname=self.dataframe.at[self.num_row, ColumnGoogleTable.sobstv_surname],
                    sobstv_name=self.dataframe.at[self.num_row, ColumnGoogleTable.sobstv_name],
                    sobstv_otchestvo=self.dataframe.at[self.num_row, ColumnGoogleTable.sobstv_otchestvo],
                    sobstv_birthday=self.dataframe.at[self.num_row, ColumnGoogleTable.sobstv_birthday],
                    sobstv_pass_seriya=self.dataframe.at[self.num_row, ColumnGoogleTable.sobstv_pass_seriya],
                    sobstv_pass_number=self.dataframe.at[self.num_row, ColumnGoogleTable.sobstv_pass_number],
                    sobstv_pass_vidach=self.dataframe.at[self.num_row, ColumnGoogleTable.sobstv_pass_vidach],
                    sobstv_pass_address=self.dataframe.at[self.num_row, ColumnGoogleTable.sobstv_pass_address],
                    target=self.dataframe.at[self.num_row, ColumnGoogleTable.target],
                    mark=self.dataframe.at[self.num_row, ColumnGoogleTable.mark],
                    model=self.dataframe.at[self.num_row, ColumnGoogleTable.model],
                    other_mark=self.dataframe.at[self.num_row, ColumnGoogleTable.other_mark],
                    year=self.dataframe.at[self.num_row, ColumnGoogleTable.year],
                    powers=self.dataframe.at[self.num_row, ColumnGoogleTable.powers],
                    type_engine=self.dataframe.at[self.num_row, ColumnGoogleTable.type_engine],
                    type_cusov=self.dataframe.at[self.num_row, ColumnGoogleTable.type_cusov],
                    transmission=self.dataframe.at[self.num_row, ColumnGoogleTable.transmission],
                    modification=self.dataframe.at[self.num_row, ColumnGoogleTable.modification],
                    max_mass=self.dataframe.at[self.num_row, ColumnGoogleTable.max_mass],
                    pricep=self.dataframe.at[self.num_row, ColumnGoogleTable.pricep],
                    count_pass_mest=self.dataframe.at[self.num_row, ColumnGoogleTable.count_pass_mest],
                    type_document={'ptc': self.dataframe.at[self.num_row, ColumnGoogleTable.type_document_ptc],
                                   'ctc': self.dataframe.at[self.num_row, ColumnGoogleTable.type_document_ctc],
                                   'eptc': self.dataframe.at[self.num_row, ColumnGoogleTable.type_document_eptc]},
                    ctc_ptc_seriya=self.dataframe.at[self.num_row, ColumnGoogleTable.ctc_ptc_seriya],
                    ctc_ptc_number=self.dataframe.at[self.num_row, ColumnGoogleTable.ctc_ptc_number],
                    ctc_ptc_vidach=self.dataframe.at[self.num_row, ColumnGoogleTable.ctc_ptc_vidach],
                    ctc_ptc_reg_znak=self.dataframe.at[self.num_row, ColumnGoogleTable.ctc_ptc_reg_znak],
                    ctc_ptc_vin=self.dataframe.at[self.num_row, ColumnGoogleTable.ctc_ptc_vin],
                    ctc_ptc_nomer_shassi=self.dataframe.at[self.num_row, ColumnGoogleTable.ctc_ptc_nomer_shassi],
                    ctc_ptc_nomer_cusov=self.dataframe.at[self.num_row, ColumnGoogleTable.ctc_ptc_nomer_cusov],
                    nomer_dk=self.dataframe.at[self.num_row, ColumnGoogleTable.nomer_dk],
                    data_TO=self.dataframe.at[self.num_row, ColumnGoogleTable.data_TO],
                    zapr_photo=self.dataframe.at[self.num_row, ColumnGoogleTable.zapr_photo],
                    c_ogr_or_not = self.dataframe.at[self.num_row, ColumnGoogleTable.c_ogr_or_not],
                    OSAGO_start=self.dataframe.at[self.num_row, ColumnGoogleTable.OSAGO_start],
                    OSAGO_count_mouth=self.dataframe.at[self.num_row, ColumnGoogleTable.OSAGO_count_mouth],
                    strah_comp=self.dataframe.at[self.num_row, ColumnGoogleTable.strah_comp],
                    service_sms=self.dataframe.at[2, ColumnGoogleTable.service_sms]
                ))
                if self.dataframe.at[self.num_row, ColumnGoogleTable.one_vod_surname] != "":
                    self.data[-1].add_voditel(
                        surname=self.dataframe.at[self.num_row, ColumnGoogleTable.one_vod_surname],
                        name=self.dataframe.at[self.num_row, ColumnGoogleTable.one_vod_name],
                        otchestvo=self.dataframe.at[self.num_row, ColumnGoogleTable.one_vod_otchestvo],
                        birthday=self.dataframe.at[self.num_row, ColumnGoogleTable.one_vod_birthday],
                        seriya_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.one_vod_seria_vu],
                        nomer_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.one_vod_nomer_vu],
                        data_vidachi_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.one_vod_data_vidachi_vu],
                        nachalo_staga=self.dataframe.at[self.num_row, ColumnGoogleTable.one_vod_nachalo_staga]
                    )
                if self.dataframe.at[self.num_row, ColumnGoogleTable.two_vod_surname] != "":
                    self.data[-1].add_voditel(
                        surname=self.dataframe.at[self.num_row, ColumnGoogleTable.two_vod_surname],
                        name=self.dataframe.at[self.num_row, ColumnGoogleTable.two_vod_name],
                        otchestvo=self.dataframe.at[self.num_row, ColumnGoogleTable.two_vod_otchestvo],
                        birthday=self.dataframe.at[self.num_row, ColumnGoogleTable.two_vod_birthday],
                        seriya_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.two_vod_seria_vu],
                        nomer_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.two_vod_nomer_vu],
                        data_vidachi_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.two_vod_data_vidachi_vu],
                        nachalo_staga=self.dataframe.at[self.num_row, ColumnGoogleTable.two_vod_nachalo_staga]
                    )
                if self.dataframe.at[self.num_row, ColumnGoogleTable.three_vod_surname] != "":
                    self.data[-1].add_voditel(
                        surname=self.dataframe.at[self.num_row, ColumnGoogleTable.three_vod_surname],
                        name=self.dataframe.at[self.num_row, ColumnGoogleTable.three_vod_name],
                        otchestvo=self.dataframe.at[self.num_row, ColumnGoogleTable.three_vod_otchestvo],
                        birthday=self.dataframe.at[self.num_row, ColumnGoogleTable.three_vod_birthday],
                        seriya_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.three_vod_seria_vu],
                        nomer_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.three_vod_nomer_vu],
                        data_vidachi_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.three_vod_data_vidachi_vu],
                        nachalo_staga=self.dataframe.at[self.num_row, ColumnGoogleTable.three_vod_nachalo_staga]
                    )
                if self.dataframe.at[self.num_row, ColumnGoogleTable.four_vod_surname] != "":
                    self.data[-1].add_voditel(
                        surname=self.dataframe.at[self.num_row, ColumnGoogleTable.four_vod_surname],
                        name=self.dataframe.at[self.num_row, ColumnGoogleTable.four_vod_name],
                        otchestvo=self.dataframe.at[self.num_row, ColumnGoogleTable.four_vod_otchestvo],
                        birthday=self.dataframe.at[self.num_row, ColumnGoogleTable.four_vod_birthday],
                        seriya_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.four_vod_seria_vu],
                        nomer_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.four_vod_nomer_vu],
                        data_vidachi_vu=self.dataframe.at[self.num_row, ColumnGoogleTable.four_vod_data_vidachi_vu],
                        nachalo_staga=self.dataframe.at[self.num_row, ColumnGoogleTable.four_vod_nachalo_staga]
                    )

class OneRegData:
    def __init__(self, sheet, row_data,
                 server_address, start_bot, status_bot,
                 url_rca, login_rca, password_rca,
                 login_osk, password_osk,
                 email_login, email_password,
                 surname, name, otchestvo, birthday, pass_seriya, pass_number, pass_vidach, pass_address,
                 sobstv_yavl_strah, sobstv_surname, sobstv_name, sobstv_otchestvo, sobstv_birthday, sobstv_pass_seriya, sobstv_pass_number, sobstv_pass_vidach, sobstv_pass_address,
                 target, mark, model, other_mark, year, powers, type_engine, type_cusov, transmission, modification,
                 max_mass, pricep,
                 count_pass_mest,
                 type_document,
                 ctc_ptc_seriya, ctc_ptc_number, ctc_ptc_vidach, ctc_ptc_reg_znak, ctc_ptc_vin, ctc_ptc_nomer_shassi, ctc_ptc_nomer_cusov,
                 nomer_dk, data_TO, zapr_photo,
                 c_ogr_or_not,
                 OSAGO_start, OSAGO_count_mouth,
                 strah_comp,
                 service_sms):
        self.sheet = sheet
        self.row_data = row_data

        self.server_address = server_address
        self._start_bot = start_bot
        self.status_bot = status_bot

        self.url_rca = url_rca
        self.login_rca = login_rca
        self.password_rca = password_rca

        self.login_osk = login_osk
        self.password_osk = password_osk

        self.email_login = email_login
        self.email_password = email_password

        self.surname = surname
        self.name = name
        self.otchestvo = otchestvo
        self.birthday = birthday
        self.pass_seriya = pass_seriya
        self.pass_number = pass_number
        self.pass_vidach = pass_vidach
        self.pass_address = pass_address

        if sobstv_yavl_strah == "\"+\"":
            self.sobstv_yavl_strah = sobstv_yavl_strah
        else:
            self.sobstv_yavl_strah = sobstv_yavl_strah
            self.sobstv_surname = sobstv_surname
            self.sobstv_name = sobstv_name
            self.sobstv_otchestvo = sobstv_otchestvo
            self.sobstv_birthday = sobstv_birthday
            self.sobstv_pass_seriya = sobstv_pass_seriya
            self.sobstv_pass_number = sobstv_pass_number
            self.sobstv_pass_vidach = sobstv_pass_vidach
            self.sobstv_pass_address = sobstv_pass_address

        self.target = target
        self.mark = mark
        self.model = model
        self.other_mark = other_mark
        self.year = year
        self.powers = powers
        self.type_engine = type_engine
        self.type_cusov = type_cusov
        self.transmission = transmission
        self.modification = modification

        self.max_mass = max_mass
        self.pricep = pricep

        self.count_pass_mest = count_pass_mest

        self.type_document = type_document

        self.ctc_ptc_seriya = ctc_ptc_seriya
        self.ctc_ptc_number = ctc_ptc_number
        self.ctc_ptc_vidach = ctc_ptc_vidach
        self.ctc_ptc_reg_znak =ctc_ptc_reg_znak
        self.ctc_ptc_vin = ctc_ptc_vin
        self.ctc_ptc_nomer_shassi = ctc_ptc_nomer_shassi
        self.ctc_ptc_nomer_cusov = ctc_ptc_nomer_cusov

        self.nomer_dk = nomer_dk
        self.data_TO = data_TO
        self.zapr_photo = zapr_photo

        self.c_ogr_or_not = c_ogr_or_not

        self.voditeli = []

        self.OSAGO_start = OSAGO_start
        self.OSAGO_count_mouth = OSAGO_count_mouth

        self.strah_comp = strah_comp.replace(", ", ",").replace(" , ", ",").replace(" ,", ",").split(",")
        self.service_sms = service_sms

    def add_voditel(self, surname, name, otchestvo, birthday, seriya_vu, nomer_vu, data_vidachi_vu, nachalo_staga):
        self.voditeli.append(
            Voditel(
                surname=surname,
                name=name,
                otchestvo=otchestvo,
                birthday=birthday,
                seriya_vu=seriya_vu,
                nomer_vu=nomer_vu,
                data_vidachi_vu=data_vidachi_vu,
                nachalo_staga=nachalo_staga
            )
        )

    def set_value(self, name, value):
        self.sheet.update("{0}{1}".format(ColumnGoogleTable.__dict__[name], self.row_data), value)

    @property
    def start_bot(self):
        for self._ in range(0, 3):
            try:
                self.st_gs = self.sheet.acell("{0}{1}".format(ColumnGoogleTable.__dict__["start_bot"], self.row_data)).value
                if self.st_gs is None:
                    return ''
                else:
                    return self.st_gs
            except:
                time.sleep((random.randrange(1, 10))/10)
        raise Exception


class Voditel():
    def __init__(self, surname, name, otchestvo, birthday, seriya_vu, nomer_vu, data_vidachi_vu, nachalo_staga):
        self.surname = surname
        self.name = name
        self.otchestvo = otchestvo
        self.birthday = birthday
        self.seriya_vu = seriya_vu
        self.nomer_vu = nomer_vu
        self.data_vidachi_vu = data_vidachi_vu
        self.nachalo_staga = nachalo_staga
    def __repr__(self):
        return "Имя: %s, Фамилия: %s, Отчество: %s, Дата рождения: %s, Серия ВУ: %s, Номер ВУ: %s, Дата выдачи ВУ: %s, Начало стажа: %s" % (
            self.surname, self.name,
            self.otchestvo,
            self.birthday,
            self.seriya_vu,
            self.nomer_vu,
            self.data_vidachi_vu,
            self.nachalo_staga
        )

# data = GoogleTable().data
# print(data[2].voditeli)