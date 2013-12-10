"""
Redips - A basic web crawler
Compatible with Python 2.7.X
"""
import urllib2
import re
import cPickle
from bs4 import BeautifulSoup
from urllib2 import urlopen
from urlparse import *

def load(pickle):
    """
    file(pickle) -> Redips
    Load the crawler stored in the pickle file
    """
    with open(pickle, 'rb') as pickle_file:
        redips = cPickle.load(pickle_file)
        redips.pickle = pickle
    return redips

class Redips:
    """
    Redips is the crawler that crawls a seed url
    """
    def __init__(self, seed_url = None, pickle = 'redips.pickle'):
        self.index = {}
        self.graph = {}
        if seed_url:
            self.to_crawl = [seed_url]
        else:
            self.to_crawl = []
        self.crawled_links = []
        self.pickle = pickle

    def add_url(self, url):
        """
        string(url) -> None
        Add the url to the list of links to crawl
        """
        self.to_crawl.append(url)
    
    def save(self):
        """
        None -> None
        Save the state of the crawler in a pickle
        """
        with open(self.pickle, 'wb') as pickle:
            cPickle.dump(self, pickle)

    def crawl(self):
        """
        None -> None
        crawl the links in the to_crawl list and create an index of keywords
        and a graph of links 
        index: {keyword : [url1, url2, url3...]}
        graph: {url : [outlink1, outlink2, 
        """

        # Iteratively crawl fetched links
        while self.to_crawl:
            # Extract a link from the links to crawl list
            url = self.to_crawl.pop(0)
            
            # Crawl if the extracted link is not already crawled
            if url not in self.crawled_links:
                print "Crawling " + url
                self.crawl_page(url)
                self.crawled_links.append(url)

        print "Crawl Finished"
            
    def get_url(self, url):
        """
        string -> Url
        Open the input url
        """
        try:
            url_object = urlopen(url)
        except urllib2.URLError:
            print "Invalid seed url"
            return
        
        # Redirect the url if possible
        redirected_url = url_object.geturl()
        redirected_url_object = urlopen(redirected_url)

        return redirected_url_object

    def get_source_page(self, url):
        """
        Url -> string
        Return the source page of the input url
        """
        try:
            page = url.read()
        except:
            return ""
        return page

    def crawl_page(self, seed_url):
        """
        string -> index, graph
        Crawl the page by:
        - Adding the seed_url's entry into the graph
        - Adding the contents of the seed_url page to the index
        and return the graph and index
        """
        # Make a blank entry in the graph for the seed_url
        self.graph[seed_url] = []
        
        # Open the seed url
        url = self.get_url(seed_url)
        
        # Get the source page of the url
        source_page = self.get_source_page(url)
        
        # Make a Beautiful Soup of the source page
        soup = BeautifulSoup(source_page)
        
        # Extract links and add them to the graph
        for link in soup.find_all('a'):
            fetched_link = link.get('href')
            if fetched_link:
                fetched_link = self.convert_to_absolute(url.geturl(), fetched_link)
                self.to_crawl.append(fetched_link)
                self.graph[seed_url].append(fetched_link)
        
        # Add page to the index
        self.add_page_to_index(seed_url, soup)

    def convert_to_absolute(self, seed_url, url):
        """
        string, string -> string
        Convert the input url from relative to absolute
        """
        parsed_link = urlparse(url)
            
        if not parsed_link.scheme:
            return urljoin(seed_url, url)
        else:
            return url

    def add_page_to_index(self, seed_url, soup = None):
        """
        string(seed_url), BeautifulSoup(soup) -> None
        Add all the words on the seed url to the index
        """
        
        # Make the soup if not supplied
        if not soup:
            print "making soup"
            soup = BeautifulSoup(self.get_url(seed_url).read())
        
        # Get the content of the page
        content = soup.get_text()
        words = re.findall(r"[\w']+", content)
        
        # Add each word on the page to the index
        for word in words:
            self.add_to_index(seed_url, word)

    def add_to_index(self, seed_url, word):
        """
        string(seed_url), string(word) -> None
        Add the input word to the index
        """
        if word in self.index:
            self.index[word].add(seed_url)
        else:
            self.index[word] = set([seed_url])
            
    def get_index(self):
        """
        None -> dict(index)
        Return the index
        """
        return self.index

    def get_graph(self):
        """
        None -> dict(graph)
        Return the graph
        """
        return self.graph

    def reset_to_crawl(self):
        """
        None -> None
        Clear the fetched links list of the crawler
        """
        self.to_crawl = []
