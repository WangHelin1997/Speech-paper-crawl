import requests
from bs4 import BeautifulSoup

def extract_arxiv_results(url):
    alltext = []
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <li> elements with class "arxiv-result"
        arxiv_results = soup.find_all('li', class_='arxiv-result')

        # Iterate through each <li> element
        for result in arxiv_results:
            # Find the <p> element with class "list-title is-inline-block" within the <li> element
            p_tag = result.find('p', class_='list-title is-inline-block')
            if p_tag:
                # Extract and print the text of the <p> element
                alltext.append(p_tag.text.strip().split('\n')[0])

    else:
        print("Failed to retrieve webpage. Status code:", response.status_code)
    
    return alltext

search_list=[
    'speech', 'voice', 'spoken', 'audio', 'sound', 'acoustic', 'speech content', 'spoken language'
    'Acoustic Echo Cancellation', 'Speech Dereverberation', 'Speech Enhancement', 'Speech-to-speech Translation',
    'Speech Separation', 'Voice Conversion',
    'DeepFake Detection', 'Dialogue Act Classification', 'Enhancement Detection', 'MultiSpeaker Detection', 'Noise Detection', 'Reverberation Detection', 'Sarcasm Detection', 'Speech Detection', 'Spoof Detection', 'Stress Detection',
    'Accent Classification', 'Dialogue Act Classification', 'Dialogue Emotion Classification', 'Emotion Recognition', 'Intent Classification', 'Language Identification', 'Non-verbal Voice Recognition', 'Offensive Language Identification', 'Speaker Counting', 'Speaker Identification', 'Speech Command Recognition', 'Vocal Sound Classification',
    'Speaker Diarization', 'Overlapping Speech Detection',
    'Dysarthric Speech Assessments', 'HowFarAreYou', 'Noise SNR Level Prediction', 'Speech Quality Assessment',
    'Laughter Synthesis', 'Target Speaker Extraction',
    'Speaker Verification',
    'Dialogue Act Pairing', 'Keyword Spotting',
    'Accented Text-to-speech', 'Speech Edit',
    'Speech Text Matching', 'Spoken Term Detection',
    'Instruct TTS', 'Text-To-Speech Synthesis',
    'Emotional TTS', 'Expressive TTS',
]
search_list = [tmp.replace(' ', '+') for tmp in search_list]

output = []
for tmp in search_list:
    for i in range(0, 10000, 200):
        url = 'https://arxiv.org/search/?query='+tmp+'&searchtype=all&abstracts=show&order=-announced_date_first&size=200&start=' + str(i)
        print(url)
        alltext = extract_arxiv_results(url)
        output = [*output, *alltext]

output = list(set(output))
with open('arxiv_id.txt', 'w') as fi:
    for x in output:
        fi.write(x+'\n')