import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from pprint import pprint
from sys import platform
import wordfile

search_text_for_filename = ""
if platform == "linux" or platform == "linux2":
    geckodriver = "geckodriver/geckodriver"
elif platform == "win32":
    geckodriver = "geckodriver/geckodriver.exe"

base_url = "https://www.jobindex.dk/"
urls = []
word_dict = []


def extract_items_from_urls(browser, search_text):
    for url in urls:
        try:
            print("Going to URL: " + url)
            browser.get(url)
            for word in word_dict:
                if word in browser.page_source:
                    print("Found word " + word + " in page source! Incrementing word count.")
                    word_dict[word] += 1
        except TimeoutException:
            print("Page loading timed out.. Going to next page.")

    print("All URLs visited. Writing results to file.")

    wordfile.write_results_to_file(search_text, word_dict)


def scrape_all_search_pages(browser, search_text):
    index = 1

    while True:
        cookies_and_popups_disabled = False

        # Set up URL.
        page_nr = "page=" + str(index)
        search_string = "jobsoegning?" + page_nr + "&q=" + search_text
        search_url = base_url + search_string

        # Open search page.
        print("Opening page: " + search_url)
        browser.get(search_url)

        # Scrape current search page.
        print("Scraping page " + str(index))
        scrape_search_page(browser, cookies_and_popups_disabled)

        if index > 0:
            cookies_and_popups_disabled = True

        # Break if no more pages to search (i.e. If no next page button).
        try:
            browser.find_element(By.XPATH, "//a[@aria-label='Næste']")
        except NoSuchElementException:
            print("No more pages to search. Breaking..")
            break

        # Increment index and go to next page.
        index += 1
        print("Going to next page.")

    pprint(urls)
    total_jobs = len(urls)
    print("Found " + str(total_jobs) + " total job postings.")


def scrape_search_page(browser, cookies_and_popups_disabled):
    print("Cookies and popups disabled: " + str(cookies_and_popups_disabled))
    if cookies_and_popups_disabled:
        # Accept all cookies.
        accept_cookies = browser.find_element(By.ID, "jix-cookie-consent-accept-all")
        if accept_cookies:
            accept_cookies.click()
            sleep(0.05)

        # Close jobmail popup.
        jobmail_popup = browser.find_element(By.XPATH, "//button[@class='close']")
        if jobmail_popup:
            jobmail_popup.click()
            jobmail_popup.click()
            sleep(0.05)

    # Find "view job" buttons.
    results = browser.find_elements(By.XPATH, "//a[@class='btn btn-sm btn-primary']")
    sleep(0.05)

    j = 0

    for result in results:
        href = result.get_attribute("href")
        urls.append(href)
        j += 1

    print("Found " + str(j) + " job postings.")


def main():
    global search_text_for_filename
    search_text = sys.argv[1]
    temp_string = search_text.split()
    search_text_for_filename = "_".join(temp_string)

    if len(search_text) < 3:
        print("Search text to short. Write a longer search text.")
        return

    print("Searching for search text: " + search_text)

    global word_dict
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(executable_path=geckodriver, options=options)
    browser.set_page_load_timeout(10)

    try:
        # word_dict = wordfile.get_word_dict()
        # scrape_all_search_pages(browser, search_text)
        # extract_items_from_urls(browser, search_text)
        wordfile.export_to_csv_to_excel("results/results_for__Azure AD_")
    except Exception as e:
        print(e)
        browser.quit()
    browser.quit()


if __name__ == "__main__":
    main()
