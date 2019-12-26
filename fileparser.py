# pip install requests
# pip install numpy
import threading
import time
from math import ceil
from collections import Counter
import requests
import re
import numpy


class FileReader:
    def __init__(self):
        self._url = 'https://www.gutenberg.org/files/2600/2600-0.txt'
        self._file_size = 0

        mb = 1024 * 1024
        self._chunk_size = 1 * mb

        self._total_words_in_file = 0
        self._total_word_list = []

    def _top_5(self, total_word_list):
        counter_word = Counter(total_word_list)
        most_occurred_words = counter_word.most_common(5)
        print("most_occurred_words: ", most_occurred_words)
        return most_occurred_words

    def _get_word_list(self, word_list):
        word_numpy_array = numpy.array(word_list)
        unique, counts = numpy.unique(word_numpy_array, return_counts=True)
        occurrence_dict = dict(zip(unique, counts))
        # print(occurrence_dict)
        most_used_word = max(occurrence_dict, key=occurrence_dict.get)
        print(most_used_word, ':', occurrence_dict[most_used_word])
        return unique.tolist()

    def _get_total_word_count(self, content: str):
        total_words = re.findall(r'\w+', content.lower())
        # print("total words in part: ", len(total_words))
        return total_words

    def _read_file(self, headers):
        response = requests.get(self._url, headers=headers)
        response.encoding = 'utf-8'
        # print(response.text)

        total_words = self._get_total_word_count(response.text)
        self._total_words_in_file += len(total_words)
        self._get_word_list(total_words)
        self._total_word_list = self._total_word_list + total_words

    def file_reader(self):
        response_header = requests.head(self._url)
        # TODO(Ayush) check status 200
        self._file_size = int(response_header.headers['Content-Length'])

        part = ceil(self._file_size / self._chunk_size)

        range_start = 0
        range_end = self._chunk_size

        # with concurrent.futures.ThreadPoolExecutor(max_workers=part) as executor:
        #     executor.map(self._read_file, range(part+1))
        while part > 0:
            if part == 1:
                range_end = self._file_size
            headers = {"Range": "bytes=" + str(range_start) + "-" + str(range_end)}
            x = threading.Thread(target=self._read_file, args=(headers,))
            x.start()
            range_start = range_end + 1
            range_end = range_end + self._chunk_size
            part -= 1

        # TODO(Ayush) improving this
        while threading.active_count() != 1:
            # threading.current_thread().join()
            time.sleep(20)                          # temporary solution, will fix it today
            # print("active thread", threading.active_count())

        print("total words in file: ", self._total_words_in_file)
        self._top_5(self._total_word_list)


if __name__ == '__main__':
    FileReader().file_reader()
