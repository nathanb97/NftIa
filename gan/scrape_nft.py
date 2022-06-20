import undetected_chromedriver.v2 as uc

from lxml import html

import time


from selenium import webdriver
import time
from tqdm import tqdm
from pathlib import Path



class Scraper():
    
    def __init__(self):
        uc_options = uc.ChromeOptions()
        uc_options.add_argument("--headless")
        self.driver = uc.Chrome(options=uc_options, driver_executable_path="/usr/bin/chromedriver")
        uc_options = uc.ChromeOptions()
        uc_options.add_argument("--headless")

        self.driver_to_download = uc.Chrome(options=uc_options, driver_executable_path="/usr/bin/chromedriver")
        self.connect_google_image()

    def accept_cookies(self, path):
        try:
            f = self.driver.find_element_by_xpath(path)
            f.click()
            time.sleep(5)
        except:
            pass


    def connect_google_image(self):
        self.driver.get("https://images.google.fr/")
        time.sleep(2)
        try:
            f = self.driver.find_element_by_xpath("(//div[@class='QS5gu sy4vM'])[2]")
            f.click()
            time.sleep(5)
        except:
            print("ça a pas cliqué")
    def search(self, name):
        self.connect_google_image()
        keyboard = self.driver.find_element_by_xpath("//input[@class='gLFyf gsfi']")
        keyboard.send_keys(name)
        time.sleep(1)
        keyboard.send_keys(u'\ue007')
        time.sleep(1)
        return self.driver.current_url
    
    def searchs_from_list(self, names:list):
        for name in (names):
            yield self.search(name)

    @classmethod
    def scroll(
        cls,
        driver,
        xpath: str,
        click: bool = False,
        time_after_scroll_click: float = 0,
        time_before_click: float = 0,
    ):
        element = driver.find_element_by_xpath(xpath)
        element.location_once_scrolled_into_view
        if click:
            time.sleep(time_before_click)
            driver.execute_script("arguments[0].click();", element)

        time.sleep(time_after_scroll_click)
    def get_links_img(self, link_search:str, register_location:str):
        cache = set()
        self.driver.get(link_search)
        while True:
            try:
                self.accept_cookies("//button[@id='onetrust-accept-btn-handler']")
                self.accept_cookies("//button[@class=' css-1dn3rsy']")
                self.scroll(self.driver, "//footer[@class='css-1moclpj']", time_after_scroll_click=2)
                elements = self.driver.find_elements_by_xpath("//div[@class='css-2r2ti0']//img")
                links = [element.get_attribute('src') for element in elements]
                new_links = []
                for link in links:
                    if link not in cache:
                        new_links.append(link)
                        cache.add(link)
                if len(new_links) == 0:
                    break
                yield new_links
            except Exception as e:
                print("prblm", e)
            
    def scrape_link_character(self, link_search:str, register_location:str):
        for link_images in self.get_links_img(link_search, register_location):
                for link_image in link_images:
                    try:
                        self.driver_to_download.get(link_image)
                        time.sleep(1)
                        path = str(Path(register_location) / Path(str(link_image.split('/')[-1])))
                        print(path)
                        self.driver_to_download.save_screenshot(path)
                        time.sleep(1)
                        # driver.execute_script("window.history.go(-1)")
                    except Exception as e:
                        print("prblm", e)





# In[240]:




# In[241]:



# In[221]:


scraper = Scraper()


# In[222]:


# import pickle
# with open('/home/brami/Bureau/travail/git/scrape_image/journalistes_femmes.pickle', 'rb') as handle:
#     journalistes_femmes = pickle.load(handle)
# with open('/home/brami/Bureau/travail/git/scrape_image/journalistes_hommes.pickle', 'rb') as handle:
#     journalistes_hommes = pickle.load(handle)
    


# # In[223]:



# # In[242]:

# tot = journalistes_hommes + journalistes_femmes
# for name in tqdm(tot[436 + 54 + 337:]):

links = [
    # "https://www.binance.com/en/nft/collection/wonderfulday-tiger-nft-559586812315783169?orderBy=list_time&orderType=-1&isBack=1&id=559586812315783169&order=list_time%40-1&ref=HDYAHEES",
    # "https://www.binance.com/en/nft/collection/fancy-bears-metaverse-576663131907645441?orderBy=list_time&orderType=-1&isBack=1&id=576663131907645441&order=list_time%40-1",
    # "https://www.binance.com/en/nft/collection/rhnox-582397728009814017?orderBy=list_time&orderType=-1&isBack=1&id=582397728009814017&order=list_time%40-1",
    # "https://www.binance.com/en/nft/collection/nftshka-515806179919245312?orderBy=list_time&orderType=-1&isBack=1&id=515806179919245312&order=list_time%40-1",
    # "https://www.binance.com/en/nft/collection/mirror-gen2-ticket-577018345014747137?orderBy=list_time&orderType=-1&isBack=1&id=577018345014747137&order=list_time%40-1",
    "https://www.binance.com/en/nft/search-result?ref=HDYAHEES&tab=nft&keyword=monkey&order=set_end_time%401"

]
for ind, link in tqdm(enumerate(links)):
    try:
        name = str(5)
        path = Path("/home/brami/Bureau/personal_project/nft/images") / Path(name.lower().replace(" ", "_"))
        path.mkdir(parents=True, exist_ok=True)
        scraper.scrape_link_character(link, register_location=str(path))
    except:
        pass


# In[ ]:




