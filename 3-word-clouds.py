import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud, STOPWORDS

# Uses for word clouds: 
# See a quick summary of things with the most prominent words highlighted
# E.g. Get overal customer feedback
# E.g. check keyword density of website texts for SEO

with open('chat_2.txt', encoding='utf-8', errors='ignore') as infile:
    text = infile.read()

formatted_text = re.sub('\d{2}\/\d{2}\/\d{4},\s\d{2}:\d{2}\s-\s(Erle|Judit):\s', '', text)
formatted_text = re.sub('\<Media omitted\>', '', formatted_text)


mask = np.array(Image.open('heart.png'))

stopwords = STOPWORDS
# stopwords.update(['now', 'yes', 'one', 'will', 'P', 'really', 'Ok', 'want'])

wc = WordCloud(max_words=500,
    relative_scaling=0.5, 
    mask=mask, 
    background_color='black',
    stopwords=stopwords,
    margin=2,
    random_state=7, # This fixes the seed nr so results are repeatable
    contour_width=0,
    # contour_color='black',
    colormap='Spectral'
    ).generate(formatted_text)

colors = wc.to_array()

plt.figure(figsize=(500,500))
plt.imshow(colors, interpolation='bilinear')
plt.axis('off')
plt.show()

# Doesn't work, probably because my image format is weird. I should try with png
plt.savefig('chat-cloud.png')
