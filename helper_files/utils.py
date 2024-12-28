import requests
from bs4 import BeautifulSoup



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
        url = 'https://my.telegram.org/auth/send_password'
        payload = {
            "phone": number
        }
        res = self.session.post(url=url, headers=self.headers, data=payload)
        try:
            return res.json()['random_hash']
        except Exception as e:
            log_debug(e)
            log_debug(res.text)

    def confirm_My_Telegram_org_otp(self, otp, random_hash, phone):
        url = 'https://my.telegram.org/auth/login'

        data = {
            'phone': phone,
            'random_hash': random_hash,
            'password': otp,
            'remember': '1',
        }

        res = self.session.post('https://my.telegram.org/auth/login', headers = self.headers, data = data)

        if 'Invalid confirmation code!' not in res.text:
            return True
        else:
            return False

    def get_id_hash(self):
        res=self.session.get('https://my.telegram.org/apps')
        soup = BeautifulSoup(res.text, "html.parser")

        id = [i.text for i in soup.find_all("strong") if (i.text.isdigit() and len(i.text) == 8)][0]
        hash = [i.text for i in soup.find_all('span') if (len(i.text) == 32 and " " not in i.text)][0]

        return {"id": id, "hash": hash}


    # def create_app(self):
    #     res=self.session.get('https://my.telegram.org/apps')
    #     soup=BeautifulSoup(res.text,'html.parser')
    #     hash = soup.find('input', {'name': 'hash'})['value']

    #     url='https://my.telegram.org/apps/create'
    #     payload = {
    #         'hash': hash,
    #         'app_title': 'Telegram_Unlimited_storage',
    #         'app_shortname': 'TeleDrive',
    #         'app_url': 'www.telegram.org',
    #         'app_platform': 'android',
    #         'app_desc': ''
    #     }
    #     res=self.session.post(url=url, headers=self.headers, data=payload)
    #     print(res.text)
    #     return self.get_id_hash()

    
        



    # def telegram_login(self, phone, random_hash, otp):
    #     url = 'https://my.telegram.org/auth/login'

    #     data = {
    #         'phone': phone,
    #         'random_hash': random_hash,
    #         'password': otp,
    #         'remember': '1',
    #     }
    #     res = self.session.post('https://my.telegram.org/auth/login', headers = self.headers, data = data)

    #     no=number.replace('+','')
    #     if 'Invalid confirmation code!' not in res.text:
    #         try:
    #             id,hash= self.get_id_hash()
    #             data={"id":id, "hash":hash, "number":number}
    #             with open(f"{no}.json", "w") as json_file:
    #                 json.dump(data, json_file)
    #             return {"id":id, "hash":hash, "number":number, "message":"Success"}
                
    #         except:
    #             id,hash=self.create_app()
    #             data={"id":id, "hash":hash, "number":number}
    #             with open(f"{no}.json", "w") as json_file:
    #                 json.dump(data, json_file)
    #             return {"id":id, "hash":hash, "number":number, "message":"Success"}

    #     else:
    #         return {"message":'Invalid confirmation code!'}