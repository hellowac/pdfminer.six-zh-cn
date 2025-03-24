.. _toc_target_page:

如何解析 ToC 条目的目标页面
*********************************************
How to resolve the target page of ToC entries

.. tab:: 中文

    pdfminer.six 允许通过方法 :meth:`PDFDocument.get_outlines` 访问文档的目录（在 PDF 的内部结构中称为 "Outlines"）。  

    一个最小的示例如下：  

    .. code-block:: python

        from pathlib import Path
        from pdfminer.pdfparser import PDFParser, PDFSyntaxError
        from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines


        file_name = Path("...")

        with open(file_name, "rb") as fp:
            try:
                parser = PDFParser(fp)
                document = PDFDocument(parser)
                outlines = document.get_outlines()
                for (level, title, dest, a, se) in outlines:
                    ...  # 执行某些操作
            except PDFNoOutlines:
                print("未找到目录。")
            except PDFSyntaxError:
                print("PDF 文件损坏或不是 PDF 文件。")
            finally:
                parser.close()

    但是，每个目录项的不同字段代表什么含义呢？要回答这个问题，我们可以参考 `PDF 参考手册 <https://www.adobe.com/go/pdfreference/>`__ 的 *12.3.3 Document Outline* 章节：  

    * **Level** (:obj:`int`): 该条目所在的层级。例如，顶级条目的 `level` 值为 ``1``，其子条目的 `level` 值为 ``2``，依此类推。  

    * **Title** (:obj:`str`): 条目的名称，例如 `"1. Introduction"`。  

    * **Dest** (:obj:`Union[list, bytes]`, `可选`):  
        该字段用于指示条目目标对象（可以是页面或其他对象）。  
        如果 `Dest` 字段存在，则 `A` 字段不会出现。  
        具体的目标定义方式可参考 `PDF 参考手册 <https://www.adobe.com/go/pdfreference/>`__ 的 *12.3.2 Destinations* 章节。  

    * **A** (:obj:`pdfminer.pdftypes.PDFObjRef`, `可选`):  
        除了 `Dest`，还可以使用 `A` 字段来定义目标，该字段表示一个操作（Action）。  
        详细信息请参考 *12.6 Actions* 章节。  

    * **SE** (:obj:`pdfminer.pdftypes.PDFObjRef`, `可选`):  
        该字段指向条目对应的结构元素（Structure Element）。  
        详细信息请参考 *14.7.2 Structure Hierarchy* 章节。  
        需要注意的是，大多数 PDF 不会包含该字段，而是使用 `Dest` 或 `A` 代替。  

        遗憾的是，pdfminer.six 并不会直接提供目录项所指向的页面编号。  
        不过，了解了上述字段的含义后，我们可以自己实现一个目录项的页面号解析器：  

    .. code-block:: python

        from enum import Enum, auto
        from pathlib import Path
        from typing import Any, Optional
        from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
        from pdfminer.pdfpage import PDFPage, LITERAL_PAGE
        from pdfminer.pdfparser import PDFParser, PDFSyntaxError
        from pdfminer.pdftypes import PDFObjRef


        class PDFRefType(Enum):
            """PDF 引用类型。"""

            PDF_OBJ_REF = auto()
            DICTIONARY = auto()
            LIST = auto()
            NAMED_REF = auto()
            UNK = auto()  # 备用类型


        class RefPageNumberResolver:
            """PDF 引用到页码解析器。

            .. note::

                远程跳转（Remote Go-To Actions，见 `https://www.adobe.com/go/pdfreference/`__ 的 12.6.4.3 章节）
                不在本解析器的范围内。

            属性：
                document (:obj:`pdfminer.pdfdocument.PDFDocument`):  
                    包含引用的 PDF 文档。  
                objid_to_pagenum (:obj:`dict[int, int]`):  
                    从对象 ID 映射到所在的页码。  
            """

            def __init__(self, document: PDFDocument):
                self.document = document
                # obj_id -> page_number
                self.objid_to_pagenum: dict[int, int] = {
                    page.pageid: page_num
                    for page_num, page in enumerate(PDFPage.create_pages(document), 1)
                }

            @classmethod
            def get_ref_type(cls, ref: Any) -> PDFRefType:
                """获取 PDF 引用的类型。"""
                if isinstance(ref, PDFObjRef):
                    return PDFRefType.PDF_OBJ_REF
                elif isinstance(ref, dict) and "D" in ref:
                    return PDFRefType.DICTIONARY
                elif isinstance(ref, list) and any(isinstance(e, PDFObjRef) for e in ref):
                    return PDFRefType.LIST
                elif isinstance(ref, bytes):
                    return PDFRefType.NAMED_REF
                else:
                    return PDFRefType.UNK

            @classmethod
            def is_ref_page(cls, ref: Any) -> bool:
                """检查引用是否指向 `/Page` 类型的对象。

                参数：
                    ref (:obj:`Any`):  
                        PDF 引用。

                返回：
                    :obj:`bool`: 若引用指向页面，则返回 `True`，否则返回 `False`。
                """
                return isinstance(ref, dict) and "Type" in ref and ref["Type"] is LITERAL_PAGE

            def resolve(self, ref: Any) -> Optional[int]:
                """递归解析 PDF 引用到页码。

                参数：
                    ref (:obj:`Any`):  
                        PDF 引用。

                返回：
                    :obj:`Optional[int]`: 解析出的页码，或 `None`（如果无法解析）。
                """
                ref_type = self.get_ref_type(ref)

                if ref_type is PDFRefType.PDF_OBJ_REF and self.is_ref_page(ref.resolve()):
                    return self.objid_to_pagenum.get(ref.objid)
                elif ref_type is PDFRefType.PDF_OBJ_REF:
                    return self.resolve(ref.resolve())

                if ref_type is PDFRefType.DICTIONARY:
                    return self.resolve(ref["D"])

                if ref_type is PDFRefType.LIST:
                    return self.resolve(next(filter(lambda e: isinstance(e, PDFObjRef), ref)))

                if ref_type is PDFRefType.NAMED_REF:
                    return self.resolve(self.document.get_dest(ref))

                return None  # 无法解析

    类 :class:`PDFRefType` 只是一个辅助工具，用于分类引用类型。  
    
    由于一个引用可能指向另一个引用，因此在某些情况下，我们需要递归调用 :meth:`RefPageNumberResolver.resolve`，直到最终解析到 `Page` 对象。  
    
    然后，我们可以从 `RefPageNumberResolver.objid_to_pagenum` 这个字典中获取该对象对应的页码。  

    使用这个页码解析器，我们可以以可读格式打印 PDF 文档的目录：  

    .. code-block:: python

        def print_outlines(file: str) -> dict[int, int]:
            """格式化打印 PDF 文档的目录（ToC）。"""
            with open(file, "rb") as fp:
                try:
                    parser = PDFParser(fp)
                    document = PDFDocument(parser)

                    ref_pagenum_resolver = RefPageNumberResolver(document)

                    outlines = list(document.get_outlines())
                    if not outlines:
                        print("未找到目录。")
                    for (level, title, dest, a, se) in outlines:
                        if dest:
                            page_num = ref_pagenum_resolver.resolve(dest)
                        elif a:
                            page_num = ref_pagenum_resolver.resolve(a)
                        elif se:
                            page_num = ref_pagenum_resolver.resolve(se)
                        else:
                            page_num = None
        
                        leading_spaces = (level-1) * 4
                        fill_dots = 80 - len(title) - leading_spaces

                        print(
                            f"{' ' * leading_spaces}"
                            f"{title}",
                            f"{'.' * fill_dots}",
                            f"{page_num:>3}"
                        )
                except PDFNoOutlines:
                    print("未找到目录。")
                except PDFSyntaxError:
                    print("PDF 文件损坏或不是 PDF 文件。")


        if __name__ == "__main__":
            file_name = Path("...")
            print_outlines(file_name)


.. tab:: 英文


    pdfminer.six allows to access the Table of Contents (or "Outlines" as called in
    the PDF internal structure) of a document through the method
    :meth:`PDFDocument.get_outlines`.

    A minimal example would be:

    .. code-block:: python

        from pathlib import Path
        from pdfminer.pdfparser import PDFParser, PDFSyntaxError
        from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines


        file_name = Path("...")

        with open(file_name, "rb") as fp:
            try:
                parser = PDFParser(fp)
                document = PDFDocument(parser)
                outlines = document.get_outlines()
                for (level, title, dest, a, se) in outlines:
                    ...  # do something
            except PDFNoOutlines:
                print("No outlines found.")
            except PDFSyntaxError:
                print("Corrupted PDF or non-PDF file.")
            finally:
                parser.close()

    But what do the different fields of each outline entry mean? To answer this
    question we can refer to the section *12.3.3 Document Outline* of the
    `PDF Reference <https://www.adobe.com/go/pdfreference/>`__:

    * **Level** (:obj:`int`): This is, unsurprisingly, the level at which the entry
        is. Entries at the top level will have level ``1``. Entries nested within
        those ones (i.e., their children), will have level ``2``, and so on.
    * **Title** (:obj:`str`): Again, quite self-explanatory, this field contains the
        name of the entry. For example: "1. Introduction".
    * **Dest** (:obj:`Union[list, bytes]`, `optional`): This
        is where things start to get interesting. First thing to mention is that if a
        **Dest** entry is present, the **A** entry shall not be present. Both of them
        allow to specify the object the entry targets (this could be a page or any
        other object). Destinations can be specified in multiple ways. In order to not
        paraphrase what the
        `PDF Reference <https://www.adobe.com/go/pdfreference/>`__ states, we refer
        the reader to the chapter *12.3.2 Destinations* for more information on the
        topic.
    * **A** (:obj:`pdfminer.pdftypes.PDFObjRef`, `optional`): Alternatively to using
        a destination, the target of an entry can also be specified as an action.
        Again, actions can get somewhat complicated, so we refer the reader to the
        chapter *12.6 Actions* of the reference.
    * **SE** (:obj:`pdfminer.pdftypes.PDFObjRef`, `optional`): This field contains
        the structure element the entry points at. More information about structure
        elements can be found in the chapter *14.7.2 Structure Hierarchy*. It is worth
        mentioning that most PDFs will not include this field, using **Dest** or **A**
        instead, or if they do, they might still include a destination (**Dest**) to
        keep compatibility with PDF versions previous to 1.3.

        Unfortunately, pdfminer.six doesn't expose the page number that each of the
        entries targets. However, once we know what each of the fields above mean, we
        can implement a ToC-entry page number resolver ourselves:

    .. code-block:: python

        from enum import Enum, auto
        from pathlib import Path
        from typing import Any, Optional
        from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
        from pdfminer.pdfpage import PDFPage, LITERAL_PAGE
        from pdfminer.pdfparser import PDFParser, PDFSyntaxError
        from pdfminer.pdftypes import PDFObjRef


        class PDFRefType(Enum):
            """PDF reference type."""

            PDF_OBJ_REF = auto()
            DICTIONARY = auto()
            LIST = auto()
            NAMED_REF = auto()
            UNK = auto()  # fallback


        class RefPageNumberResolver:
            """PDF Reference to page number resolver.

            .. note::

                Remote Go-To Actions (see 12.6.4.3 in
                `https://www.adobe.com/go/pdfreference/`__)
                are out of the scope of this resolver.

            Attributes:
                document (:obj:`pdfminer.pdfdocument.PDFDocument`):
                    The document that contains the references.
                objid_to_pagenum (:obj:`dict[int, int]`):
                    Mapping from an object id to the number of the page that contains
                    that object.
            """

            def __init__(self, document: PDFDocument):
                self.document = document
                # obj_id -> page_number
                self.objid_to_pagenum: dict[int, int] = {
                    page.pageid: page_num
                    for page_num, page in enumerate(PDFPage.create_pages(document), 1)
                }

            @classmethod
            def get_ref_type(cls, ref: Any) -> PDFRefType:
                """Get the type of a PDF reference."""
                if isinstance(ref, PDFObjRef):
                    return PDFRefType.PDF_OBJ_REF
                elif isinstance(ref, dict) and "D" in ref:
                    return PDFRefType.DICTIONARY
                elif isinstance(ref, list) and any(isinstance(e, PDFObjRef) for e in ref):
                    return PDFRefType.LIST
                elif isinstance(ref, bytes):
                    return PDFRefType.NAMED_REF
                else:
                    return PDFRefType.UNK

            @classmethod
            def is_ref_page(cls, ref: Any) -> bool:
                """Check whether a reference is of type '/Page'.

                Args:
                    ref (:obj:`Any`):
                        The PDF reference.

                Returns:
                    :obj:`bool`: :obj:`True` if the reference references
                    a page, :obj:`False` otherwise.
                """
                return isinstance(ref, dict) and "Type" in ref and ref["Type"] is LITERAL_PAGE

            def resolve(self, ref: Any) -> Optional[int]:
                """Resolve a PDF reference to a page number recursively.

                Args:
                    ref (:obj:`Any`):
                        The PDF reference.

                Returns:
                    :obj:`Optional[int]`: The page number or :obj:`None`
                    if the reference could not be resolved (e.g., remote Go-To
                    Actions or malformed references).
                """
                ref_type = self.get_ref_type(ref)

                if ref_type is PDFRefType.PDF_OBJ_REF and self.is_ref_page(ref.resolve()):
                    return self.objid_to_pagenum.get(ref.objid)
                elif ref_type is PDFRefType.PDF_OBJ_REF:
                    return self.resolve(ref.resolve())

                if ref_type is PDFRefType.DICTIONARY:
                    return self.resolve(ref["D"])

                if ref_type is PDFRefType.LIST:
                    # Get the PDFObjRef in the list (usually first element).
                    return self.resolve(next(filter(lambda e: isinstance(e, PDFObjRef), ref)))

                if ref_type is PDFRefType.NAMED_REF:
                    return self.resolve(self.document.get_dest(ref))

                return None  # PDFRefType.UNK

    The class :class:`PDFRefType` is just a helper to categorize the type of
    reference we are dealing with. Due to the fact that a reference can point to
    another reference, in some cases we will have to recursively call
    :meth:`RefPageNumberResolver.resolve` until we finally reach a page object.
    Then, we can get the page number by accessing the dictionary
    :attr:`RefPageNumberResolver.objid_to_pagenum`, which maps the page object id to
    the page number.

    Using this page number resolver, we can for example print the Table of Contents
    of a document in a human-readable format with the following code:

    .. code-block:: python

        def print_outlines(file: str) -> dict[int, int]:
            """Pretty print the outlines (ToC) of a PDF document."""
            with open(file, "rb") as fp:
                try:
                    parser = PDFParser(fp)
                    document = PDFDocument(parser)

                    ref_pagenum_resolver = RefPageNumberResolver(document)

                    outlines = list(document.get_outlines())
                    if not outlines:
                        print("No outlines found.")
                    for (level, title, dest, a, se) in outlines:
                        if dest:
                            page_num = ref_pagenum_resolver.resolve(dest)
                        elif a:
                            page_num = ref_pagenum_resolver.resolve(a)
                        elif se:
                            page_num = ref_pagenum_resolver.resolve(se)
                        else:
                            page_num = None
        
                        # Calculate leading spaces and filling dots for formatting.
                        leading_spaces = (level-1) * 4
                        fill_dots = 80 - len(title) - leading_spaces

                        print(
                            f"{' ' * leading_spaces}"
                            f"{title}",
                            f"{'.' * fill_dots}",
                            f"{page_num:>3}"
                        )
                except PDFNoOutlines:
                    print("No outlines found.")
                except PDFSyntaxError:
                    print("Corrupted PDF or non-PDF file.")
                finally:
                    try:
                        parser.close()
                    except NameError:
                        pass  # nothing to do


        def main():
            file_name = Path("...")
            print_outlines(file_name)


        if __name__ == "__main__":
            main()
