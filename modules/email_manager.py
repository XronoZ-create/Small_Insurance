import imaplib
import mailparser
import email
import base64

class EmailManager:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        if "gmail.com" in login:
            self.imap = "imap.gmail.com"
        else:
            self.imap = "imap.yandex.ru"

    def get_last_mail_osk_code(self):
        self.mail = imaplib.IMAP4_SSL(self.imap)
        self.mail.login(self.login, self.password)
        self.mail.select('INBOX')
        try:
            self._, self.pisma = self.mail.search(None, f'HEADER FROM "osk-ins.ru" TO "{self.login}"')
            self.id_pismo = self.pisma[0].split()[-1]
        except IndexError:
            raise NotFindMail
        # print(self.id_pismo)
        self._, self.byte_pismo = self.mail.fetch(self.id_pismo, "(RFC822)")
        self.text_pismo = mailparser.parse_from_bytes(self.byte_pismo[0][1]).text_plain[0]

        # print(self.text_pismo)
        self.code = self.text_pismo.split("&code=")[1].split("&")[0]
        return self.code

    def get_last_mail_rca_url_confirm(self):
        self.mail = imaplib.IMAP4_SSL(self.imap)
        self.mail.login(self.login, self.password)
        self.mail.select('INBOX')
        try:
            self._, self.pisma = self.mail.search(None, f'HEADER FROM "autoins.ru" TO "{self.login}"')
            self.id_pismo = self.pisma[0].split()[-1]
        except IndexError:
            raise NotFindMail
        # print(self.id_pismo)
        self._, self.byte_pismo = self.mail.fetch(self.id_pismo, "(RFC822)")
        self.text_pismo = mailparser.parse_from_bytes(self.byte_pismo[0][1]).body

        # print(self.text_pismo)
        self.url_confirm = self.text_pismo.split("перейдите на страницу авторизации: ")[1].split("<br>")[0]
        # print(self.url_confirm)
        return self.url_confirm

    def get_last_mail_ugsk_verif(self):
        self.mail = imaplib.IMAP4_SSL(self.imap)
        self.mail.login(self.login, self.password)
        self.mail.select('INBOX')
        try:
            self._, self.pisma = self.mail.search(None, f'HEADER FROM "info@ugsk.ru" TO "{self.login}"')
            self.id_pismo = self.pisma[0].split()[-1]
        except IndexError:
            raise NotFindMail
        # print(self.id_pismo)
        self._, self.byte_pismo = self.mail.fetch(self.id_pismo, "(RFC822)")
        self.text_pismo = mailparser.parse_from_bytes(self.byte_pismo[0][1]).text_plain[0]

        # print(self.text_pismo)
        self.url = self.text_pismo.split("по ссылке ")[1].split(" и")[0]
        return self.url

    def get_last_mail_21_code(self):
        self.mail = imaplib.IMAP4_SSL(self.imap)
        self.mail.login(self.login, self.password)
        self.mail.select('INBOX')
        try:
            self._, self.pisma = self.mail.search(None, f'HEADER FROM "21-vek.spb.ru" TO "{self.login}"')
            self.id_pismo = self.pisma[0].split()[-1]
        except IndexError:
            raise NotFindMail
        # print(self.id_pismo)
        self._, self.byte_pismo = self.mail.fetch(self.id_pismo, "(RFC822)")
        self.text_pismo = mailparser.parse_from_bytes(self.byte_pismo[0][1]).text_plain[0]

        # print(self.text_pismo)
        self.code = self.text_pismo.split("&code=")[1].split("&")[0]
        return self.code

    def get_last_mail_arm_code(self):
        self.mail = imaplib.IMAP4_SSL(self.imap)
        self.mail.login(self.login, self.password)
        self.mail.select('INBOX')
        try:
            self._, self.pisma = self.mail.search(None, f'HEADER FROM "armeec.ru" TO "{self.login}"')
            self.id_pismo = self.pisma[0].split()[-1]
        except IndexError:
            raise NotFindMail
        # print(self.id_pismo)
        self._, self.byte_pismo = self.mail.fetch(self.id_pismo, "(RFC822)")
        self.text_pismo = mailparser.parse_from_bytes(self.byte_pismo[0][1]).text_plain[0]

        # print(self.text_pismo)
        self.code = self.text_pismo.split("&code=")[1].split("&")[0]
        return self.code

    def get_last_mail_vsk_code(self):
        self.mail = imaplib.IMAP4_SSL(self.imap)
        self.mail.login(self.login, self.password)
        self.mail.select('INBOX')
        try:
            self._, self.pisma = self.mail.search(None, f'HEADER FROM "vsk.ru" TO "{self.login}"')
            self.id_pismo = self.pisma[0].split()[-1]
        except IndexError:
            raise NotFindMail
        # print(self.id_pismo)
        self._, self.byte_pismo = self.mail.fetch(self.id_pismo, '(RFC822)')
        self.base64_body = email.message_from_bytes(self.byte_pismo[0][1]).get_payload()[0].get_payload()
        self.string_body = base64.b64decode(self.base64_body).decode('utf-8')
        print(self.string_body)

        self.code = self.string_body.split("Введите код ")[1].split(" ")[0]
        return self.code

class NotFindMail(Exception):
    pass
