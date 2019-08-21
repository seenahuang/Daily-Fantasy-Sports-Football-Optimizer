from selenium import webdriver


driver = webdriver.Chrome()

driver.get("https://www.draftkings.com/draft/contest/74675294")
driver.find_element(By.XPATH, "/html/body").click()