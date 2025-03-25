.. _tutorial_extract_pages:

使用 Python 从 PDF 中提取元素
****************************************
Extract elements from a PDF using Python

.. tab:: 中文

    高级函数可用于实现常见任务。在本例中，我们可以使用 :ref:`api_extract_pages`：

    .. code-block:: python

        from pdfminer.high_level import extract_pages
        for page_layout in extract_pages("test.pdf"):
            for element in page_layout:
                print(element)


    每个 ``element`` 将是一个 ``LTTextBox``, ``LTFigure``, ``LTLine``, ``LTRect`` 或一个 ``LTImage`` 。其中一些可以进一步迭代，例如迭代 ``LTTextBox`` 将得到一个 ``LTTextLine``，而这些又可以迭代得到一个 ``LTChar``。请参阅此处的图表：:ref:`topic_pdf_to_text_layout`。

    假设我们想提取所有文本。我们可以这样做：

    .. code-block:: python

        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextContainer
        for page_layout in extract_pages("test.pdf"):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    print(element.get_text())

    或者，我们可以提取每个字符的字体名称或大小：

    .. code-block:: python

        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextContainer, LTChar
        for page_layout in extract_pages("test.pdf"):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        for character in text_line:
                            if isinstance(character, LTChar):
                                print(character.fontname)
                                print(character.size)

.. tab:: 英文

    The high level functions can be used to achieve common tasks. In this case,
    we can use :ref:`api_extract_pages`:

    .. code-block:: python

        from pdfminer.high_level import extract_pages
        for page_layout in extract_pages("test.pdf"):
            for element in page_layout:
                print(element)


    Each ``element`` will be an ``LTTextBox``, ``LTFigure``, ``LTLine``, ``LTRect``
    or an ``LTImage``. Some of these can be iterated further, for example iterating
    though an ``LTTextBox`` will give you an ``LTTextLine``, and these in turn can
    be iterated through to get an ``LTChar``. See the diagram here:
    :ref:`topic_pdf_to_text_layout`.

    Let's say we want to extract all of the text. We could do:

    .. code-block:: python

        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextContainer
        for page_layout in extract_pages("test.pdf"):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    print(element.get_text())

    Or, we could extract the fontname or size of each individual character:

    .. code-block:: python

        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextContainer, LTChar
        for page_layout in extract_pages("test.pdf"):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        for character in text_line:
                            if isinstance(character, LTChar):
                                print(character.fontname)
                                print(character.size)
