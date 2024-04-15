import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()
options.headless = False  # Set headless to False to run in non-headless mode

driver = uc.Chrome(use_subprocess=True, options=options)
driver.get("https://ege.sdamgia.ru")
driver.maximize_window()

time.sleep(20)
driver.close()
