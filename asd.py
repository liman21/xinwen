from selenium import webdriver
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option('w3c', False)
chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
# chromeOptions.add_argument('--headless')  # 隐藏浏览器
driver = webdriver.Chrome(options=chromeOptions
                          ,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
                          )
driver.get(url='https://blog.csdn.net/sinat_21591675/article/details/82770360')
print(1)