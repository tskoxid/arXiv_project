## arXiv_pdf_parser
Parsing paragraphs from pdf.

### Input
На вход подается ссылка на pdf-file.

### Output
На выходе получает два файла:
1. Весь текст в формате .pdf
2. Json файл со структурой: {Introduction:, Related Works:, Main text:, Conclusion:}


## arXiv_info_receiving
Получение и занесение информации статей с arXiv.

На вход подается ссылка на статью, далее:
1. Проверяется есть ли данная статья в базе.
2. Если статьи нет, то добавляется неободимая информация.
3. Запрос шлется максимум раз в три секунды в соответствии с правилами api arXiv.
