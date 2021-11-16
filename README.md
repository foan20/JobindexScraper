## JobindexScraper

A Selenium-based web scraper designed for jobindex.dk

## How it works

JobindexScraper works by fetching the urls of all job postings for a specific jobtitle/search term on jobindex.dk.
After this, each url is visited and checked against a wordlist (wordlist.txt). For each time a word from the wordlist is
encountered in the page source, a counter is incremented. Once all urls have been visited, the results are writen as
comma-separated values to a .xlsx file and a pie chart of counts is displayed.

## Wordlist

The wordlist is currently only equipped with cybersecurity-specific words and terms. This list is easily extendable
and/or replaceable.

## Install requirements

`python -m pip install -r requirements.txt`

## Usage

`python JobindexScraper.py "jobtitle/search-term"`
