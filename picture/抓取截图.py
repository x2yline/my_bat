import os
import time
time1 = time.time()
from selenium import webdriver
from selenium import webdriver
browser = webdriver.Ie()
print('begin')
url = "http://netclass.csu.edu.cn/jpkc2003/shenglixue/kejian/ch6.files/frame.htm"
#browser.set_window_size(1200, 900)
browser.maximize_window()
browser.get(url)
#time.spleep(10)
time.sleep(2)
browser.switch_to.frame(browser.find_element_by_name('PPTNav'))
browser.save_screenshot("1.png")
for i in range(2,63,1):
    name = str(i)+'.png'
    element = browser.find_element_by_id('nb_nextBorder').click()
    time.sleep(0.5)
    browser.save_screenshot(name)
browser.close()

def take_screenshot(url, save_fn="capture.png"):
    browser = webdriver.Chrome() # Get local session of firefox
    browser.set_window_size(1200, 900)
    browser.get(url) # Load page
    browser.execute_script("""
        (function () {
            var y = 0;
            var step = 100;
            window.scroll(0, 0);

            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 100);
                } else {
                    window.scroll(0, 0);
                    document.title += "scroll-done";
                }
            }

            setTimeout(f, 1000);
        })();
    """)

    for i in range(30):
        if "scroll-done" in browser.title:
            break
        time.sleep(10)

    browser.save_screenshot(save_fn)
    browser.close()