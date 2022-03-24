import requests
import bs4
# We need to use an older version of Gensim for this to work
from gensim.summarization import summarize
from nltk.tokenize import sent_tokenize

# Gensim is a package that uses machine learning under the hood to make summaries.
# It's built upon the google PageRank algorithm, and checks how sentences are linked to other sentences

def get_speech():
   url = 'https://singjupost.com/we-should-all-be-feminists-by-chimamanda-ngozi-adichie-full-transcript/?singlepage=1'
   page = requests.get(url)
   page.raise_for_status()
   soup = bs4.BeautifulSoup(page.text, 'html.parser')

   # Remove the first 3 elements and the last 6, since they are not part of the speech
   p_elements = [element.text for element in soup.select('.entry-content p')][3:]
   p_elements = [element.text for element in soup.select('.entry-content p')][:-6]


   speech = ''.join(p_elements)
   return speech

def main():
   print('\nSummary of We Should All Be Feminists, by Chimamanda Ngozi Adichie:\n')

   speech = get_speech()
   summary = summarize(speech, word_count=225)

   # We clean up the summary since gensim sometimes duplicates sentences (therefore we use a set)
   sentences = sent_tokenize(summary)
   sents = set(sentences)

   print(' '.join(sents))

main()

