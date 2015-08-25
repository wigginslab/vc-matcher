"""
Uses pycrunchbase to access the following information from Crunchbase:
- List of all top VCs (defaults to VCs with more than 20 investments)
- Investments per VC

Generates n-grams (unigrams, bigrams, and trigrams -- by default)
for every top VC investment and pickes the n-grams.
"""
import argparse
import cPickle as pickle
import nltk
from nltk import ngrams
import os
import pycrunchbase
import re

class CBScraper:
    def __init__(self, api_key, vc_threshold, max_ngrams, max_num_vcs):
        self.cb = pycrunchbase.CrunchBase(api_key)
        self.vc_threshold = vc_threshold
        self.max_ngrams = max_ngrams
        self.max_num_vcs = max_num_vcs

        # MockCBScraper should override so that test files
        # can be stored elsewhere
        self.TOP_VCS_FILE = "../data/vctree2/topvcs.p"
        self.COMPANY_GRAMS1_FILE = "../data/vctree2/cograms.p"
        self.COMPANY_GRAMS2_FILE = "../data/vctree2/cograms2.p"
        self.COMPANY_GRAMS3_FILE = "../data/vctree2/cograms3.p"

        self.generate_dicts()

    def generate_dicts(self):
        # dictionary forms:
        # same form as MockCBScraper to make unit testing easier
        #
        # vc_dict -->
        # { `vc permalink` : { "name": `vc name`,
        #                      "number_of_investments" : `no. of investments`,
        #                      "investments":
        #                      [(`company permalink`, `round`, `date`), ...] } }
        # co_dict -->
        # { `company permalink` : `n-grams` }

        self.vc_dict = {}
        self.co_dict = {}

        num_investors = 0
        investors_page = self.cb.all_investors()
        while investors_page:
            # the `.all_investors()` method doesn't give us full information
            # about a VC. We have to call `.organization(`permalink`)` to get
            # more information about an investor
            for investor in investors_page:
                vc = self.cb.organization(investor.permalink)

                # only look at top VCs as determined by threshold
                if vc.number_of_investments < self.vc_threshold:
                    continue

                vc_info = {}
                vc_info["name"] = vc.name
                vc_info["number_of_investments"] = vc.number_of_investments

                vc_investments = []

                #########################################################
                # -- HACK -- return all investments by calling `.more(...)`
                # but `.more(...)` could spend an inordinate amount of time
                # so timeout quickly.
                # either pycrunchbase or the CrunchBase API is buggy
                vc_invs = None
                try:
                    # timeout after 10 seconds
                    vc_invs = timelimit(10, self.cb.more, [vc.investments])
                except TimeLimitExpired:
                    vc_invs = vc.investments
                #########################################################

                for investment in vc_invs:
                    # series could be `None`. See CrunchBase API documentation for details
                    series = investment.relationships["funding_round"] \
                             ["properties"]["series"]

                    co = investment.relationships["funding_round"]\
                         ["relationships"]["funded_organization"]["properties"]\
                         ["permalink"]

                    date = investment.relationships["funding_round"]\
                           ["properties"]["announced_on"]

                    vc_investments.append((co, series, date))
                    short_co_desc =  investment.relationships["funding_round"]\
                                     ["relationships"]["funded_organization"]\
                                     ["properties"]["short_description"]
                    self.co_dict[co] = "" if short_co_desc is None else \
                                       self.clean_up_txt(short_co_desc)

                vc_info["investments"] = vc_investments

                self.vc_dict[vc.permalink] = vc_info

                print "Top VC --> ", vc, "; investments --> ", vc.investments

                num_investors += 1
                if num_investors >= self.max_num_vcs and self.max_num_vcs != -1:
                    # so we can exit outer while loop
                    investors_page = None
                    break

            if investors_page:
                investors_page = self.cb.more(investors_page)

        """
        # Disabled for now because it does a LOT of API calls
        for co in self.co_dict:            
            self.co_dict[co] = self.generate_ngrams_for_company_full(co)
        """

    def generate_ngrams_for_company_full(self, co):
        # now obtain information about every company in `self.co_dict`
        # from the following sources:
        # categories/tags for company,
        # short & long description of company,
        # short & long description of company's products
        company = self.cb.organization(co)

        txt = ""
        txt += company.description if company.description else ""
        txt += company.short_description if company.short_description else ""

        products = company.products
        for product in products:
            txt += product.short_description if product.short_description \
                   else ""
            txt += product.description if product.description else ""
        txt += " ".join([cat.name for cat in company.categories])

        return self.clean_up_txt(txt)

    def clean_up_txt(self, txt):
        # strip EOL, apostrophes, numbers, HTML, all other punctuation, and then
        # break into sentences
        ptn1=re.compile(r"""\ba\b|\ban\b|\bthe\b|\band\b|\bthat\b|\bthis\b|
        \bto\b|\bas\b|\bfor\b|\bof\b|\bin\b|\byou\b|\byour\b|\bbut\b|
        \bwith\b|\bon\b|\bis\b|\bby\b|\bfrom\b|\btheir\b|\bit\b|\bits\b|
        \btheir\b|\bor\b|\bat\b|\bwhich\b|\bcan\b|\binc\b|\bhas\b|\bhave\b|
        \balso\b|\bthan\b|\ball\b|\bbe\b|\bthey\b|\bwas\b|\bsuch\b|
        \binto\b""", re.X)
        ptn2=re.compile(r'\&#[0-9A-F]{4};')
        #words beginning with digits--get rid of digits
        ptn3=re.compile(r'\b[0-9]+')
        # end of clause or sentence to make into periods ,;:!?
        ptn4=re.compile(r'[!\?:;]')
        # other punctuation: get rid of
        ptn5=re.compile(r'[\"$\(\)&\/,]')
        # Break into sentences
        ptn6=re.compile(r'\.[ ]+(?=[A-Z])')

        TAG_RE = re.compile(r'<[^>]+>')
	txt = TAG_RE.sub("", txt.replace("\n"," ").encode('ascii','ignore').\
                         replace('\\/','/').replace("'",""))
	txt = ptn5.sub(" ",ptn4.sub(".",ptn3.sub(" ",ptn2.sub("",txt))))
	sents = ptn6.split(txt)

        grams = set([])
	for sent in sents:
	    new_sent = ptn1.sub("",sent.lower().replace("."," ")).split()
            # generate n-grams
            for n in range(2, self.max_ngrams+1):
                grams.update(set(ngrams(new_sent, n)))

        return grams

    def pickle_grams(self):
        top_vcs = []
        for vc_permalink in self.vc_dict:
            top_vcs.append((vc_permalink,
                            self.vc_dict[vc_permalink]["name"],
                            self.vc_dict[vc_permalink]["investments"]))
        # pickle information about top VCs
        with open(os.path.join(os.path.dirname(__file__), \
                               self.TOP_VCS_FILE), "w") as f:
	    pickle.dump(top_vcs,f)

        co_grams = self.co_dict.items()
        # pickle n-grams for each company
        with open(os.path.join(os.path.dirname(__file__), \
                               self.COMPANY_GRAMS1_FILE), "w") as f:
	    pickle.dump(co_grams,f)

        totgrams = {}
        for co, grams in co_grams:
	    for gram in grams:
		totgrams[gram] = totgrams.get(gram,0) + 1

        co_grams2 = []
        co_grams3 = []
        for co, grams in co_grams:
	    grams2 = [i for i in grams if totgrams[i]>1]
	    co_grams2.append((co,grams2))

            grams3 = [i for i in grams if totgrams[i]>2]
            co_grams3.append((co,grams3))

        with open(os.path.join(os.path.dirname(__file__), \
                               self.COMPANY_GRAMS2_FILE), "w") as f:
	    pickle.dump(co_grams2,f)

        with open(os.path.join(os.path.dirname(__file__), \
                               self.COMPANY_GRAMS3_FILE), "w") as f:
	    pickle.dump(co_grams3,f)

######################################################################
# http://eli.thegreenplace.net/2011/08/22/how-not-to-set-a-timeout-on-\
#    a-computation-in-python
class TimeLimitExpired(Exception): pass

def timelimit(timeout, func, args=(), kwargs={}):
    """ Run func with the given timeout. If func didn't finish running
        within the timeout, raise TimeLimitExpired
    """
    import threading
    class FuncThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            self.result = func(*args, **kwargs)

        def _stop(self):
            if self.isAlive():
                threading.Thread._Thread__stop(self)

    it = FuncThread()
    it.start()
    it.join(timeout)
    if it.isAlive():
        it._stop()
        raise TimeLimitExpired()
    else:
        return it.result
######################################################################

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", dest="api_key", type=str, required=True,
                        help="Your Crunchbase api key")
    parser.add_argument("-t", "--top-vc-threshold", dest="vc_threshold",
                        type=int, default=20,
                        help="Least number of investments to be considered a \
                        top VC (defaults to 20)")
    parser.add_argument("-n", "--ngrams", action="count", dest="max_ngrams",
                        default=3,
                        help="Specify max type of n-gram to generate \
                        (default to 3 <--> unigrams, bigrams, and trigrams)")
    parser.add_argument("-m", "--max-vcs", type=int, default=1000,
                        dest="max_num_vcs",
                        help="Maximum number of investors to search through on \
                        Crunchbase (defaults to 1000, use -1 to search all)")

    args = parser.parse_args()
    cbs = CBScraper(args.api_key,
                    args.vc_threshold,
                    args.max_ngrams,
                    args.max_num_vcs)
    cbs.pickle_grams()

if __name__ == "__main__":
    main()
