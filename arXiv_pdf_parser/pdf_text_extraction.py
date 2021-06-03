from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import io
import os
import re
import requests
import json


class PdfParser:

    def __init__(self, password='', maxpages: int = 0, caching: bool = True):
        self.password = password
        self.maxpages = maxpages
        self.caching = caching
        self.pagenos = set()

    @staticmethod
    def download_pdf(url_pdf: str):
        file = requests.get(url_pdf, stream=True)
        text_bytes = io.BytesIO(file.content)
        return text_bytes

    def convert_pdf_to_txt(self, file):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.get_pages(file, self.pagenos, maxpages=self.maxpages, password=self.password,
                                      caching=self.caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()
        device.close()
        retstr.close()
        return text

    @staticmethod
    def search_introduction(input_string: str):
        re_search = re.search(r'(Introduction|INTRODUCTION) ?\n(.*\n)+\n2\.? ', input_string)
        return re_search

    @staticmethod
    def search_main_text(input_string: str):
        re_search = re.search(r'(.*\n)+\n\d\\?\.? ?(Conclusion|CONCLUSION)', input_string)
        return re_search

    @staticmethod
    def search_conclusion(input_string: str):
        re_search = re.search(r'(Conclusion|CONCLUSION)(.*\n)+\n.*(References|REFERENCES)', input_string)
        return re_search

    @staticmethod
    def search_related_works(input_string: str):
        re_search = re.search(r'(Related Work|RELATED WORK)(.*\n)+\n3\.? ?[A-z]', input_string)
        return re_search

    def extract_parts(self, input_string: str):
        dict_text = {}

        try:
            text_introduction = self.search_introduction(input_string)
            dict_text['Introduction'] = text_introduction.group(0)
            input_string = input_string[text_introduction.end() - 3:]
        except AttributeError:
            dict_text['Introduction'] = ''
            print("Doesn't find any Introduction")

        try:
            text_related_works = self.search_related_works(input_string)
            dict_text['Related_Works'] = text_related_works.group(0)[:text_related_works.end() - 3]
            input_string = input_string[text_related_works.end() - 3:].replace('.', '\.').replace('[', '\[')
        except AttributeError:
            dict_text['Related_Works'] = ''
            print("Doesn't find any Related Works")

        try:
            text_main = self.search_main_text(input_string)
            dict_text['Main'] = text_main.group(0)
            input_string = input_string[text_main.end() - 13:]
        except AttributeError:
            dict_text['Main'] = ''
            print("Doesn't find any Main Text")

        try:
            text_conclusion = self.search_conclusion(input_string)
            dict_text['Conclusion'] = text_conclusion.group(0)[:-11]
        except AttributeError:
            dict_text['Conclusion'] = ''
            print("Doesn't find any Conclusion in article")

        return dict_text

    @staticmethod
    def sub_text(input_string: str):
        text_preproc = re.sub(r'\[.*]', '', input_string)
        text_preproc = re.sub(r'\[.*\n.*]', '', text_preproc)
        text_preproc = re.sub(r'arXiv.*\d{4}', '', text_preproc)
        text_preproc = re.sub(r'\n\d{1,3}\n\n', '\n', text_preproc)
        text_preproc = re.sub(r'(\(cid:\d*\))', '', text_preproc)
        text_preproc = re.sub('^ ', '', text_preproc)
        return text_preproc

    def preprocessing_text(self, text_raw: str):
        text_preproc = text_raw.replace('-\n', '').replace('ﬁ', 'fi').replace('', '').replace('', '')
        text_preproc = text_preproc.replace('ﬂ', 'fl').replace('ﬀ', 'ff')
        text_preproc = text_preproc.replace(' .', '.').replace(' ,', ',')
        text_preproc = self.sub_text(text_preproc)
        text_preproc = re.split('\n\n', text_preproc)
        text_output = ''
        list_text = []
        for i, paragraph in enumerate(text_preproc):
            if len(paragraph) < 3:
                continue
            if not paragraph[0].isalnum():
                list_text.append(paragraph)
                continue

        for element in list_text:
            text_preproc.remove(element)

        for paragraph in text_preproc:
            rows = paragraph.split('\n')
            text_row = ''
            for row in rows:
                text_row += row + ' '
            text_output += text_row + '\n\n'

        return text_output

    def postprocessing_text(self, text_raw: str):
        text_raw = self.preprocessing_text(text_raw)
        text_raw = text_raw.replace('\n\n', ' ')
        return text_raw

    @staticmethod
    def text_to_file(data: str, count: int):
        with io.open(os.path.join('output_data/', f'file_{count}.txt'), 'w', encoding='utf8') as file:
            file.write(data)
            file.close()

    @staticmethod
    def dict_to_json(dict_article: dict, count: int):
        with open(os.path.join('output_data/', f"file_{count}.json"), "w") as outfile:
            json.dump(dict_article, outfile)

    def pdf_pipeline(self, url: str, count: int):
        file = self.download_pdf(url)
        text_raw = self.convert_pdf_to_txt(file)
        self.text_to_file(text_raw, count)
        split_paper = self.extract_parts(text_raw)
        for key, value in split_paper.items():
            split_paper.update({key: self.postprocessing_text(value)})
        self.dict_to_json(split_paper, count)
