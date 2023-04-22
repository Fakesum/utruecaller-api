__version__ = "0.0.1a"
__name__ = 'utruecaller_api'

# WARNING: DONT CHANGE ANYTHING ABOVE

from seleniumbase import SB, BaseCase
from selenium.webdriver.common.keys import Keys
import time
import threading
import requests
from truecallerpy.app import search_phonenumber

def _list(f):
    def wrapper(*args, **kwargs) -> list:
        return list(f(*args, **kwargs))
    return wrapper

def _relog(driver):
    driver.execute_script("""localStorage["tc:user"] = '{"token": null}'""")
    driver.get("https://accounts.google.com/o/oauth2/v2/auth?response_type=code&respone_mode=query&redirect_uri=https%3A%2F%2Fasia-south1-truecaller-web.cloudfunctions.net%2Fapi%2Fnoneu%2Fauth%2Fgoogle%2Fv1&state=asia-south1%7Cin%7Ctrue%7Cweb%7Chttps%3A%2F%2Fwww.truecaller.com&client_id=22378802832-klpcj5dosalhnu0vshg3hjm9qgidmp8j.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.readonly")

def wait_for_truecaller_page(driver: BaseCase):
    while driver.get_current_url() != "https://www.truecaller.com/":
        print(driver.get_current_url())
        time.sleep(0.1)

def deactivate(key):
    while True:
        try:
            requests.post("https://asia-south1-truecaller-web.cloudfunctions.net/api/noneu/deactivate/v1",
                headers={
                    "authorization": "Bearer "+ key,
                    "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"Linux\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "cross-site"
            })
            break
        except:
            pass

def renew(driver):
    wait_for_truecaller_page(driver)

    google_access, accesstoken = driver.execute_script("""var google_access = localStorage["tc:user"];var accesstoken = atob(google_access.split(".")[1]);return [google_access, accesstoken];""")
    # relog_thread = threading.Thread(target=_relog, args=(driver,))
    # relog_thread.start()

    # deactivate_thread = threading.Thread(target=deactivate, args=(google_access,))
    # deactivate_thread.start()

    # relog_thread.join()
    # deactivate_thread.join()

    deactivate(google_access)
    _relog(driver)

    return accesstoken

@_list
def get_access_tokens(google_account_username: str, google_account_password: str, n_keys: str):
    for _ in range(n_keys):
        with SB(uc=True) as driver:
            driver.get("https://accounts.google.com/o/oauth2/v2/auth?response_type=code&respone_mode=query&redirect_uri=https%3A%2F%2Fasia-south1-truecaller-web.cloudfunctions.net%2Fapi%2Fnoneu%2Fauth%2Fgoogle%2Fv1&state=asia-south1%7Cin%7Ctrue%7Cweb%7Chttps%3A%2F%2Fwww.truecaller.com&client_id=22378802832-klpcj5dosalhnu0vshg3hjm9qgidmp8j.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts.readonly")

            driver.type("#identifierId", google_account_username + Keys.ENTER)
            driver.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", google_account_password+Keys.ENTER)

            while True:
                yield renew(driver)