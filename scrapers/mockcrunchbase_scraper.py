"""
MockCBScraper is a mock subclass of CBScraper to be used for 
testing only.
"""
from crunchbase_scraper import CBScraper
import nltk
import os
import random
import string

class MockCBScraper(CBScraper):
    def __init__(self):
        # generate unigrams, bigrams, and trigrams
        self.max_ngrams = 3

        self.TOP_VCS_FILE = "../data/tests/vctree/topvcs.p"
        self.COMPANY_GRAMS1_FILE = "../data/tests/vctree/cograms.p"
        self.COMPANY_GRAMS2_FILE = "../data/tests/vctree/cograms2.p"
        self.COMPANY_GRAMS3_FILE = "../data/tests/vctree/cograms3.p"

        self.generate_dicts()

    def generate_dicts(self):
        # Generates 3125 = 5^5 VCs: aaaaa, aaaab, ..., eeeed, eeeee
        # Investments per VCs: a -> 1, b -> 2, c -> 3, d -> 4, e -> 5
        #   for example: "aabde" has 1 + 1 + 2 + 4 + 5 = 13 investments
        # Non-VC companies: "a", "b", ..., "z"
        #
        #
        # dictionary forms:
        # vc_dict -->
        # { `vc permalink` : { "name": `vc name`,
        #                      "number_of_investments" : `no. of investments`,
        #                      "investments":
        #                      [(`company permalink`, `round`, `date`), ...] } }
        # co_dict -->
        # { `company permalink` : `n-grams` }
        chars = "abcde"
        vc_names = [''.join([chars[i], chars[j], chars[k], chars[l], chars[m]])\
                    for i in range(5) for j in range(5) for k in range(5) \
                    for l in range(5) for m in range(5)]
        co_names = [chr(i+ord('a')) for i in range(26)]

        self.vc_dict = {}
        for vc_name in vc_names:
            self.vc_dict[vc_name] = {}

            # (VC name) == (VC permalink) in this case but this is
            # not the case for the production crunchbase scraper
            self.vc_dict[vc_name]["name"] = vc_name

            num_invs = self.get_number_of_investments(vc_name)
            self.vc_dict[vc_name]["number_of_investments"] = num_invs
            self.vc_dict[vc_name]["investments"] = []
            for co in co_names[:num_invs]:
                self.vc_dict[vc_name]["investments"].append((co, 'A', '2015-02-02'))

        self.co_dict = {}
        for co in co_names:
            # generate random text with 100 random words
            self.co_dict[co] = []
            for i in range(100):
                self.co_dict[co].append(''.join(random.sample(string.letters,
                                                      random.randint(4, 10))))

    def get_number_of_investments(self, vc_name):
        return sum([(ord(ch)-ord('a')+1) for ch in vc_name])
