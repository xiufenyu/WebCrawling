import os, time, re
from multiprocessing import Pool
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.options import Options  

# Run the script in session_replay
input_file = './source_code/hospital_session_replay_eu_inner_urls.csv'
output_path = './output/'
output_file = './source_code/eu_innerlinks_hotjar_ws.websocket'
failed_file = "./source_code/failed_inner_links.cvs"


def browse_url(driver, url, site, country):
   global input_file
   global output_path
   global output_file

   driver.get(url)

   print(" processing " + url + " ....")
   time.sleep(3)
   # Access requests via the `requests` attribute
   for request in driver.requests:
     if request.ws_messages:
       print("############# WS ###############")
       print(request.url)
       req_url = request.url
       with open(output_file, 'a+') as f1:
          ln1 = url + "," + req_url + "," + site + "," + country
          f1.write(ln1 + "\n")


def process_urls():
   urls = []
   with open(input_file) as fi:
      urls = fi.readlines()
      with Pool(32) as p:
         print(p.map(multi_handler, urls))


def multi_handler(line):
      line = line.strip()
      line_arr = line.split(',')
      site = line_arr[0]
      url = line_arr[2]
      country = line_arr[1]
      # Create a new instance of the Chrome driver
      chrome_options = Options()  
      chrome_options.add_argument("--headless")

      driver = webdriver.Chrome(chrome_options=chrome_options)
      driver.set_page_load_timeout(30)
      try:
         browse_url(driver, url, site, country)
      except Exception as e:
         with open(failed_file, 'a+') as f1:
            ln1 = site + "," + url + "," + site + "," + country
            f1.write(ln1 + "\n")
      finally:
         driver.quit()
         
#### MAIN ####
if os.path.exists(output_file):
   os.remove(output_file)

process_urls()