import tldextract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import pandas as pd


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

#function to count no. of unique elements
def get_no_of_elements(l):
    count = 0
    for element in l:
        count += 1
    return count

# your csv file path
file_path = 'csv_file_path'

# extracting the index of the hostname from the downloaded Report.csv file
df = pd.read_csv(file_path, usecols=['Rule'])
column_of_interest = df['Rule']
print(type(column_of_interest))
data = column_of_interest.to_dict()

for k, v in data.items():
    if v == 'Hostname':
        index = k  # k is the index of the hostname in csv file

# saving the hostname row from csv file to the hostnames variable
hostnames = pd.read_csv(file_path, sep=",")['Matched Files'][index]
hostnames = re.sub("\(.*?\)", "", hostnames)

file = convert(hostnames)

# storing the extracted domain names to the newlist
assets = domain_extract(file)

# Converting the list to dictionary and removing empty key values (if any) to make it readable for wordcloud
freq = to_dict(assets)
freq = dict([(k, v) for k, v in freq.items() if len(k) > 0])
print(sorted(freq.items(), key=lambda x: x[1], reverse=True))

# wordcloud
wordcloud = WordCloud(width=1000, height=500).generate_from_frequencies(freq)

# display wordcloud image
plt.figure(figsize=(15, 8))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

# ip_address list generate

f = open(file_path, 'rb')
doc = str(f.read())

ip_addresses = list((re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3} ', doc)))
ip_addr = []
for unique_ip in ip_addresses:
    if unique_ip not in ip_addr:
        ip_addr.append(unique_ip)
print(ip_addr)

# generating a Report.txt in the working directory
with open("Generated_report.txt", 'w') as f:
    f.write("Unique IP found: " + str(get_no_of_elements(ip_addr)) + '\n\n')
    f.write("Unique Hostnames found: " + str(get_no_of_elements(freq)) + '\n\n')
    f.write('Hostnames with no. of occurrence in  file: \n\n')
    for key, value in (sorted(freq.items(), key=lambda x: x[1], reverse=True)):
        f.write('%s:%s\n' % (key, value))
    f.write('\n Unique IP addresses found in file: \n\n')
    f.write(str(ip_addr))
print('File generated successfully!')
