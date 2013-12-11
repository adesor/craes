"""
craes: A search engine implemented in Python
- Uses the rank generated by reknar
- Uses the index generated by redips
"""

import reknar
import redips
import random

class Craes:
    def __init__(self, index=None, ranks=None):
        if not index:
            red = redips.load('redips.pickle')
            self.index = red.get_index()
        else:
            self.index = index

        if not ranks:
            rek = reknar.load('reknar.pickle')
            self.ranks = rek.get_ranks()
        else:
            self.ranks = ranks
    
    def lookup(self, keyword):
        """
        string(keyword) -> list(URL)
        Return the list of URLs corresponding to the input keyword
        in the index
        """
        if keyword in self.index:
            return list(self.index[keyword])
        return None

    def get_best(self, keyword):
        """
        string(keyword) -> string(URL)
        Return the URL best suited for the input keyword
        """
        pages = self.lookup(keyword)

        if not pages:
            print "Sorry,", keyword, " is not in our index yet!"
            return

        best_page = pages[0]
        for page in pages:
            if self.ranks[page] > self.ranks[best_page]:
                best_page = page
        return best_page

    def lucky_search(self, keyword):
        """
        string(keyword) -> None
        Print the best search result
        """
        print self.get_best(keyword)

    def get_results(self, keyword):
        """
        string(keyword) -> list(string(URL))
        Return a list of URLs corresponding to the given keyword
        ordered by their ranks
        """
        
        pages = self.lookup(keyword)
        if not pages:
            print "Sorry,", keyword, " is not in our index yet!"
            return

        self.quick_sort(pages, 0, len(pages))
        return pages

    def search(self, keyword):
        """
        string(keyword) -> None
        Print a list of URLs corresponding to the given keyword
        ordered by their ranks
        """
        pages = self.get_results(keyword)
        for page in pages:
            print page

    def quick_sort(self, pages, start_pt, end_pt):
        if start_pt < end_pt - 1:
            partition_pt = self.partition(pages, start_pt, end_pt)
            self.quick_sort(pages, start_pt, partition_pt)
            self.quick_sort(pages, partition_pt + 1, end_pt)

    def partition(self, pages, start_pt, end_pt):
        random_pos = random.randrange(start_pt, end_pt)
        pages[start_pt], pages[random_pos] = pages[random_pos], pages[start_pt]
        pivot = pages[start_pt]
        pivot_pos = start_pt
        i = start_pt + 1
        for j in range(start_pt + 1, end_pt):
            if self.ranks[pages[j]] > self.ranks[pivot]:
                pages[i], pages[j] = pages[j], pages[i]
                i += 1
        pages[pivot_pos], pages[i-1] = pages[i-1], pages[pivot_pos]
        return i-1

