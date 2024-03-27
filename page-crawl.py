import requests
from bs4 import BeautifulSoup
import multiprocessing
import time

def extract_arxiv_results(url):
    max_retries = 10
    retry_delay = 1  # Initial retry delay in seconds
    ans = ''

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract title
                title = soup.find('h1', class_='title').text.strip().split('Title:')[-1]

                # Extract abstract
                abstract = soup.find('blockquote', class_='abstract').text.strip().split('Abstract:')[-1]
                ans = title + '\n' + abstract + '\n'
                return ans, None
                
            elif response.status_code == 429:
                # Retry after waiting for increasing amount of time
                print(f"Received 429 status code. Retrying after {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Exponential backoff: increase the delay exponentially
                retry_delay *= 2
            else:
                print(f"Unexpected status code: {response.status_code}")

        except Exception as e:
            print(f"Error occurred: {e}")
    
    print("Max retries exceeded. Unable to make request.")
    return ans, url


def process_one(i, sub_list):
    full_text = ''
    error_urls = ''
    for tmp in sub_list:
        print(tmp.split('arXiv:')[-1].split('\n')[0])
        url = 'https://arxiv.org/abs/'+tmp.split('arXiv:')[-1].split('\n')[0]
        ans, err = extract_arxiv_results(url)
        full_text += ans
        if err is not None:
            error_urls += err + '\n'
    with open('arxiv_text'+str(i)+'.txt', 'w') as fi:
        fi.write(full_text)
    with open('arxiv_text_error'+str(i)+'.txt', 'w') as fi:
        fi.write(error_urls)


with open('id.txt', 'r') as fi:
    search_list = fi.readlines()
print(len(search_list))

sublist_size = len(search_list) // 50
sublist = [search_list[i*sublist_size:(i+1)*sublist_size] for i in range(50)] 
if len(search_list) % 50 != 0:
    remainder = len(search_list) % 50
    for i in range(remainder):
        sublist[i].append(search_list[-(i+1)]) 

cmds = []
for i in range(50):
    cmds.append((i, sublist[i]))

with multiprocessing.Pool(processes=3) as pool: # Too many processes may cause status code of 429
    pool.starmap(process_one, cmds)
