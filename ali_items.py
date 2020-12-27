import selenium.webdriver as webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
#from bs4 import BeautifulSoup

driver = webdriver.Chrome()

# mens clothing 
html = 'https://www.aliexpress.com/category/100003070/men-clothing.html' 
search = '?minPrice=1500&maxPrice=&page='
#results = item_counts(html, search) # 464
res = search_items(html, search)

search = '?minPrice=1000&maxPrice=1500&page='  # 622
#results = item_counts(html, search)
res2 = search_items(html, search)

search = '?minPrice=800&maxPrice=1000&page='  # 700
#results = item_counts(html, search)
res3 = search_items(html, search)

search = '?minPrice=800&maxPrice=1000&page='  # 700
#results = item_counts(html, search)
res3 = search_items(html, search)



def item_counts(html, search):
    driver.get(html+search)
    driver.implicitly_wait(1) # seconds
    
    results = driver.find_element_by_class_name('next-breadcrumb-text.activated').text
    print('results found : {}'.format(results))
    
    results = results.split('(')[-1].split()[0].replace(',','')
    results = int(results)
    
    return results

def search_items(html, search):
    # read results count
    results = item_counts(html, search)
    items_per_page = 60
    total_pages = int(results / items_per_page) + 1
    
    res = {}
    for page in range(1,total_pages+1):
        print('page {}---------------------------'.format(page))
        s_ = search + '{0}'.format(page)
        driver.get(html+s_)
        driver.implicitly_wait(1) # seconds
        
        # select body
        #body = driver.find_element_by_css_selector('body')
        #body.click()
        # pass new user coupon
        try:
            new_user = driver.find_element_by_xpath("/html/body/div[7]/div[2]/div/a") # "//next-dialog-close|//newuser-container"
        except NoSuchElementException:
            pass 
        else:
            print("new user clicked ----------")
            new_user.click()
        
        # scroll to bottom
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        
        for i in range(0,10):
            body = driver.find_element_by_tag_name('body')
            body.send_keys(Keys.PAGE_DOWN)
            driver.implicitly_wait(1) # seconds
        
        #    sleep(1)
        items = driver.find_elements_by_class_name("list-item")
        
        for (n, i) in enumerate(items):
            print('{}-----------'.format(n))
            print(i.text)
            print(i.find_element_by_tag_name('a').get_attribute('href'))
            res['p{:02d}_i{:02d}'.format(page, n)] = i.find_element_by_tag_name('a').get_attribute('href')
            
    return res


