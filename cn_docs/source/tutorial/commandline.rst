.. _tutorial_commandline:

使用命令行从 PDF 中提取文本
*********************************************

Extract text from a PDF using the commandline

.. tab:: 中文

    pdfminer.six 有几种可以从命令行使用的工具。命令行工具面向偶尔想要从 pdf 中提取文本的用户。

    如果您想以编程方式使用 pdfminer.six，请查看高级或可组合界面。

.. tab:: 英文

    pdfminer.six has several tools that can be used from the command line. The command-line tools are aimed at users that occasionally want to extract text from a pdf.

    Take a look at the high-level or composable interface if you want to use pdfminer.six programmatically.

Examples
========

pdf2txt.py
----------

::

    $ pdf2txt.py example.pdf
    all the text from the pdf appears on the command line

.. tab:: 中文

    :ref:`api_pdf2txt` 工具可从 PDF 中提取所有文本。它使用布局分析和合理的默认值以合理的方式对文本进行排序和分组。

.. tab:: 英文

    The :ref:`api_pdf2txt` tool extracts all the text from a PDF. It uses layout analysis with sensible defaults to order and group the text in a sensible way.

dumppdf.py
----------

::

    $ dumppdf.py -a example.pdf
    <pdf><object id="1">
    ...
    </object>
    ...
    </pdf>

.. tab:: 中文

    :ref:`api_dumppdf` 工具可用于从 PDF 中提取内部结构。此工具主要用于调试目的，但对于使用 PDF 的任何人都很有用。

.. tab:: 英文

    The :ref:`api_dumppdf` tool can be used to extract the internal structure from a PDF. This tool is primarily for debugging purposes, but that can be useful to anybody working with PDF's.
