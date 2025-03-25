.. _faq:

FAQ
**************************

Frequently asked questions

为什么它被称为 pdfminer.six？
==============================

Why is it called pdfminer.six?

.. tab:: 中文

    pdfminer.six 是 `Euske 创建的原始 pdfminer <https://github.com/euske>`_ 的一个分支。  
    实际上，几乎所有的代码和架构都是由 Euske 创建的。  
    然而，在很长一段时间内，原始的 pdfminer 并不支持 Python 3。直到 2020 年，原始 pdfminer 仍然只支持 Python 2。  
    pdfminer.six 的最初目标是为其添加对 Python 3 的支持。这一目标通过 `six` 包实现。  
    `six` 包用于编写兼容 Python 2 和 Python 3 的代码，因此得名 pdfminer.six。

    自 2020 年起，pdfminer.six 停止了对 Python 2 的支持，因为 Python 2 已经 `终止维护 <https://www.python.org/doc/sunset-python-2/>`_。  
    尽管 .six 这一部分的名称已不再适用，我们仍保留该名称，以防止对现有用户造成破坏性变更。

    当前的标语“We fathom PDF”是 `对 six 的一种幽默致敬 <https://github.com/pdfminer/pdfminer.six/issues/197#issuecomment-655091942>`_。  
    “Fathom” 一词既表示对某事物的深刻理解，同时也是一个长度单位，等于六英尺。


.. tab:: 英文

    Pdfminer.six is a fork of the `original pdfminer created by Euske
    <https://github.com/euske>`_. Almost all of the code and architecture are in
    -fact created by Euske. But, for a long time, this original pdfminer did not
    support Python 3. Until 2020 the original pdfminer only supported Python 2.
    The original goal of pdfminer.six was to add support for Python 3. This was
    done with the `six` package. The `six` package helps to write code that is
    compatible with both Python 2 and Python 3. Hence, pdfminer.six.

    As of 2020, pdfminer.six dropped the support for Python 2 because it was
    `end-of-life <https://www.python.org/doc/sunset-python-2/>`_. While the .six
    part is no longer applicable, we kept the name to prevent breaking changes for
    existing users.

    The current punchline "We fathom PDF" is a `whimsical reference
    <https://github.com/pdfminer/pdfminer.six/issues/197#issuecomment-655091942>`_
    to the six. Fathom means both deeply understanding something, and a fathom is
    also equal to six feet.

pdfminer.six 与 pdfminer 的其他分支相比如何？
==========================================================

How does pdfminer.six compare to other forks of pdfminer?

.. tab:: 中文

    pdfminer.six 现在是一个独立的、由社区维护的 Python 库，用于从 PDF 中提取文本。  
    我们积极修复 bug（包括针对那些不严格遵循 PDF 参考规范的 PDF），添加新功能，并改进 pdfminer.six 的可用性。  
    正是这一社区的支持，使 pdfminer.six 与原始 pdfminer 的其他分支有所不同。  
    PDF 作为一种格式非常多样，存在无数偏离官方标准的情况。  
    支持所有 PDF 的唯一方法，就是拥有一个积极使用并改进 pdfminer 的社区。

    自 2020 年以来，原始的 pdfminer 已 `停止维护 <https://github.com/euske/pdfminer#pdfminer>`_，  
    如果你需要一个仍在维护的 pdfminer 版本，Euske 推荐使用 pdfminer.six。


.. tab:: 英文


    Pdfminer.six is now an independent and community-maintained package for
    extracting text from PDFs with Python. We actively fix bugs (also for PDFs
    that don't strictly follow the PDF Reference), add new features and improve
    the usability of pdfminer.six. This community separates pdfminer.six from the
    other forks of the original pdfminer. PDF as a format is very diverse and
    there are countless deviations from the official format. The only way to
    support all the PDFs out there is to have a community that actively uses and
    improves pdfminer.

    Since 2020, the original pdfminer is `dormant
    <https://github.com/euske/pdfminer#pdfminer>`_, and pdfminer.six is the fork
    which Euske recommends if you need an actively maintained version of pdfminer.

为什么文本输出中有 `(cid:x)` 值？
=====================================================

Why are there `(cid:x)` values in the textual output?

.. tab:: 中文

    pdfminer.six 最常见的问题之一是文本输出包含原始字符 ID `(cid:x)`。  
    这通常会让人感到困惑，因为 PDF 在查看器中显示正常，而来自同一 PDF 的其他文本可以正确提取。

    其根本原因在于，PDF 对每个字符有两种不同的表示方式。  
    每个字符都会映射到一个字形（glyph），该字形决定字符在 PDF 查看器中的显示方式。  
    同时，每个字符也会映射到一个 Unicode 值，该值用于复制和粘贴文本。  
    某些 PDF 的 Unicode 映射不完整，因此无法将字符转换为 Unicode。  
    在这些情况下，pdfminer.six 默认显示原始字符 ID `(cid:x)`。

    要快速测试 pdfminer.six 是否可以提取更好的文本，可以尝试从 PDF 查看器中复制文本并粘贴到文本编辑器。  
    如果结果是正确的文本，那么 pdfminer.six 也应该能够正确提取文本。  
    如果结果是乱码，那么 pdfminer.six 也无法将字符转换为 Unicode。

    参考资料：

    #. `第 5 章：文本，PDF 参考手册 1.7 <https://opensource.adobe.com/dc-acrobat-sdk-docs/pdflsdk/index.html#pdf-reference>`_
    #. `文本：PDF，维基百科 <https://en.wikipedia.org/wiki/PDF#Text>`_


.. tab:: 英文


    One of the most common issues with pdfminer.six is that the textual output
    contains raw character id's `(cid:x)`. This is often experienced as confusing
    because the text is shown fine in a PDF viewer and other text from the same
    PDF is extracted properly.

    The underlying problem is that a PDF has two different representations
    of each character. Each character is mapped to a glyph that determines
    how the character is shown in a PDF viewer. And each character is also
    mapped to its unicode value that is used when copy-pasting the character.
    Some PDF's have incomplete unicode mappings and therefore it is impossible
    to convert the character to unicode. In these cases pdfminer.six defaults
    to showing the raw character id `(cid:x)`

    A quick test to see if pdfminer.six should be able to do better is to
    copy-paste the text from a PDF viewer to a text editor. If the result
    is proper text, pdfminer.six should also be able to extract proper text.
    If the result is gibberish, pdfminer.six will also not be able to convert
    the characters to unicode.

    References: 

    #. `Chapter 5: Text, PDF Reference 1.7 <https://opensource.adobe.com/dc-acrobat-sdk-docs/pdflsdk/index.html#pdf-reference>`_
    #. `Text: PDF, Wikipedia <https://en.wikipedia.org/wiki/PDF#Text>`_
