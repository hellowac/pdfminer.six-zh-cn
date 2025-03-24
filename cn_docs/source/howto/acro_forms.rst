.. _acro_forms:

如何使用 PDFMiner 从 PDF 中提取 AcroForm 交互式表单字段
*************************************************************************

How to extract AcroForm interactive form fields from a PDF using PDFMiner

.. tab:: 中文

    在开始之前，请确保你已经 :ref:`安装了 pdfminer.six<install>`。  

    其次，你需要一个包含 AcroForms 的 PDF（通常在可填写表单或多选框的 PDF 文件中）。GitHub 仓库的 `samples/acroform` 目录下提供了一些示例。  

    目前仅支持 AcroForm 交互式表单，不支持 XFA 表单。  

    .. code-block:: python

        from pdfminer.pdfparser import PDFParser
        from pdfminer.pdfdocument import PDFDocument
        from pdfminer.pdftypes import resolve1
        from pdfminer.psparser import PSLiteral, PSKeyword
        from pdfminer.utils import decode_text    

        data = {}

        def decode_value(value):
            # 解码 PSLiteral 和 PSKeyword
            if isinstance(value, (PSLiteral, PSKeyword)):
                value = value.name

            # 解码字节数据
            if isinstance(value, bytes):
                value = decode_text(value)

            return value

        with open(file_path, 'rb') as fp:
            parser = PDFParser(fp)
            
            doc = PDFDocument(parser)
            res = resolve1(doc.catalog)

            if 'AcroForm' not in res:
                raise ValueError("未找到 AcroForm")

            fields = resolve1(doc.catalog['AcroForm'])['Fields']  # 可能需要进一步解析

            for f in fields:
                field = resolve1(f)
                name, values = field.get('T'), field.get('V')

                # 解码字段名称
                name = decode_text(name)

                # 解析间接对象
                values = resolve1(values)
                
                # 解码字段值
                if isinstance(values, list):
                    values = [decode_value(v) for v in values]
                else:
                    values = decode_value(values)

                data.update({name: values})    

                print(name, values)

    此代码片段会打印所有字段的名称和值，并将它们保存在 `data` 字典中。  

    工作原理：  

    - 初始化解析器和 `PDFDocument` 对象  

    .. code-block:: python

        parser = PDFParser(fp)
        doc = PDFDocument(parser)

    - 获取 `Catalog` （目录）  

    (`Catalog` 目录包含对其他对象的引用，这些对象定义了文档结构，详见 PDF 32000-1:2008 规范第 7.7.2 节：  
    https://opensource.adobe.com/dc-acrobat-sdk-docs/pdflsdk/index.html#pdf-reference)  

    .. code-block:: python

        res = resolve1(doc.catalog)

    - 检查 `Catalog` 是否包含 `AcroForm` 关键字，如果没有，则抛出 `ValueError`  

    (如果 `Catalog` 中缺少 `AcroForm` 关键字，则 PDF 文件不包含 AcroForm 类型的交互式表单，详见 PDF 32000-1:2008 规范第 12.7.2 节)  

    .. code-block:: python

        if 'AcroForm' not in res:
            raise ValueError("未找到 AcroForm")

    - 解析 `Catalog` 中的 `AcroForm` 条目，并获取字段列表  

    .. code-block:: python

        fields = resolve1(doc.catalog['AcroForm'])['Fields']
        for f in fields:
            field = resolve1(f)

    - 获取字段名称和字段值  

    .. code-block:: python

        name, values = field.get('T'), field.get('V')

    - 解码字段名称  

    .. code-block:: python

        name = decode_text(name)

    - 解析间接字段值对象  

    .. code-block:: python

        values = resolve1(values)

    - 视情况调用值解码方法  

    (某些字段可能包含多个值，例如，组合框（Combo Box）可能同时包含多个选项值)  

    .. code-block:: python

        if isinstance(values, list):
            values = [decode_value(v) for v in values]
        else:
            values = decode_value(values)

    (`decode_value` 方法会自动解码字段值，并返回字符串)  

    - 解码 `PSLiteral` 和 `PSKeyword` 字段值  

    .. code-block:: python

        if isinstance(value, (PSLiteral, PSKeyword)):
            value = value.name

    - 解码字节类型字段值  

    .. code-block:: python

        if isinstance(value, bytes):
            value = utils.decode_text(value)

.. tab:: 英文

    Before you start, make sure you have :ref:`installed pdfminer.six<install>`.

    The second thing you need is a PDF with AcroForms (as found in PDF files with fillable forms or multiple choices). There are some examples of these in the GitHub repository under `samples/acroform`.

    Only AcroForm interactive forms are supported, XFA forms are not supported.

    .. code-block:: python

        from pdfminer.pdfparser import PDFParser
        from pdfminer.pdfdocument import PDFDocument
        from pdfminer.pdftypes import resolve1
        from pdfminer.psparser import PSLiteral, PSKeyword
        from pdfminer.utils import decode_text    
        
        
        data = {}
    
    
        def decode_value(value):

            # decode PSLiteral, PSKeyword
            if isinstance(value, (PSLiteral, PSKeyword)):
                value = value.name

            # decode bytes
            if isinstance(value, bytes):
                value = decode_text(value)

            return value


        with open(file_path, 'rb') as fp:
            parser = PDFParser(fp)
            
            doc = PDFDocument(parser)
            res = resolve1(doc.catalog)

            if 'AcroForm' not in res:
                raise ValueError("No AcroForm Found")
                
            fields = resolve1(doc.catalog['AcroForm'])['Fields']  # may need further resolving

            for f in fields:
                field = resolve1(f)
                name, values = field.get('T'), field.get('V')

                # decode name
                name = decode_text(name)

                # resolve indirect obj
                values = resolve1(values)
                
                # decode value(s)
                if isinstance(values, list):
                    values = [decode_value(v) for v in values]
                else:
                    values = decode_value(values)

                data.update({name: values})    
                
                print(name, values)

    This code snippet will print all the fields' names and values and save them in the "data" dictionary.


    How it works:

    - Initialize the parser and the PDFDocument objects

    .. code-block:: python

        parser = PDFParser(fp)
        doc = PDFDocument(parser)

    - Get the Catalog

    (the catalog contains references to other objects defining the document structure, see section 7.7.2 of PDF 32000-1:2008 specs: https://opensource.adobe.com/dc-acrobat-sdk-docs/pdflsdk/index.html#pdf-reference)

    .. code-block:: python

        res = resolve1(doc.catalog)

    - Check if the catalog contains the AcroForm key and raise ValueError if not 

    (the PDF does not contain Acroform type of interactive forms if this key is missing in the catalog, see section 12.7.2 of PDF 32000-1:2008 specs)

    .. code-block:: python

        if 'AcroForm' not in res:
            raise ValueError("No AcroForm Found")

    - Get the field list resolving the entry in the catalog

    .. code-block:: python

        fields = resolve1(doc.catalog['AcroForm'])['Fields']
        for f in fields:
            field = resolve1(f)

    - Get field name and field value(s)

    .. code-block:: python

        name, values = field.get('T'), field.get('V')

    - Decode field name.

    .. code-block:: python

        name = decode_text(name)

    - Resolve indirect field value objects

    .. code-block:: python

        values = resolve1(value)

    - Call the value(s) decoding method as needed

    (a single field can hold multiple values, for example, a combo box can hold more than one value at a time)

    .. code-block:: python

        if isinstance(values, list):
            values = [decode_value(v) for v in values]
        else:
            values = decode_value(values)
            
    (the decode_value method takes care of decoding the field's value, returning a string)

    - Decode PSLiteral and PSKeyword field values

    .. code-block:: python

        if isinstance(value, (PSLiteral, PSKeyword)):
            value = value.name

    - Decode bytes field values

    .. code-block:: python

        if isinstance(value, bytes):
            value = utils.decode_text(value)
