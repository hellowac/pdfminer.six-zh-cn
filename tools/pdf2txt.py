#!/usr/bin/env python3
"""
.. tab:: 中文

    一个从 PDF 中提取文本和图像并将其输出为纯文本、html、xml 或标签的命令行工具。

.. tab:: 英文

    A command line tool for extracting text and images from PDF and
    output it to plain text, html, xml or tags.
"""

import argparse
import logging
import sys
from typing import Any, Container, Iterable, List, Optional

import pdfminer.high_level
from pdfminer.layout import LAParams
from pdfminer.pdfexceptions import PDFValueError
from pdfminer.utils import AnyIO

logging.basicConfig()

OUTPUT_TYPES = ((".htm", "html"), (".html", "html"), (".xml", "xml"), (".tag", "tag"))


def float_or_disabled(x: str) -> Optional[float]:
    if x.lower().strip() == "disabled":
        return None
    try:
        return float(x)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid float value: {x}")


def extract_text(
    files: Iterable[str] = [],
    outfile: str = "-",
    laparams: Optional[LAParams] = None,
    output_type: str = "text",
    codec: str = "utf-8",
    strip_control: bool = False,
    maxpages: int = 0,
    page_numbers: Optional[Container[int]] = None,
    password: str = "",
    scale: float = 1.0,
    rotation: int = 0,
    layoutmode: str = "normal",
    output_dir: Optional[str] = None,
    debug: bool = False,
    disable_caching: bool = False,
    **kwargs: Any,
) -> AnyIO:
    if not files:
        raise PDFValueError("Must provide files to work upon!")

    if output_type == "text" and outfile != "-":
        for override, alttype in OUTPUT_TYPES:
            if outfile.endswith(override):
                output_type = alttype

    if outfile == "-":
        outfp: AnyIO = sys.stdout
        if sys.stdout.encoding is not None:
            codec = "utf-8"
    else:
        outfp = open(outfile, "wb")

    for fname in files:
        with open(fname, "rb") as fp:
            pdfminer.high_level.extract_text_to_fp(fp, **locals())
    return outfp


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument(
        "files",
        type=str,
        default=None,
        nargs="+",
        help="一个或多个 PDF 文件的路径.",  # One or more paths to PDF files
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"pdfminer.six v{pdfminer.__version__}",
    )
    parser.add_argument(
        "--debug",
        "-d",
        default=False,
        action="store_true",
        help="使用调试日志记录级别.",  # Use debug logging level
    )
    parser.add_argument(
        "--disable-caching",
        "-C",
        default=False,
        action="store_true",
        help=".是否应禁用缓存或字体等资源",  # If caching or resources, such as fonts, should be disabled
    )

    parse_params = parser.add_argument_group(
        "解析器/Parser",
        description="""PDF 解析期间使用""",  # Used during PDF parsing
    )
    parse_params.add_argument(
        "--page-numbers",
        type=int,
        default=None,
        nargs="+",
        help="要解析的页码的空格分隔列表。",  # A space-seperated list of page numbers to parse.
    )
    parse_params.add_argument(
        "--pagenos",
        "-p",
        type=str,
        help="要解析的页码的逗号分隔列表。包含在旧版应用程序中，使用 --page-numbers 可获得更符合习惯的参数输入。",
        # "A comma-separated list of page numbers to parse. "
        # "Included for legacy applications, use --page-numbers "
        # "for more idiomatic argument entry.",
    )
    parse_params.add_argument(
        "--maxpages",
        "-m",
        type=int,
        default=0,
        help="解析的最大页面数.",  # The maximum number of pages to parse
    )
    parse_params.add_argument(
        "--password",
        "-P",
        type=str,
        default="",
        help=".用于解密 PDF 文件的密码",  # The password to use for decrypting PDF file
    )
    parse_params.add_argument(
        "--rotation",
        "-R",
        default=0,
        type=int,
        help="在进行其他类型的处理之前旋转 PDF 的度数。",
        # "The number of degrees to rotate the PDF "
        # "before other types of processing.",
    )

    la_params = LAParams()  # will be used for defaults
    la_param_group = parser.add_argument_group(
        "布局分析/Layout analysis",
        description="在布局分析期间使用",  # Used during layout analysis.
    )
    la_param_group.add_argument(
        "--no-laparams",
        "-n",
        default=False,
        action="store_true",
        help="是否应忽略布局分析参数.",  # If layout analysis parameters should be ignored
    )
    la_param_group.add_argument(
        "--detect-vertical",
        "-V",
        default=la_params.detect_vertical,
        action="store_true",
        help="在布局分析期间是否应考虑垂直文本",  # If vertical text should be considered during layout analysis
    )
    la_param_group.add_argument(
        "--line-overlap",
        type=float,
        default=la_params.line_overlap,
        help="如果两个字符的重叠部分大于此值，则认为它们在同一行。重叠部分是相对于两个字符的最小高度指定的。",
        # "If two characters have more overlap than this they "
        # "are considered to be on the same line. The overlap is specified "
        # "relative to the minimum height of both characters.",
    )
    la_param_group.add_argument(
        "--char-margin",
        "-M",
        type=float,
        default=la_params.char_margin,
        help="如果两个字符之间的距离小于此边距，则它们将被视为同一行的一部分。边距是相对于字符的宽度指定的。",
        # "If two characters are closer together than this margin they "
        # "are considered to be part of the same line. The margin is "
        # "specified relative to the width of the character.",
    )
    la_param_group.add_argument(
        "--word-margin",
        "-W",
        type=float,
        default=la_params.word_margin,
        help="如果同一行上的两个字符之间的距离大于此边距，则它们将被视为两个单独的单词，中间会添加一个空格以方便阅读。边距是相对于字符的宽度指定的。",
        # "If two characters on the same line are further apart than this "
        # "margin then they are considered to be two separate words, and "
        # "an intermediate space will be added for readability. The margin "
        # "is specified relative to the width of the character.",
    )
    la_param_group.add_argument(
        "--line-margin",
        "-L",
        type=float,
        default=la_params.line_margin,
        help="如果两行靠得很近，则认为它们是同一段落的一部分。边距是相对于行高指定的。",
        # "If two lines are close together they are considered to "
        # "be part of the same paragraph. The margin is specified "
        # "relative to the height of a line.",
    )
    la_param_group.add_argument(
        "--boxes-flow",
        "-F",
        type=float_or_disabled,
        default=la_params.boxes_flow,
        help="指定在确定行顺序时文本的水平和垂直位置有多重要。该值应在 -1.0（仅水平位置重要）到 +1.0（仅垂直位置重要）的范围内。您还可以传递“disabled”以禁用高级布局分析，而是根据文本框左下角的位置返回文本。",
        # "Specifies how much a horizontal and vertical position of a "
        # "text matters when determining the order of lines. The value "
        # "should be within the range of -1.0 (only horizontal position "
        # "matters) to +1.0 (only vertical position matters). You can also "
        # "pass `disabled` to disable advanced layout analysis, and "
        # "instead return text based on the position of the bottom left "
        # "corner of the text box.",
    )
    la_param_group.add_argument(
        "--all-texts",
        "-A",
        default=la_params.all_texts,
        action="store_true",
        help="是否应该对图中的文字进行布局分析",
        # "If layout analysis should be performed on text in figures.",
    )

    output_params = parser.add_argument_group(
        "输出/Output",
        description="在输出生成期间使用",  # Used during output generation.
    )
    output_params.add_argument(
        "--outfile",
        "-o",
        type=str,
        default="-",
        help="写入输出的文件路径。或者“-”（默认）写入标准输出。",
        # "Path to file where output is written. "
        # 'Or "-" (default) to write to stdout.',
    )
    output_params.add_argument(
        "--output_type",
        "-t",
        type=str,
        default="text",
        help="要生成的输出类型 {text,html,xml,tag}。",
        # "Type of output to generate {text,html,xml,tag}.",
    )
    output_params.add_argument(
        "--codec",
        "-c",
        type=str,
        default="utf-8",
        help="输出文件中使用的文本编码。",
        # "Text encoding to use in output file.",
    )
    output_params.add_argument(
        "--output-dir",
        "-O",
        default=None,
        help="放置提取图像的输出目录。如果没有指定，则不会提取图像。",
        # "The output directory to put extracted images in. If not given, "
        # "images are not extracted.",
    )
    output_params.add_argument(
        "--layoutmode",
        "-Y",
        default="normal",
        type=str,
        help="生成 html 时使用的布局类型 {normal、exact、loose}。如果是 normal，则每行在 html 中单独定位。如果是 exac，则每个字符在 html 中单独定位。如果是 loose，结果与 normal 相同，但每行文本后都有一个额外的换行符。仅在 output_type 为 html 时使用。",
        # "Type of layout to use when generating html "
        # "{normal,exact,loose}. If normal,each line is"
        # " positioned separately in the html. If exact"
        # ", each character is positioned separately in"
        # " the html. If loose, same result as normal "
        # "but with an additional newline after each "
        # "text line. Only used when output_type is html.",
    )
    output_params.add_argument(
        "--scale",
        "-s",
        type=float,
        default=1.0,
        help="生成 html 文件时使用的缩放量。仅当 output_type 为 html 时使用。",
        # "The amount of zoom to use when generating html file. "
        # "Only used when output_type is html.",
    )
    output_params.add_argument(
        "--strip-control",
        "-S",
        default=False,
        action="store_true",
        help="从文本中删除控制语句。仅当 output_type 为 xml 时使用",
        # "Remove control statement from text. Only used when output_type is xml.",
    )

    return parser


def parse_args(args: Optional[List[str]]) -> argparse.Namespace:
    parsed_args = create_parser().parse_args(args=args)

    # Propagate parsed layout parameters to LAParams object
    if parsed_args.no_laparams:
        parsed_args.laparams = None
    else:
        parsed_args.laparams = LAParams(
            line_overlap=parsed_args.line_overlap,
            char_margin=parsed_args.char_margin,
            line_margin=parsed_args.line_margin,
            word_margin=parsed_args.word_margin,
            boxes_flow=parsed_args.boxes_flow,
            detect_vertical=parsed_args.detect_vertical,
            all_texts=parsed_args.all_texts,
        )

    if parsed_args.page_numbers:
        parsed_args.page_numbers = {x - 1 for x in parsed_args.page_numbers}

    if parsed_args.pagenos:
        parsed_args.page_numbers = {int(x) - 1 for x in parsed_args.pagenos.split(",")}

    if parsed_args.output_type == "text" and parsed_args.outfile != "-":
        for override, alttype in OUTPUT_TYPES:
            if parsed_args.outfile.endswith(override):
                parsed_args.output_type = alttype

    return parsed_args


def main(args: Optional[List[str]] = None) -> int:
    parsed_args = parse_args(args)
    outfp = extract_text(**vars(parsed_args))
    outfp.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
