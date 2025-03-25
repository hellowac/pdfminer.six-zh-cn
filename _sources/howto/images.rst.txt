.. _images:

如何从 PDF 中提取图像
********************************

How to extract images from a PDF

.. tab:: 中文

    在开始之前，请确保你已经 :ref:`安装了 pdfminer.six<install>`。其次，你需要一个包含图片的 PDF。如果你没有，可以下载 `这篇研究论文 <https://www.robots.ox.ac.uk/~vgg/publications/2012/parkhi12a/parkhi12a.pdf>`_，其中包含猫和狗的图片，并将其保存为 `example.pdf`::  

        $ curl https://www.robots.ox.ac.uk/~vgg/publications/2012/parkhi12a/parkhi12a.pdf --output example.pdf  

    然后运行 :ref:`pdf2txt<api_pdf2txt>` 命令::  

        $ pdf2txt.py example.pdf --output-dir cats-and-dogs  

    此命令会从 PDF 中提取所有图片，并将其保存到 `cats-and-dogs` 目录中。  


.. tab:: 英文

    Before you start, make sure you have :ref:`installed pdfminer.six<install>`. The second thing you need is a PDF with images. If you don't have one, you can download `this research paper <https://www.robots.ox.ac.uk/~vgg/publications/2012/parkhi12a/parkhi12a.pdf>`_ with images of cats and dogs and save it as `example.pdf`::

        $ curl https://www.robots.ox.ac.uk/~vgg/publications/2012/parkhi12a/parkhi12a.pdf --output example.pdf

    Then run the :ref:`pdf2txt<api_pdf2txt>` command::

        $ pdf2txt.py example.pdf --output-dir cats-and-dogs

    This command extracts all the images from the PDF and saves them into the `cats-and-dogs` directory.
