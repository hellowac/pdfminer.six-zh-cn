pdfminer.six
============

以下是翻译后的 Markdown 文本：  

---

[![持续集成](https://github.com/pdfminer/pdfminer.six/actions/workflows/actions.yml/badge.svg)](https://github.com/pdfminer/pdfminer.six/actions/workflows/actions.yml)  
[![PyPI 版本](https://img.shields.io/pypi/v/pdfminer.six.svg)](https://pypi.python.org/pypi/pdfminer.six/)  
[![Gitter 聊天室](https://badges.gitter.im/pdfminer-six/Lobby.svg)](https://gitter.im/pdfminer-six/Lobby?utm_source=badge&utm_medium)  

*我们深入理解 PDF*  

Pdfminer.six 是原始 PDFMiner 的一个由社区维护的分支。它是一个用于从 PDF 文档中提取信息的工具，专注于获取和分析文本数据。Pdfminer.six 直接从 PDF 的源代码中提取页面上的文本，同时也能获取文本的精确位置、字体或颜色等信息。  

它采用模块化设计，使得 pdfminer.six 的各个组件都可以轻松替换。你可以实现自己的解释器或渲染设备，利用 pdfminer.six 的强大功能进行文本分析之外的其他用途。  

完整文档请查阅 [Read the Docs](https://pdfminersix.readthedocs.io)。  

特性  
--------

- 完全用 Python 编写。  
- 解析、分析和转换 PDF 文档。  
- 以文本、图像、HTML 或 [hOCR](https://en.wikipedia.org/wiki/HOCR) 形式提取内容。  
- 支持 PDF-1.7 规范（基本完全支持）。  
- 支持 CJK 语言和竖排文字。  
- 支持多种字体类型（Type1、TrueType、Type3 和 CID）。  
- 支持提取图像（JPG、JBIG2、位图）。  
- 支持多种压缩格式（ASCIIHexDecode、ASCII85Decode、LZWDecode、FlateDecode、RunLengthDecode、CCITTFaxDecode）。  
- 支持 RC4 和 AES 加密。  
- 支持提取 AcroForm 交互式表单。  
- 支持提取目录（Table of contents）。  
- 支持提取标记内容（Tagged contents）。  
- 支持自动布局分析。  

如何使用
----------------

1. 安装 Python 3.8 或更新版本。  
2. 安装 pdfminer.six：  

   ```bash
   pip install pdfminer.six
   ```

3. （可选）安装额外依赖以支持提取图像：  

   ```bash
   pip install 'pdfminer.six[image]'
   ```

4. 使用命令行界面从 PDF 中提取文本：  

   ```bash
   pdf2txt.py example.pdf
   ```

5. 或者在 Python 代码中使用：  

   ```python
   from pdfminer.high_level import extract_text

   text = extract_text("example.pdf")
   print(text)
   ```

贡献
--------

请务必阅读 [贡献指南](https://github.com/pdfminer/pdfminer.six/blob/master/CONTRIBUTING.md)。  

致谢
--------

此存储库包含来自 `pyHanko` 的代码；原始许可证已包含在 [此处](/docs/licenses/LICENSE.pyHanko)。  
