欢迎阅读 pdfminer.six 的文档！
****************************************

Welcome to pdfminer.six's documentation!

.. image:: https://travis-ci.org/pdfminer/pdfminer.six.svg?branch=master
    :target: https://travis-ci.org/pdfminer/pdfminer.six
    :alt: Travis-ci build badge

.. image:: https://img.shields.io/pypi/v/pdfminer.six.svg
    :target: https://pypi.python.org/pypi/pdfminer.six/
    :alt: PyPi version badge

.. image:: https://badges.gitter.im/pdfminer-six/Lobby.svg
    :target: https://gitter.im/pdfminer-six/Lobby?utm_source=badge&utm_medium
    :alt: gitter badge

.. tab:: 中文

    我们理解 PDF。

    Pdfminer.six 是一个用于从 PDF 文档中提取信息的 Python 包。

    在 `github <https://github.com/pdfminer/pdfminer.six>`_ 上查看源代码。

.. tab:: 英文

    We fathom PDF.

    Pdfminer.six is a python package for extracting information from PDF documents.

    Check out the source on `github <https://github.com/pdfminer/pdfminer.six>`_.

内容
=======

Content

.. tab:: 中文

    本文档分为四个部分（根据 `Diátaxis 文档框架 <https://diataxis.fr>`_）。
    
    :ref:`tutorial` 部分可帮助您首次设置和使用 pdfminer.six。如果这是您第一次使用 pdfminer.six，请阅读此部分。
    
    :ref:`howto` 提供了解决常见问题的具体方法。
    
    如果您想要了解有关 pdfminer.six 内部工作原理的更多背景信息，请查看 :ref:`topic`。
    
    :ref:`reference` 为 pdfminer.six 中的所有常用类和函数提供了详细的 api 文档。

.. tab:: 英文

    This documentation is organized into four sections (according to the `Diátaxis
    documentation framework <https://diataxis.fr>`_). The
    :ref:`tutorial` section helps you setup and use pdfminer.six for the first
    time. Read this section if this is your first time working with pdfminer.six.
    The :ref:`howto` offers specific recipies for solving common problems.
    Take a look at the :ref:`topic` if you want more background information on
    how pdfminer.six works internally. The :ref:`reference` provides
    detailed api documentation for all the common classes and functions in
    pdfminer.six.

.. toctree::
    :maxdepth: 2

    tutorial/index
    howto/index
    topic/index
    reference/index
    faq


功能
========

Features

.. tab:: 中文

    * 将 PDF 文档中的所有对象解析为 Python 对象。
    * 以人类可读的方式分析和分组文本。
    * 提取文本、图像（JPG、JBIG2 和位图）、目录、标记内容等。
    * 支持 PDF-1.7 规范中的（几乎所有）功能
    * 支持中文、日文和韩文（CJK）语言以及垂直书写。
    * 支持各种字体类型（Type1、TrueType、Type3 和 CID）。
    * 支持 RC4 和 AES 加密。
    * 支持 AcroForm 交互式表单提取。

.. tab:: 英文

    * Parse all objects from a PDF document into Python objects.
    * Analyze and group text in a human-readable way.
    * Extract text, images (JPG, JBIG2 and Bitmaps), table-of-contents, tagged contents and more.
    * Support for (almost all) features from the PDF-1.7 specification
    * Support for Chinese, Japanese and Korean CJK) languages as well as vertical writing.
    * Support for various font types (Type1, TrueType, Type3, and CID).
    * Support for RC4 and AES encryption.
    * Support for AcroForm interactive form extraction.


安装说明
=========================

Installation instructions

.. tab:: 中文

    * 安装 Python 3.8 或更新版本。
    * 安装 pdfminer.six。

    ::
        
        $ pip install pdfminer.six

    * （可选）安装用于提取图像的额外依赖项。

    ::
    
        $ pip install 'pdfminer.six[image]'

    * 使用命令行界面从 pdf 中提取文本。

    ::
    
        $ pdf2txt.py example.pdf

    * 或者与 Python 一起使用。

    .. code-block:: python

        from pdfminer.high_level import extract_text

        text = extract_text("example.pdf")
        print(text)

.. tab:: 英文

    * Install Python 3.8 or newer.
    * Install pdfminer.six.

    ::
        $ pip install pdfminer.six`

    * (Optionally) install extra dependencies for extracting images.

    ::
        $ pip install 'pdfminer.six[image]'`

    * Use the command-line interface to extract text from pdf.

    ::
        $ pdf2txt.py example.pdf`

    * Or use it with Python.

    .. code-block:: python

        from pdfminer.high_level import extract_text

        text = extract_text("example.pdf")
        print(text)



贡献
============

Contributing

.. tab:: 中文

    我们欢迎任何对 pdfminer.six 做出贡献的人！但在做任何事情之前，请先查看一下 `贡献指南 <https://github.com/pdfminer/pdfminer.six/blob/master/CONTRIBUTING.md>`_。

.. tab:: 英文

    We welcome any contributors to pdfminer.six! But, before doing anything, take
    a look at the `contribution guide
    <https://github.com/pdfminer/pdfminer.six/blob/master/CONTRIBUTING.md>`_.
