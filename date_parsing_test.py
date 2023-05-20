import time
import dateutil.parser as parser
import re

test_dates = ['2022-06-12T18:01:58.181Z',
              '2022-06-12 10:30 pm',
              '2022-06-12',
              '10:30 pm',
              'apple',
              '123test']

date_pattern = r'(?:\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[a-z\s,.]*(?:\d{1,2}[-/th|st|nd|rd)\s,]*)+(?:\d{2,4})+'
time_pattern = r'((T?)(\d{2}\:\d{2}?\:?\d{2})?(\.?\d{,3}?)?\s?(?:Z|AM|PM|am|pm))?'
time_pattern2 = r'\s(\d{2}\:\d{2}\s?(?:AM|PM|am|pm))'

def regex_time(match_string:str,
               pattern:str):
    start = time.perf_counter()
    out = re.search(pattern,match_string)
    end = time.perf_counter()
    print(f'Regex execution time: {end - start} seconds')
    return out

def dateutil_time(match_string:str):
    start = time.perf_counter()
    try:
        out = parser.parse(match_string)
    except:
        out = None
    end = time.perf_counter()
    print(f'Dateutil execution time: {end - start} seconds')
    return out

for test_str in test_dates:
    temp = regex_time(test_str,
                      date_pattern+time_pattern)
    print(f'Test string: {test_str}')
    if temp:
        print('Regex Date found')
        print(temp)
    else:
        print('***NO DATE FOUND***')
    temp = dateutil_time(test_str)
    if temp:
        print('Dateutil Date found')
        print(temp)
    else:
        print('***NO DATE FOUND***')
