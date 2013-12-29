VC-Matcher
========
Predicts which VC's will invest in a company based on user given data and crunchbase data.


Development Environment Installation Instructions
---
Set the following environment variables
*port- port to serve the app on
*host - host to serve the app on
*crunchbase_key - your api key for Crunchbase

 
 ```python
pip install -r requirements.txt
python app/cb_scraper.py
python sync_db.py
python app.py
 ```

How it works
---
1. It pulls from Crunchbase  a list of all the 'financial
organizations' [vcs], which include all VCs (but not most angels).
2. Goes through this list getting the info on each from Crunchbase
3. Makes a list of all VCs that have more than 19 investments [topvcs]
(it also then saves this variable as a pickle so I can restart without
going through steps 1-3 again... steps 1-3 make an awful lot of
requests to CB, so they take a while)
4. It then makes a list of all the portfolio companies to get (since
any company may have several VCs, we don't want to just go through
each VCs portfolio because then we'd be calling the API multiple times
for the same company.) [costoget]
5. It then gets each company information, gets the tag and overvew and
creates a set of cograms.
6. The last part creates sets of n-grams (grams, bigrams, trigrams)
