.. _install:

将 pdfminer.six 安装为 Python 包
****************************************

Install pdfminer.six as a Python package

.. tab:: 中文

    首次使用 pdfminer.six 时，您需要在 Python 环境中安装 Python
    包。

    本教程要求您的系统安装了可用的 Python 和 pip
    。如果您没有并且不知道如何安装，请查看 `The Hitchhiker's Guide to Python! <https://docs.python-guide.org/>`_。

.. tab:: 英文

    To use pdfminer.six for the first time, you need to install the Python
    package in your Python environment.

    This tutorial requires you to have a system with a working Python and pip
    installation. If you don't have one and don't know how to install it, take a
    look at `The Hitchhiker's Guide to Python! <https://docs.python-guide.org/>`_.

使用 pip 安装
=================

Install using pip

.. tab:: 中文

    在命令行上运行以下命令，将 pdfminer.six 安装为Python 包::

        pip install pdfminer.six

.. tab:: 英文

    Run the following command on the commandline to install pdfminer.six as a
    Python package::

        pip install pdfminer.six


测试 pdfminer.six 安装
==============================

Test pdfminer.six installation

.. tab:: 中文

    您可以通过在 Python 中导入 pdfminer.six 来测试其安装。

    从命令行打开交互式 Python 会话 import pdfminer.six::

        >>> import pdfminer
        >>> print(pdfminer.__version__) # doctest: +IGNORE_RESULT
        '<installed version>'

    现在您可以将 pdfminer.six 用作 Python 包。但 pdfminer.six 还附带了一些有用的命令行工具。要测试这些工具是否已正确安装，请在命令行上运行以下命令::

        $ pdf2txt.py --version
        pdfminer.six <installed version>

.. tab:: 英文

    You can test the pdfminer.six installation by importing it in Python.

    Open an interactive Python session from the commandline import pdfminer
    .six::

        >>> import pdfminer
        >>> print(pdfminer.__version__)  # doctest: +IGNORE_RESULT
        '<installed version>'

    Now you can use pdfminer.six as a Python package. But pdfminer.six also
    comes with a couple of useful commandline tools. To test if these tools are
    correctly installed, run the following on your commandline::

        $ pdf2txt.py --version
        pdfminer.six <installed version>
