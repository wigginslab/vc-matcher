import unittest2 as unittest
from scrapers import *

class TestCBScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = MockCBScraper()

    def test_topvcs_pickled_correctly(self):
        self.scraper.pickle_grams()

        top_vcs = None
        with open(os.path.join(os.path.dirname(__file__), \
                               self.scraper.TOP_VCS_FILE)) as f:
            top_vcs = pickle.load(f)

        for (vc_permalink, vc_name, vc_investments) in top_vcs:
            self.assertIn(vc_permalink, self.scraper.vc_dict)
            vc_info = self.scraper.vc_dict[vc_permalink]

            self.assertEqual(vc_name, vc_info["name"])

            for i in range(len(vc_investments)):
                company, series, date = vc_investments[i]
                vc_info_invs = vc_info["investments"]

                self.assertEqual(company, vc_info_invs[i][0])
                self.assertEqual(series, vc_info_invs[i][1])
                self.assertEqual(date, vc_info_invs[i][2])

if __name__ == "__main__":
    unittest.main()
