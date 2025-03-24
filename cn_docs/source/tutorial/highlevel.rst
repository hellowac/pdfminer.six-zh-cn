.. _tutorial_highlevel:

使用 Python 从 PDF 中提取文本
************************************

Extract text from a PDF using Python

.. tab:: 中文

    高级 API 可用于执行常见任务。

    从 PDF 中提取文本的最简单方法是使用 :ref:`api_extract_text`:

    .. doctest::

        >>> from pdfminer.high_level import extract_text
        >>> text = extract_text('samples/simple1.pdf')
        >>> print(repr(text))
        'Hello \n\nWorld\n\nHello \n\nWorld\n\nH e l l o  \n\nW o r l d\n\nH e l l o  \n\nW o r l d\n\n\x0c'
        >>> print(text)
        ... # doctest: +NORMALIZE_WHITESPACE
        Hello
        <BLANKLINE>
        World
        <BLANKLINE>
        Hello
        <BLANKLINE>
        World
        <BLANKLINE>
        H e l l o
        <BLANKLINE>
        W o r l d
        <BLANKLINE>
        H e l l o
        <BLANKLINE>
        W o r l d
        <BLANKLINE>


    从 PDF 读取文本并在命令行上打印:

    .. doctest::

        >>> from io import StringIO
        >>> from pdfminer.high_level import extract_text_to_fp
        >>> output_string = StringIO()
        >>> with open('samples/simple1.pdf', 'rb') as fin:
        ...     extract_text_to_fp(fin, output_string)
        >>> print(output_string.getvalue().strip())
        Hello WorldHello WorldHello WorldHello World

    或者将其转换为 html 并使用布局分析：

    .. doctest::

        >>> from io import StringIO
        >>> from pdfminer.high_level import extract_text_to_fp
        >>> from pdfminer.layout import LAParams
        >>> output_string = StringIO()
        >>> with open('samples/simple1.pdf', 'rb') as fin:
        ...     extract_text_to_fp(fin, output_string, laparams=LAParams(),
        ...                        output_type='html', codec=None)

.. tab:: 英文

    The high-level API can be used to do common tasks.

    The most simple way to extract text from a PDF is to use
    :ref:`api_extract_text`:

    .. doctest::

        >>> from pdfminer.high_level import extract_text
        >>> text = extract_text('samples/simple1.pdf')
        >>> print(repr(text))
        'Hello \n\nWorld\n\nHello \n\nWorld\n\nH e l l o  \n\nW o r l d\n\nH e l l o  \n\nW o r l d\n\n\x0c'
        >>> print(text)
        ... # doctest: +NORMALIZE_WHITESPACE
        Hello
        <BLANKLINE>
        World
        <BLANKLINE>
        Hello
        <BLANKLINE>
        World
        <BLANKLINE>
        H e l l o
        <BLANKLINE>
        W o r l d
        <BLANKLINE>
        H e l l o
        <BLANKLINE>
        W o r l d
        <BLANKLINE>


    To read text from a PDF and print it on the command line:

    .. doctest::

        >>> from io import StringIO
        >>> from pdfminer.high_level import extract_text_to_fp
        >>> output_string = StringIO()
        >>> with open('samples/simple1.pdf', 'rb') as fin:
        ...     extract_text_to_fp(fin, output_string)
        >>> print(output_string.getvalue().strip())
        Hello WorldHello WorldHello WorldHello World

    Or to convert it to html and use layout analysis:

    .. doctest::

        >>> from io import StringIO
        >>> from pdfminer.high_level import extract_text_to_fp
        >>> from pdfminer.layout import LAParams
        >>> output_string = StringIO()
        >>> with open('samples/simple1.pdf', 'rb') as fin:
        ...     extract_text_to_fp(fin, output_string, laparams=LAParams(),
        ...                        output_type='html', codec=None)
