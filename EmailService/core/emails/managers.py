import settings
from .email_client import EmailClient


class EmailManager:
    
    def __init__(self):
        self.client = EmailClient()
    
    async def send_blog_user_greetings_email(self, username: str, email: str):
        sender_email = settings.NO_REPLY_EMAIL
        template = settings.MAIN_EMAIL_TEMPLATE
        subject = "Witaj w serwisie MicroSociety"
        part1 = '''Chcielibyśmy powitać Cię w gronie naszej małej społeczności.
            Mamy nadzieję, że będziesz się z nami świetnie bawić i poznasz wiele ciekawych osób.'''
        part3 = '''Przywitaj się ze wszystkimi na tagu #hello i opowiedz o sobie!'''
        
    
        self.client.send_email(
            sender_email, email, subject, username, template, part1=part1, part3=part3)
        
    async def send_blog_user_farewell_email(self, username: str, email: str):
        sender_email = settings.NO_REPLY_EMAIL
        template = settings.MAIN_EMAIL_TEMPLATE
        subject = "Microsociety - pożegnanie"
        part1 = '''Przykro nam, że odchodzisz z serwisu. Staramy się dbać o zachowanie najlepszych
            standardów w społeczności - jeśli chciałbyś, żebyśmy coś zmienili, napisz do nas na opinie@microsociety.pl.'''
        part3 = '''Mamy nadzieję, że kiedyś do nas wrócisz!'''
        
        self.client.send_email(
            sender_email, email, subject, username, template, part1=part1, part3=part3)
        
    async def send_moderator_greetings_email(self, firstname: str, password: str, email: str):
        sender_email = settings.NO_REPLY_EMAIL
        template = settings.MAIN_EMAIL_TEMPLATE
        subject = "Microsociety - dostęp do konta pracownika"
        part1 = '''Administrator Microsociety stworzył dla Ciebie konto z uprawnieniami moderatora. 
                Twój profil w serwisie jest publiczny, więc pamiętaj, żeby go dostosować. 
                Dane dostępowe:'''
        part2 = f'Email: {email}'
        part3 = f'Hasło: {password}'
        
        self.client.send_email(
            sender_email, email, subject, firstname, template, part1=part1, part2=part2, part3=part3)
        
    async def send_admin_greetings_email(self, firstname: str, password: str, email: str):
        sender_email = settings.NO_REPLY_EMAIL
        template = settings.MAIN_EMAIL_TEMPLATE
        subject = "Microsociety - dostęp do konta pracownika"
        part1 = '''Administrator Microsociety stworzył dla Ciebie konto z uprawnieniami administratora. 
                Masz dostęp jedynie do części pracowniczej serwisu. 
                Dane dostępowe:'''
        part2 = f'Email: {email}'
        part3 = f'Hasło: {password}'
        
        self.client.send_email(
            sender_email, email, subject, firstname, template, part1=part1, part2=part2, part3=part3)
        
    async def send_password_reset_email(self, username: str, email: str, code: str):
        sender_email = settings.NO_REPLY_EMAIL
        template = settings.MAIN_EMAIL_TEMPLATE
        subject = "Microsociety - reset hasła"
        part1 = '''Poniższy link pozwoli Ci na zresetowanie hasła w naszym serwisie:'''
        part2 = f'{settings.DOMAIN}/{settings.PASS_RESET_ENDPOINT}/{code}'
        part3 = '''Jeśli nie prosiłeś o zresetowanie hasła, zignoruj ten email!'''
        
    
        self.client.send_email(
            sender_email, email, subject, username, template, part1=part1, part2=part2, part3=part3)