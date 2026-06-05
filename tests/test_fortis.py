# import requests

# url = "https://fa-ermg-saasfaprod1.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.workLocation,requisitionList.otherWorkLocations,requisitionList.secondaryLocations,flexFieldsFacet.values,requisitionList.requisitionFlexFields&finder=findReqs;siteNumber=CX_1,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=25,lastSelectedFacet=CATEGORIES,selectedCategoriesFacet=300000787441924,sortBy=POSTING_DATES_DESC"

# response = requests.get(url)

# print("Status:", response.status_code)

# data = response.json()

# print(data.keys())
# requisitions = data["items"][0]["requisitionList"]

# print(f"Total Jobs: {len(requisitions)}")
# print("\nFirst Job:\n")
# print(requisitions[0])
# # tests/test_fortis.py

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scraper.parsers.fortis_parser import FortisParser


parser = FortisParser()

jobs = parser.fetch_jobs()

print("\nFirst Job:\n")

if jobs:
    print(jobs[0])

print(f"\nTotal Jobs: {len(jobs)}")