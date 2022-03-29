# %%
from bs4 import BeautifulSoup
from time import sleep
import re
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains





# %%

def search_image_by_google(driver,url:str="https://www.talkwalker.com/uploads/2017/00001/mc1/Not%20Hotdog.png",keyword:list=list()) -> list:
    print("search called")
    # searching on google
    
    sleep(1)
    driver.find_element_by_css_selector("[aria-label='Search by image']").click()
    input_tag = driver.find_element_by_css_selector("[name='image_url']")
    input_tag.clear()
    sleep(3)
    input_tag.send_keys(url,Keys.RETURN)

    # searching on google end return page source code --> data
    data = driver.page_source

    soup = BeautifulSoup(data,'html.parser')

    
        # get wiki result
    try:
        wiki_result = soup.select_one('.kno-ecr-pt span').getText()
        print("wiki result\n",[re.sub(r"\xa0",'',x) for x in wiki_result],'\n')
        return [re.sub(r"\xa0",'',x) for x in wiki_result]
    except:
        pass

    # get search result
    try:
        result = re.findall(r'Possible related search:(.+)',str(soup.select_one('#topstuff').getText()),re.I)
        print("result",[re.sub(r"\xa0",'',x) for x in result])
        return [re.sub(r"\xa0",'',x) for x in result]
    except:
        pass


    

    return ''


def search_image_by_bing(driver,url:str="https://www.talkwalker.com/uploads/2017/00001/mc1/Not%20Hotdog.png",keyword:list=list()):
    
    print("search with bing called")
    # Test name: bing search
    # Step # | name | target | value
    # 1 | open | https://www.bing.com/?FORM=Z9FD1 | 
    driver.get("https://www.bing.com/?FORM=Z9FD1")
    # 2 | setWindowSize | 1382x744 | 
    driver.set_window_size(1382, 744)
    # 3 | click | id=sbi_b | 
    driver.find_element(By.ID, "sbi_b").click()
    # 4 | mouseDown | css=#sb_pastepn > span | 
    element = driver.find_element(By.CSS_SELECTOR, "#sb_pastepn > span")
    actions = ActionChains(driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 5 | mouseUp | id=sb_imgpst | 
    element = driver.find_element(By.ID, "sb_imgpst")
    actions = ActionChains(driver)
    actions.move_to_element(element).release().perform()
    # 6 | click | id=sb_pastearea | 
    driver.find_element(By.ID, "sb_pastearea").click()
    # 7 | type | id=sb_imgpst | https://google.com
    driver.find_element(By.ID, "sb_imgpst").send_keys(url)
    # 8 | sendKeys | id=sb_imgpst | ${KEY_ENTER}
    driver.find_element(By.ID, "sb_imgpst").send_keys(Keys.ENTER)

    driver.maximize_window()
    [x.text.replace("\n",'') for x in driver.find_elements_by_css_selector(".pritext")]


    try:
        return [x.text.replace("\n",'') for x in driver.find_elements_by_css_selector(".pritext")]
    except:
        pass
    return ''









# %%
if __name__ == "__main__":
    chrome_options = Options()
    absolute_path = os.path.dirname(os.path.realpath(__file__))
    chromedriver_path = os.path.join(absolute_path, '../chromedriver')
    # chrome_options.add_argument("--start-maximized")  # To open chrome in full screen
    driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver_path)
    driver.set_page_load_timeout(80)
    google_image = 'https://www.google.com/imghp?hl=en&tab=ri&ogbl'
    driver.get(google_image)
    search_image_by_google(driver)
    driver.close()
    
# %%