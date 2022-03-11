import requests
import config
import tldextract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pprint
from PIL import Image


# retrieving assets from API
def get_data(app_id):
    api_base_url = f'http://osint.bevigil.com/api/'
    endpoint_path = f'{app_id}/all-assets/'
    headers = {
        'X-Access-Token': config.api_key
    }

    endpoint = f'{api_base_url}{endpoint_path}'
    pprint.pprint(endpoint)

    r = requests.get(endpoint, headers=headers)

    if r.status_code in range(200, 299):
        contents = r.json()
        data = contents.get('assets')
        return data


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


# function to count no. of unique elements
def get_no_of_elements(l):
    count = 0
    for element in l:
        count += 1
    return count


# app_id input from user
app_id = input('Enter APP ID here (com.example.com) : ').lower().strip()


data = get_data(app_id)

try:
    hostnames = data.get('host')
except AttributeError as ae:
    print('Invalid App Id: ' + app_id)
    exit()

ip = data.get('IP Address disclosure')
pprint.pprint(ip)

# storing the extracted domain names to the newlist
assets = domain_extract(hostnames)

# Converting the list to dictionary and removing empty key values (if any) to make it readable for wordcloud
hosts = to_dict(assets)
hosts = dict([(k, v) for k, v in hosts.items() if len(k) > 0])
pprint.pprint(sorted(hosts.items(), key=lambda x: x[1], reverse=True))

pprint.pprint("Unique Hostnames found: " + str(get_no_of_elements(hosts)))
pprint.pprint("Unique IP found: " + str(get_no_of_elements(ip)))

# asking user if they want to generate a report
answer = input("Do you want to Generate a report  (y/n): ").lower().strip()
if answer == "y":
    # generating a Report.txt in the working directory
    with open(app_id.replace('.', '_') + "_report.txt", 'w') as f:
        f.write("Unique IP found: " + str(get_no_of_elements(ip)) + '\n\n')
        f.write("Unique Hostnames found: " + str(get_no_of_elements(hosts)) + '\n\n')
        f.write('Hostnames with no. of occurrence in  file: \n\n')
        for key, value in (sorted(hosts.items(), key=lambda x: x[1], reverse=True)):
            f.write('%s:%s\n' % (key, value))
        f.write('\n Unique IP addresses found in file: \n\n')
        f.write(str(ip))
        pprint.pprint('Report generated successfully!(in current working directory)')
elif answer == "n":
    pass

# asking user if they want to generate & save wordcloud
answer = input("Do you want to  Display  & save the WorldCloud image(y/n): ").lower().strip()
if answer == "y":
    # wordcloud
    wordcloud = WordCloud(mode='RGBA',
                          background_color='rgba(255, 255, 255, 0)').generate_from_frequencies(hosts)

    # Image process
    image = Image.fromarray(wordcloud.to_array())
    background = Image.open('darth-vader.png').convert('RGBA')
    image = image.resize(background.size)
    background = background.resize(image.size)
    new_image = Image.alpha_composite(background, image)

    # display wordcloud image
    plt.figure(figsize=(15, 8))
    plt.axis('off')
    plt.imshow(new_image)
    plt.show()

    # Save the wordcloud image
    plt.figure()
    plt.axis('off')
    fig = plt.imshow(new_image, interpolation='nearest')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig(app_id.replace('.', '_')+'.png',
                bbox_inches='tight',
                pad_inches=0,
                format='png',
                dpi=1000)
    pprint.pprint('Image saved')

elif answer == "n":
    exit()
