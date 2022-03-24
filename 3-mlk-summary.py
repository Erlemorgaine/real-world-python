from collections import Counter
import re
import requests
import bs4
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

def remove_stopwords(speech_edit):
    # Returns string
    stop_words = set(stopwords.words('english'))
    speech_edit_no_stop = ''

    for word in nltk.word_tokenize(speech_edit):
        if word.lower() not in stop_words:
            speech_edit_no_stop += word + ' '
    
    return speech_edit_no_stop

def get_word_freq(speech_edit_no_stop):
    # Return a dictionary of word frequency in a string
    word_frequency = nltk.FreqDist(nltk.word_tokenize(speech_edit_no_stop.lower()))
    return word_frequency

def score_sentences(speech, word_frequencies, max_words):
    # Return dictionary of sentence scores based on word frequencies
    sentence_scores = dict()
    sentences = nltk.sent_tokenize(speech)

    for sentence in sentences:
        sentence_scores[sentence] = 0

        # Get list with words for sentence
        words = nltk.word_tokenize(sentence.lower())
        sentence_word_count = len(words)
        
        if sentence_word_count <= int(max_words):
            for word in words:

                # If the word is in the dictionary of word frequencies, add the word frequency 
                # (normalised: relative to the amount of words in the sentence) to the sentence score
                if word in word_frequencies.keys():
                    sentence_scores[sentence] += word_frequencies[word] / sentence_word_count

    return sentence_scores

def main():
    url = 'http://www.analytictech.com/mb021/mlk.htm'
    page = requests.get(url)
    page.raise_for_status()
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    p_elements = [element.text for element in soup.find_all('p')]

    speech = ''.join(p_elements)
    
    # Fix spelling error
    speech = speech.replace(')mowing', 'knowing')
    # Substitute multiple whitespaces in a row
    speech = re.sub('\s+', ' ', speech)
    # Remove non-letters
    speech_edit = re.sub('[^a-zA-Z]', ' ', speech)
    speech_edit = re.sub('\s+', ' ', speech_edit)

    while True:
        max_words = input('Enter max words per sentence for summary')
        num_sents = input('Enter number of sentences for summary')

        if max_words.isdigit() and num_sents.isdigit():
            break
        else:
            print('\nInput must be in whole numbers.\n')

    speech_edit_no_stopwords = remove_stopwords(speech_edit)
    word_freq = get_word_freq(speech_edit_no_stopwords)
    # Get which sentences have the most of the most frequent words
    sent_scores = score_sentences(speech, word_freq, max_words)

    # This ranks the sentences
    counts = Counter(sent_scores)
    summary = counts.most_common(int(num_sents))

    print('\nSummary:')
    for i in summary:
        print(i[0])


main()