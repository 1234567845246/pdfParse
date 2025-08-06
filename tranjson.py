import json
import argparse
import os
from typing import Dict, List, Any

# 中文key到英文key的映射关系
KEY_MAPPING = {
    "序号": "number",
    "发音": "pronunciation",
    "音调": "tone",
    "单词": "word",
    "词性": "part_of_speech",
    "释义": "meaning",
    "笔记": "note"
    # 可以根据需要添加更多映射
}

def convert_keys(data: Any) -> Any:
    """
    递归转换数据中的key
    """
    if isinstance(data, dict):
        return {
            KEY_MAPPING.get(k, k): convert_keys(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [convert_keys(item) for item in data]
    else:
        return data

def process_json_file(input_path: str, output_path: str = None) -> None:
    """
    处理JSON文件，转换key并保存
    """
    # 如果未指定输出路径，在输入文件名后加上_en
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_en{ext}"

    try:
        # 读取JSON文件
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 转换key
        converted_data = convert_keys(data)

        # 保存转换后的数据
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(converted_data, f, ensure_ascii=False, indent=2)

        print(f"转换完成！输出文件：{output_path}")
        print(f"转换的字段映射关系：")
        for cn, en in KEY_MAPPING.items():
            print(f"  {cn} -> {en}")

    except json.JSONDecodeError:
        print(f"错误：{input_path} 不是有效的JSON文件")
    except Exception as e:
        print(f"处理文件时发生错误：{str(e)}")

def main():
    parser = argparse.ArgumentParser(description='JSON文件中文key转英文key工具')
    parser.add_argument('input', help='输入JSON文件路径')
    parser.add_argument('-o', '--output', help='输出JSON文件路径（可选）')
    
    args = parser.parse_args()
    process_json_file(args.input, args.output)

if __name__ == '__main__':
    main()
