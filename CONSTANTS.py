import os

BASE_URL = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?' \
           'resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&isDescending=false'

CONCURRENCY = 20
TIMEOUT = 120
BASE_DIR = os.path.abspath('upload/')
