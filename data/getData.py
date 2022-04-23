import requests
import gzip
import os


def get_wiki_answers_data(limit=None):
    url = r'http://knowitall.cs.washington.edu/oqa/data/wikianswers/'

    limit = 30370994 if not limit else limit  # all clusters if no limit specified

    for i in range(limit):
        name = 'part-' + str(i).zfill(5) + '.gz'
        r = requests.get(url + name)
        with open(f'./data/{name}', 'wb') as temp_gz:
            temp_gz.write(r.content)
        with gzip.open(f'./data/{name}', 'rb') as temp_gz:
            with open(f'./data/{name[:-2]}data', 'wb') as out_file:
                out_file.write(temp_gz.read())
        os.remove(f'./data/{name}')


def main():
    get_wiki_answers_data(limit=4)


if __name__ == '__main__':
    main()
