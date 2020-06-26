# Go to autocomplete-plus package and disable 'Automatically confirm single selection' option to avoid argument print([arg],[arg]) automatic completion
#First install openpyxl with pip or anaconda
#sheet.columns/rows is a generator that uses next(rows/columns)[i].value to access data | in previous versions of python it's an array
#Alternatively, you can use list(generator)[0] in order to access rows or columns as an array which is actually not an array but a list
import openpyxl as xl
#install selenium and download webdriver exe and put it in same directory as py file
#common uses are find_element_by_id, send_keys, click()
#remember xpath location is as follows
# browser.find_element_by_xpath("//button[@value='go']") |  browser.find_element_by_xpath("//a[@href]")
#browser.switch_to.window(browser.window_handles[j])
from selenium import webdriver
#used to easily handle Select elements
from selenium.webdriver.support.ui import Select
#used to stop program for set amount of time with time.sleep()
import time
#used to send action keys to webdriver/browser via ActionChains
from selenium.webdriver.common.keys import Keys
#ActionChains(browser).key_down(Keys.CONTROL).click(button).key_up(Keys.CONTROL).perform()
from selenium.webdriver.common.action_chains import ActionChains
#this is for headless browswer, I believe it only works with Chrome and Firefox
#these are the two options that work, the first one is newer
    # options.headless=True
    # options.add_argument('--headless')
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
import os

def craigslist():
    again = None
    print('Libraries loaded...')
    #gets file from directory or current working directory which is where the .py file is located

    file = xl.load_workbook('Ads.xlsx')
    print('Worksheet loaded...')

    #gets sheets from file, returns an 1D array
    sheets = file.worksheets
    sheet = sheets[0]
    #gets columns and rows
    columns = sheet.columns
    rows = sheet.rows

    #used to get headless mode
    options = Options()
    ########################################################################
    options.headless=True
    # options.add_argument('--headless')
    # #gets browser webdriver and adds any options set before like headless mode,etc
    # browser = webdriver.Firefox()
    browser = webdriver.Chrome('/usr/bin/chromedriver',options=options)
    print('webdriver started')
    #goes to page
    browser.get('https://accounts.craigslist.org/login/home?lang=en&cc=us')
    #gets webpage elements
    emailInput = browser.find_element_by_id('inputEmailHandle')
    passwordInput = browser.find_element_by_id('inputPassword')
    loginButton = browser.find_element_by_id('login')
    #clicks button and send_keys to elements

    emailInput.send_keys('qualityinteractmexico@gmail.com')
    passwordInput.send_keys('Verde2019.')
    loginButton.click()

    print('Login successful')
    area=['mexico city, MX', 'guadalajara, MX', 'monterrey, MX']
    area=area[2]
    #After going to new page after click
    #get select element
    addSelect = Select(browser.find_element_by_name('areaabb'))
    #use select_by_visible_text to select relevant option from Select
    addSelect.select_by_visible_text(area)
    print('selected {}'.format(area))
    #finds button to be used for opening multiple pages in next loop
    button = browser.find_element_by_xpath("//button[@value='go']")
    #Loops for number of extra ads to post
    for i in range(0,4):
        #Ctrl+click
        ActionChains(browser).key_down(Keys.CONTROL).click(button).key_up(Keys.CONTROL).perform()
        print('Opening New Page: '+str(i+1)+', Success')
    #Loop for doing actions in each page
    for j in range(0,i+2):
        #go to specified window
        browser.switch_to.window(browser.window_handles[j])
        print('Working on Page '+str(j))
        #if for re stating button variable since previous elements were lost with Ctrl+click and needs to be
        #clicked after all Ctrl+clicks are done
        if j ==0:
            button = browser.find_element_by_xpath("//button[@value='go']")
            button.click()
        #radio option clicking
        radio = browser.find_element_by_xpath("//input[@value='jo']")
        radio.click()
        # browser.find_element_by_xpath("//button[@value='Continue']").click()
        radio = browser.find_element_by_xpath("//input[@value='57']")
        radio.click()


        currentURL = browser.current_url
        if 'edit' not in currentURL:
            browser.find_element_by_xpath("//a[@href]").click()
            print('Redirect page found on Page '+str(j))



        print('Add Posting Started:')

        #stores next row in variable from rows generator
        craigslistRow = next(rows)


        browser.find_element_by_name('PostingTitle').send_keys(craigslistRow[0].value)
        browser.find_element_by_name('geographic_area').send_keys(craigslistRow[1].value)
        browser.find_element_by_name('PostingBody').send_keys(craigslistRow[2].value)
        #click on span first and then search for element in span to select by clicking it
        browser.find_element_by_class_name('ui-selectmenu-text').click()
        browser.find_element_by_id('ui-id-6').click()
        browser.find_element_by_name('remuneration').send_keys(craigslistRow[3].value)
        browser.find_element_by_name('go').click()
        print(craigslistRow[0].value)

        #used relative xpah to find elements without name or id in case site is in Spanish
        try:
            browser.find_element_by_xpath("//button[@value='Done with Images']").click()
        except:
            print("Page is probably in spanish")
        finally:
            #in case page is in spanish it'll use xpath instead of 'done with Images'
            browser.find_element_by_xpath("//button[@name='go']").click()
        #used to determine if add was actually successful or if posting is to near
        try:
            print(browser.find_element_by_class_name('picker').text)
            print('---------------<|| POST FAILED||>---------------')
            os.system('echo FAILED>>runLog.txt')
            return
            print('Continuing tho...')
        except:
            print('---------------<|| POST SUCCESSFUL||>---------------')
    browser.quit();
    print('Fixing new ad order')

    sheet.move_range("A1:D5", rows=sheet.max_row, cols=0)
    sheet.delete_rows(1,5)
    print('move successful')

    print('Saving File')
    file.save('Ads.xlsx')
    print('Save successful')

    print('---------------<|| SCRIPT SUCCESSFUL||>---------------')
    os.system('echo SUCCESS>>runLog.txt')
craigslist()
