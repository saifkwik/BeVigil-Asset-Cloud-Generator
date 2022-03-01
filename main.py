import tldextract
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# function to convert string to list


def convert(string):
    li = list(string.split("\n"))
    return li


# function to extract domain names from the list
def domain_extract(word):
    asset = []
    for domains in word:
        asset.append(tldextract.extract(domains).registered_domain)
    return asset


# function to count the occurrence of words
def to_dict(assets):
    frequencies = {}
    for word in assets:
        if word not in frequencies:
            frequencies[word] = 1
        else:
            frequencies[word] += 1
    return frequencies


# to import text file and save it as string
f = open('C:\\Users\\Rango\\Documents\\bgmi.txt', 'rb')
file_contents = f.read().decode(encoding='utf-8')

file = convert(file_contents)

# storing the extracted domain names to the newlist
assets = domain_extract(file)
print(assets)

# Converting the list to dictionary to make it readable for wordcloud
freq = to_dict(assets)
print(sorted(freq.items(), key=lambda x: x[1], reverse=True))
# wordcloud
wordcloud = WordCloud(width=1000, height=500).generate_from_frequencies(freq)

# display wordcloud image
plt.figure(figsize=(15, 8))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
