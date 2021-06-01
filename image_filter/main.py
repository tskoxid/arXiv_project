import pytesseract
from PIL import ImageFile
from csv import reader
from image_scripts.classes import ImageClassification
import time
import tarfile
import os

PATH_TESSERACT_LINUX: str = r'/usr/bin/tesseract'
PATH_TESSERACT_LINUX: str = r'C:\Users\Artem\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
PATH_CORPUS: str = os.path.join('data', 'profane_corpus.csv')
pytesseract.pytesseract.tesseract_cmd = PATH_TESSERACT_LINUX
ImageFile.LOAD_TRUNCATED_IMAGES = True

tar = tarfile.open(os.path.join('data', 'models.tar.gz'))
tar.extractall("data/")
tar.close()

corpus_list: list = []
with open(PATH_CORPUS, 'r', encoding='utf8') as f:
    csv_reader = reader(f)
    for row in csv_reader:
        corpus_list.append(row[0])
corpus_set: set = set(corpus_list)


def main(url_image: str):
    start_time = time.time()
    new_examaple.pipline_filter(url_image)
    end_time = time.time() - start_time
    print(f'----%.3f seconds---- \n' % end_time)


if __name__ == '__main__':
    url_image_list = ['https://i.pinimg.com/564x/ff/12/c4/ff12c41417f4d15220628479754ede42.jpg',
                      'https://i.pinimg.com/564x/0b/76/24/0b7624609162e8336908df59231735c5.jpg',
                      'https://i.pinimg.com/564x/ef/25/22/ef2522bab80dc1f9291d1c159a346ce1.jpg',
                      'https://i.redd.it/pk7p8xa8hph11.jpg',
                      'https://i.imgur.com/0NLsRgl.jpg',
                      'https://i.redd.it/jlwxg2i4rbn11.jpg',
                      'https://i.imgur.com/iIFS0GW.jpg',
                      'https://i.imgur.com/all7awG.jpg',
                      'https://i.redd.it/0h10sajru6s11.jpg',
                      'https://i.redd.it/q4r1lnkom1k11.jpg',
                      'http://i.imgur.com/FvoPXwV.jpg',
                      'https://i.redd.it/easnunqwgri01.jpg',
                      'https://i.imgur.com/O3pq4dH.jpg',
                      'https://i.redd.it/c1r4p1au26t01.jpg',
                      'https://i.redd.it/sjrhm72wn1i11.jpg']

    new_examaple = ImageClassification(corpus_set, model_path=os.path.join('data', 'models'))

    for URL_IMAGE in url_image_list:
        main(URL_IMAGE)
