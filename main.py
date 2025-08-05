import fitz  # PyMuPDF
import json
import csv

import argparse
import os
import xml.etree.ElementTree as ET
from typing import List, Dict

def extract_table_data(pdf_path: str) -> List[Dict]:
    """
    从PDF中提取表格数据
    """
    doc = fitz.open(pdf_path)
    all_tables = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        # 使用PyMuPDF的表格检测功能
        tables = page.find_tables()
        
        if not tables:
            continue
            
        for table in tables:
            # 获取表格的单元格数据
            cells = table.extract()
            headers = cells[0]  # 假设第一行是表头
            
            # 处理每一行数据
            for row in cells[1:]:
                row_dict = {}
                for i, cell in enumerate(row):
                    if i < len(headers):
                        header = str(headers[i]).strip()
                        value = str(cell).strip()
                        row_dict[header] = value
                if row_dict:  # 只添加非空行
                    all_tables.append(row_dict)
    
    doc.close()
    return all_tables

def save_as_json(data: List[Dict], output_path: str) -> None:
    """
    保存为JSON格式
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_as_csv(data: List[Dict], output_path: str) -> None:
    """
    保存为CSV格式
    """
    if not data:
        return
        
    fieldnames = list(data[0].keys())
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def save_as_xml(data: List[Dict], output_path: str) -> None:
    """
    保存为XML格式
    """
    root = ET.Element("tables")
    for row in data:
        row_elem = ET.SubElement(root, "row")
        for key, value in row.items():
            field = ET.SubElement(row_elem, "field", name=key)
            field.text = value
    
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)



def process_single_file(pdf_path: str, output_path: str, format: str) -> int:
    """
    处理单个PDF文件并保存结果
    返回提取的数据行数
    """
    table_data = extract_table_data(pdf_path)
    
    if not table_data:
        print(f"在文件 {pdf_path} 中未找到表格数据！")
        return 0
    
    if format == 'json':
        save_as_json(table_data, output_path)
    elif format == 'csv':
        save_as_csv(table_data, output_path)
    elif format == 'xml':
        save_as_xml(table_data, output_path)
    
    return len(table_data)

def main():
    parser = argparse.ArgumentParser(description='PDF表格数据提取工具')
    parser.add_argument('pdf_paths', nargs='+', help='PDF文件路径，可以指定多个文件')
    parser.add_argument('--format', choices=['json', 'csv', 'xml'], 
                       default='json', help='输出格式 (默认: json)')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--merge', action='store_true', 
                       help='是否合并所有输入文件的数据到一个输出文件')
    
    args = parser.parse_args()
    
    try:
        if args.merge:
            # 合并模式：将所有文件的数据合并到一个输出文件
            all_data = []
            for pdf_path in args.pdf_paths:
                data = extract_table_data(pdf_path)
                if data:
                    all_data.extend(data)
                else:
                    print(f"警告：在文件 {pdf_path} 中未找到表格数据")
            
            if not all_data:
                print("错误：所有文件中都未找到表格数据！")
                return
                
            # 确定合并输出路径
            if args.output:
                output_path = args.output
            else:
                # 使用第一个文件所在目录
                first_dir = os.path.dirname(args.pdf_paths[0])
                output_path = os.path.join(first_dir, f"merged_tables.{args.format}")
            
            # 保存合并数据
            if args.format == 'json':
                save_as_json(all_data, output_path)
            elif args.format == 'csv':
                save_as_csv(all_data, output_path)
            elif args.format == 'xml':
                save_as_xml(all_data, output_path)
                
            print(f"成功合并并提取 {len(all_data)} 行表格数据到 {output_path}")
            
        else:
            # 分别处理每个文件
            total_rows = 0
            for pdf_path in args.pdf_paths:
                if args.output and len(args.pdf_paths) > 1:
                    print("警告：当处理多个文件时，--output 参数将被忽略")
                
                # 为每个文件生成输出路径
                input_dir = os.path.dirname(pdf_path)
                base = os.path.splitext(os.path.basename(pdf_path))[0]
                output_path = os.path.join(input_dir, f"{base}_table.{args.format}")
                
                # 处理单个文件
                rows = process_single_file(pdf_path, output_path, args.format)
                if rows > 0:
                    print(f"成功从 {pdf_path} 提取 {rows} 行表格数据到 {output_path}")
                total_rows += rows
            
            if total_rows > 0:
                print(f"\n总共处理了 {len(args.pdf_paths)} 个文件，提取了 {total_rows} 行数据")
       
            
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main()
