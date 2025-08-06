# PDF表格数据提取工具

这是一个基于Python和PyMuPDF库开发的PDF表格数据提取工具，可以自动识别和提取PDF文件中的表格数据，并支持多种输出格式。

## 功能特点

- 支持批量处理多个PDF文件
- 自动识别PDF中的表格结构
- 支持多种输出格式（JSON、CSV、XML）
- 可选择合并或独立输出模式
- 自动在输入文件目录生成输出文件

## 安装依赖

```bash
pip install PyMuPDF
```

## 使用方法

### 基本用法

1. 处理单个PDF文件（默认输出JSON）：
```bash
python main.py "input.pdf"
```

2. 指定输出格式：
```bash
python main.py "input.pdf" --format csv
```

3. 指定输出路径（仅在处理单个文件或合并模式时有效）：
```bash
python main.py "input.pdf" --format xml --output "output.xml"
```

### 批量处理

1. 处理多个文件（分别输出）：
```bash
python main.py "file1.pdf" "file2.pdf" "file3.pdf" --format csv
```

2. 合并多个文件数据到指定输出路径：
```bash
python main.py "file1.pdf" "file2.pdf" "file3.pdf" --format json --merge --output "result.xml"
```

## 参数说明

- `pdf_paths`：PDF文件路径，可以指定一个或多个文件
- `--format`：输出格式，可选值：
  - `json`（默认）：输出为JSON格式
  - `csv`：输出为CSV格式
  - `xml`：输出为XML格式
- `--output`：指定输出文件路径（可选）
- `--merge`：合并模式，将多个PDF的数据合并到一个输出文件

## 输出格式示例

### JSON格式
```json
[
  {
    "列1": "值1",
    "列2": "值2"
  },
  {
    "列1": "值3",
    "列2": "值4"
  }
]
```

### CSV格式
```csv
列1,列2
值1,值2
值3,值4
```

### XML格式
```xml
<?xml version="1.0" encoding="utf-8"?>
<tables>
  <row>
    <field name="列1">值1</field>
    <field name="列2">值2</field>
  </row>
  <row>
    <field name="列1">值3</field>
    <field name="列2">值4</field>
  </row>
</tables>
```

## 输出文件命名规则

1. 单文件模式：
- 未指定输出路径时：`{输入文件名}_table.{格式}`
- 指定输出路径时：使用指定的路径

2. 多文件模式：
- 不合并时：为每个输入文件生成 `{输入文件名}_table.{格式}`
- 合并模式：生成 `merged_tables.{格式}`

## 注意事项

1. 处理多个文件时，如果使用`--output`参数：
   - 在非合并模式下会被忽略
   - 在合并模式下用作合并后的输出文件路径

2. 输出文件默认保存在输入文件的同一目录下

3. 如果输入文件中没有检测到表格，程序会给出提示信息

## 错误处理

- 程序会对各种可能的错误进行处理，并提供清晰的错误信息
- 在处理多个文件时，单个文件的失败不会影响其他文件的处理

## 依赖库版本

- Python >= 3.6
- PyMuPDF (fitz)

## JSON字段转换工具 (tranjson.py)

这是一个配套工具，用于将提取的JSON数据中的中文字段名转换为英文，使数据更适合国际化使用。

### 功能特点

- 自动将JSON文件中的中文key转换为对应的英文key
- 保持原有的数据结构和值不变
- 支持自定义输出路径
- 保持JSON格式化输出，便于阅读

### 字段映射关系

当前支持以下字段的自动转换：
- 序号 -> number
- 发音 -> pronunciation
- 音调 -> tone
- 单词 -> word
- 词性 -> part_of_speech
- 释义 -> meaning
- 笔记 -> note

### 使用方法

1. 基本使用（自动生成输出文件名）：
```bash
python tranjson.py "pdf/新标日初级下册.json"
```
将生成 `pdf/新标日初级下册_en.json`

2. 指定输出文件路径：
```bash
python tranjson.py "pdf/新标日初级下册.json" -o "output.json"
```

### 参数说明

- `input`：必需，输入JSON文件的路径
- `-o, --output`：可选，输出JSON文件的路径。如果不指定，将在原文件名后添加"_en"后缀

### 注意事项

1. 输入文件必须是有效的JSON格式
2. 如果遇到未在映射关系中定义的字段，将保持原样
3. 转换过程会保持JSON的格式化和缩进
4. 所有中文内容（值）保持不变，只转换字段名（key）
