"""Functions that can be used for the most common use-cases for pdfminer.six"""

import logging
import sys
from io import StringIO
from typing import Any, BinaryIO, Container, Iterator, Optional, cast

from pdfminer.converter import (
    HOCRConverter,
    HTMLConverter,
    PDFPageAggregator,
    TextConverter,
    XMLConverter,
)
from pdfminer.image import ImageWriter
from pdfminer.layout import LAParams, LTPage
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfexceptions import PDFValueError
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.utils import AnyIO, FileOrName, open_filename


def extract_text_to_fp(
    inf: BinaryIO,
    outfp: AnyIO,
    output_type: str = "text",
    codec: str = "utf-8",
    laparams: Optional[LAParams] = None,
    maxpages: int = 0,
    page_numbers: Optional[Container[int]] = None,
    password: str = "",
    scale: float = 1.0,
    rotation: int = 0,
    layoutmode: str = "normal",
    output_dir: Optional[str] = None,
    strip_control: bool = False,
    debug: bool = False,
    disable_caching: bool = False,
    **kwargs: Any,
) -> None:
    """
    解析 inf 文件中的文本并写入类似文件的 outfp 对象。

    接受多个可选参数，但默认值相对合理。需要注意的是：传入一个空的 LAParams 与传入 None 并不相同！

    :param inf: 读取 PDF 结构的类似文件的对象，例如文件处理器（使用内置 `open()` 函数）或 `BytesIO`。
    :param outfp: 用于写入文本的类似文件的对象。
    :param output_type: 可能的值包括 'text'、'xml'、'html'、'hocr'、'tag'，但只有 'text' 能正常工作。
    :param codec: 文本解码所使用的编解码器。
    :param laparams: 来自 pdfminer.layout 的 LAParams 对象，默认为 None，但可能导致布局错误。
    :param maxpages: 解析的最大页数。
    :param page_numbers: 需要处理的零索引页码列表。
    :param password: 对于加密的 PDF，解密所需的密码。
    :param scale: 缩放因子。
    :param rotation: 旋转因子。
    :param layoutmode: 布局模式，默认为 'normal'，详见 pdfminer.converter.HTMLConverter。
    :param output_dir: 若提供此参数，则创建一个 ImageWriter 用于提取的图像。
    :param strip_control: 是否去除控制字符。
    :param debug: 输出更详细的日志数据。
    :param disable_caching: 是否禁用缓存。
    :param other: 其他参数。
    :return: 无返回值，该方法直接作用于两个流对象。若需获取字符串，可使用 StringIO。

    |

    Parses text from inf-file and writes to outfp file-like object.

    Takes loads of optional arguments but the defaults are somewhat sane.
    Beware laparams: Including an empty LAParams is not the same as passing
    None!

    :param inf: a file-like object to read PDF structure from, such as a
        file handler (using the builtin `open()` function) or a `BytesIO`.
    :param outfp: a file-like object to write the text to.
    :param output_type: May be 'text', 'xml', 'html', 'hocr', 'tag'.
        Only 'text' works properly.
    :param codec: Text decoding codec
    :param laparams: An LAParams object from pdfminer.layout. Default is None
        but may not layout correctly.
    :param maxpages: How many pages to stop parsing after
    :param page_numbers: zero-indexed page numbers to operate on.
    :param password: For encrypted PDFs, the password to decrypt.
    :param scale: Scale factor
    :param rotation: Rotation factor
    :param layoutmode: Default is 'normal', see
        pdfminer.converter.HTMLConverter
    :param output_dir: If given, creates an ImageWriter for extracted images.
    :param strip_control: Does what it says on the tin
    :param debug: Output more logging data
    :param disable_caching: Does what it says on the tin
    :param other:
    :return: nothing, acting as it does on two streams. Use StringIO to get
        strings.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    imagewriter = None
    if output_dir:
        imagewriter = ImageWriter(output_dir)

    rsrcmgr = PDFResourceManager(caching=not disable_caching)
    device: Optional[PDFDevice] = None

    if output_type != "text" and outfp == sys.stdout:
        outfp = sys.stdout.buffer

    if output_type == "text":
        device = TextConverter(
            rsrcmgr,
            outfp,
            codec=codec,
            laparams=laparams,
            imagewriter=imagewriter,
        )

    elif output_type == "xml":
        device = XMLConverter(
            rsrcmgr,
            outfp,
            codec=codec,
            laparams=laparams,
            imagewriter=imagewriter,
            stripcontrol=strip_control,
        )

    elif output_type == "html":
        device = HTMLConverter(
            rsrcmgr,
            outfp,
            codec=codec,
            scale=scale,
            layoutmode=layoutmode,
            laparams=laparams,
            imagewriter=imagewriter,
        )

    elif output_type == "hocr":
        device = HOCRConverter(
            rsrcmgr,
            outfp,
            codec=codec,
            laparams=laparams,
            stripcontrol=strip_control,
        )

    elif output_type == "tag":
        # Binary I/O is required, but we have no good way to test it here.
        device = TagExtractor(rsrcmgr, cast(BinaryIO, outfp), codec=codec)

    else:
        msg = f"Output type can be text, html, xml or tag but is {output_type}"
        raise PDFValueError(msg)

    assert device is not None
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(
        inf,
        page_numbers,
        maxpages=maxpages,
        password=password,
        caching=not disable_caching,
    ):
        page.rotate = (page.rotate + rotation) % 360
        interpreter.process_page(page)

    device.close()


def extract_text(
    pdf_file: FileOrName,
    password: str = "",
    page_numbers: Optional[Container[int]] = None,
    maxpages: int = 0,
    caching: bool = True,
    codec: str = "utf-8",
    laparams: Optional[LAParams] = None,
) -> str:
    """
    解析并返回 PDF 文件中的文本。

    :param pdf_file: PDF 文件的文件路径或类似文件的对象。
    :param password: 对于加密的 PDF，解密所需的密码。
    :param page_numbers: 需要提取的零索引页码列表。
    :param maxpages: 解析的最大页数。
    :param caching: 是否缓存资源。
    :param codec: 文本解码所使用的编解码器。
    :param laparams: 来自 pdfminer.layout 的 LAParams 对象。如果为 None，则使用一些通常效果良好的默认设置。
    :return: 一个包含所有提取文本的字符串。

    |

    Parse and return the text contained in a PDF file.

    :param pdf_file: Either a file path or a file-like object for the PDF file
        to be worked on.
    :param password: For encrypted PDFs, the password to decrypt.
    :param page_numbers: List of zero-indexed page numbers to extract.
    :param maxpages: The maximum number of pages to parse
    :param caching: If resources should be cached
    :param codec: Text decoding codec
    :param laparams: An LAParams object from pdfminer.layout. If None, uses
        some default settings that often work well.
    :return: a string containing all of the text extracted.
    """
    if laparams is None:
        laparams = LAParams()

    with open_filename(pdf_file, "rb") as fp, StringIO() as output_string:
        fp = cast(BinaryIO, fp)  # we opened in binary mode
        rsrcmgr = PDFResourceManager(caching=caching)
        device = TextConverter(rsrcmgr, output_string, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.get_pages(
            fp,
            page_numbers,
            maxpages=maxpages,
            password=password,
            caching=caching,
        ):
            interpreter.process_page(page)

        return output_string.getvalue()


def extract_pages(
    pdf_file: FileOrName,
    password: str = "",
    page_numbers: Optional[Container[int]] = None,
    maxpages: int = 0,
    caching: bool = True,
    laparams: Optional[LAParams] = None,
) -> Iterator[LTPage]:
    """
    提取并生成 LTPage 对象。

    :param pdf_file: 需要处理的 PDF 文件，可以是文件路径或类似文件的对象。
    :param password: 对于加密的 PDF，解密所需的密码。
    :param page_numbers: 需要提取的零索引页码列表。
    :param maxpages: 要解析的最大页数。
    :param caching: 是否缓存资源。
    :param laparams: 来自 pdfminer.layout 的 LAParams 对象，若为 None，则使用默认设置（通常效果较好）。
    :return: 生成的 LTPage 对象。

    |

    Extract and yield LTPage objects

    :param pdf_file: Either a file path or a file-like object for the PDF file
        to be worked on.
    :param password: For encrypted PDFs, the password to decrypt.
    :param page_numbers: List of zero-indexed page numbers to extract.
    :param maxpages: The maximum number of pages to parse
    :param caching: If resources should be cached
    :param laparams: An LAParams object from pdfminer.layout. If None, uses
        some default settings that often work well.
    :return: LTPage objects
    """
    if laparams is None:
        laparams = LAParams()

    with open_filename(pdf_file, "rb") as fp:
        fp = cast(BinaryIO, fp)  # we opened in binary mode
        resource_manager = PDFResourceManager(caching=caching)
        device = PDFPageAggregator(resource_manager, laparams=laparams)
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.get_pages(
            fp,
            page_numbers,
            maxpages=maxpages,
            password=password,
            caching=caching,
        ):
            interpreter.process_page(page)
            layout = device.get_result()
            yield layout
