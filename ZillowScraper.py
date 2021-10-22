import Selenium_module as zm

print("Zillow Downloader")
url = input("URL: ")

image_links, title = zm.get_links(url)
zm.get_images(image_links, title)
zm.cleanup_exit()
