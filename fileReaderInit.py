import re
from urllib.request import urlopen


def file_reader():
    response = urlopen('http://www.gutenberg.org/files/2600/2600-0.txt')
    content = response.read(10000).decode("utf-8-sig")  # read file in parts of 10000
    words = re.findall(r'\w+', content.lower())
    print(words)
    print(len(words))

    counts = dict()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    print(max(counts, key=counts.get), ":", counts[max(counts, key=counts.get)])

    # TODO (Ayush) run this with multi-threading
    # TODO count max 5


if __name__ == '__main__':
    file_reader()
