.. _tutorial_composable:

使用 Python 从 PDF 中提取文本 - 第 2 部分
*********************************************
Extract text from a PDF using Python - part 2

.. tab:: 中文

    命令行工具和高级 API 只是 pdfminer.six 组件常用组合的快捷方式。您可以使用这些组件根据自己的需要修改 pdfminer.six。

    例如，从 PDF 文件中提取文本并将其保存在 python 变量中::

        from io import StringIO

        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from pdfminer.pdfdocument import PDFDocument
        from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
        from pdfminer.pdfpage import PDFPage
        from pdfminer.pdfparser import PDFParser

        output_string = StringIO()
        with open('samples/simple1.pdf', 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        print(output_string.getvalue())

.. tab:: 英文

    The command line tools and the high-level API are just shortcuts for often
    used combinations of pdfminer.six components. You can use these components to
    modify pdfminer.six to your own needs.

    For example, to extract the text from a PDF file and save it in a python
    variable::

        from io import StringIO

        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from pdfminer.pdfdocument import PDFDocument
        from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
        from pdfminer.pdfpage import PDFPage
        from pdfminer.pdfparser import PDFParser

        output_string = StringIO()
        with open('samples/simple1.pdf', 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        print(output_string.getvalue())

