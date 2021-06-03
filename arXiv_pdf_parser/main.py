from pdf_text_extraction import PdfParser
import os


def main(url, count):
    start_time = time.time()
    try:
        parser.pdf_pipeline(url, count)
    except Exception as e:
        print(e)
    end_time = time.time() - start_time
    print(f'----All time is %.5f seconds---- \n' % end_time)


if __name__ == "__main__":
    os.mkdir('output_data')
    URL_PDF = [r'https://arxiv.org/pdf/1909.11687.pdf', 'https://arxiv.org/pdf/2103.15691.pdf',
               'https://arxiv.org/pdf/1706.03762.pdf']
    parser = PdfParser()
    import time

    for COUNT, URL in enumerate(URL_PDF):
        main(URL, COUNT)
