from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
import urllib.request
import os
import sys
import time

browser = webdriver.Firefox()


def wait(delay): #Wait until the website has finished loading
  
  WebDriverWait(browser, delay).until(lambda browser: browser.execute_script("return document.readyState") == "complete")

def get_links(url):

  browser.get(url)

  wait(10)
  element = browser.find_element_by_class_name("ds-media-col")
  print("Please wait...")
  time.sleep(5)
  browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight * (1/3)", element)
  time.sleep(5)
  browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight * (2/3)", element)
  time.sleep(5)
  browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
  time.sleep(5)

  resource = browser.page_source
  images = bs(resource, "lxml").find_all("img")

  image_links=[]

  for image in images:
    try:
      image_links.append(image["src"])
    except:
      pass

  for video in videos:
    try:
      image_links.append(video["src"])
    except:
      pass

  for a in range(0,len(image_links)):
    temp=image_links[a]
    cutoff=temp.find("-cc")
    if cutoff!=-1 and "-cc" in temp:
      image_links[a]=temp[0:cutoff]+"-uncropped_scaled_within_1536_1152.webp"
    elif ".mp4" in temp:
      image_links[a]=temp
    else:
      image_links[a]=None
  while None in image_links:
    image_links.remove(None)
  
  image_count = len(image_links)
  print(str(image_count) + " images found.")
  user = input("Proceed to download? (Y/N): ")
  if user.upper() == "Y":
    pass
  else:
    cleanup_exit()
  
  title = browser.title
  title = title.split(" | ", 1)[0]

  return image_links, title

def get_images(image_links, title):

  folderdir = title

  if not os.path.exists(folderdir):
    print("Creating folder: "+folderdir)
    try:
      os.mkdir(folderdir)
    except Exception as e:
      print(e)
      cleanup_exit()

  index = 0
  for link in image_links:
    filename = link.split("/")[-1].split("?")[0]
    filename = os.path.join(folderdir+"/"+filename)

    dindex = index + 1
    print("(" + str(dindex) + "/" + str(len(image_links)) + ") " + link)
    index = index + 1
    try:
      urllib.request.urlretrieve(link, filename=filename)
    except Exception as e:
      print("(" + str(dindex) + "/" + str(len(image_links)) + ") " + str(e))

def cleanup_exit():
  browser.close()
  browser.quit()
  sys.exit(0)
