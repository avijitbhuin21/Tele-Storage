import requests
from bs4 import BeautifulSoup

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

DEBUG = True

def log_debug(entity:any) -> None:
    if DEBUG == True:
        print(f"DEBUG: {entity}")


class Helper:
    def __init__(self):
        pass

class Telegram_Credentials:
    def __init__(self) -> None:
        self.session=requests.session()
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://my.telegram.org',
            'priority': 'u=1, i',
            'referer': 'https://my.telegram.org/auth',
            'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }

    
    def get_My_Telegram_org_login_otp(self,number):
        self.phone_number = number
        url = 'https://my.telegram.org/auth/send_password'
        payload = {
            "phone": number
        }
        res = self.session.post(url=url, headers=self.headers, data=payload)
        try:
            self.login_otp_random_hash = res.json()['random_hash']
            return self.login_otp_random_hash
        except Exception as e:
            log_debug(e)
            log_debug(res.text)

    def confirm_My_Telegram_org_otp(self, otp):
        url = 'https://my.telegram.org/auth/login'

        data = {
            'phone': self.phone_number,
            'random_hash': self.login_otp_random_hash,
            'password': otp,
            'remember': '1',
        }

        res = self.session.post('https://my.telegram.org/auth/login', headers = self.headers, data = data)

        if 'Invalid confirmation code!' not in res.text:
            return True
        else:
            return False

    def get_id_hash(self):
        res = self.session.get('https://my.telegram.org/apps')
        soup = BeautifulSoup(res.text, "html.parser")

        id = [i.text for i in soup.find_all("strong") if (i.text.isdigit() and len(i.text) == 8)]
        hash = [i.text for i in soup.find_all('span') if (len(i.text) == 32 and " " not in i.text)]

        if id != [] and hash != []:
            return {"id": id[0], "hash": hash[0]}
        else:
            return False


    def create_app(self):
        res = self.session.get('https://my.telegram.org/apps')
        soup = BeautifulSoup(res.text,'html.parser')
        hash = soup.find('input', {'name': 'hash'})['value']
        log_debug(f"HASH FOR CREATING APP: {hash}")

        url = 'https://my.telegram.org/apps/create'
        payload = {
            'hash': hash,
            'app_title': 'TeleStorage',
            'app_shortname': 'TeleStorage',
            'app_url': 'www.telegram.org',
            'app_platform': 'android',
            'app_desc': ''
        }
        res=self.session.post(url=url, headers=self.headers, data=payload)
        log_debug(res.text)

        return True if res.status_code == 200 else False

    def handle_extraction(self):
        data = self.get_id_hash()
        if data != False:
            return data
        else:
            log_debug(f"App Not Found, Creating one")
            if self.create_app() == True:
                return self.get_id_hash()
            else:
                log_debug("Error While Creating the app. Please Go to https://my.telegram.org/apps and create the app manually.") 


class Telegram_Session_Handler:

    def __init__(self):
        pass

    def create_session_client(self, API_ID, API_HASH, SESSION_STRING = None):
        self.client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

        return self.client

    

