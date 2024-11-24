import pandas as pd


def load_code_table(code_table_path):
    """載入速成碼表"""
    df = pd.read_csv(code_table_path, encoding="utf-8", sep="\t")
    return dict(zip(df["word"], df["code"]))


def number_to_chinese(number):
    """將阿拉伯數字轉換為中文數字"""
    chinese_numbers = {
        "0": "零",
        "1": "一",
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九",
    }
    return chinese_numbers.get(str(number), number)


def process_character(char, code_dict):
    """處理單個字符"""
    if char.isascii() and char.isalnum():  # 英文字母和數字
        if char.isdigit():
            # 數字轉換成中文後查詢碼表
            chinese_num = number_to_chinese(char)
            return code_dict.get(chinese_num, char.lower())
        else:
            # 英文字母轉小寫
            return char.lower()
    else:
        # 中文字符查詢碼表
        return code_dict.get(char, char)


def process_phrase(phrase, code_dict):
    """處理完整詞組"""
    result = []
    for char in phrase:
        if char.strip():  # 忽略空白字符
            code = process_character(char, code_dict)
            result.append(code)
    return "".join(result)


def convert_file(input_txt_path, code_table_path, output_csv_path):
    """轉換整個文件"""
    # 載入碼表
    code_dict = load_code_table(code_table_path)

    # 處理結果存儲
    results = []

    # 讀取輸入文件
    with open(input_txt_path, "r", encoding="utf-8") as f:
        for line in f:
            phrase = line.strip()
            if phrase:  # 忽略空行
                try:
                    code = process_phrase(phrase, code_dict)
                    results.append({"phrase": phrase, "code": code})
                except Exception as e:
                    print(f"處理 '{phrase}' 時發生錯誤：{str(e)}")

    # 將結果保存為CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv_path, index=False, header=False, sep="\t", encoding="utf-8")
    return df


# 使用示例
if __name__ == "__main__":
    input_txt_path = r"C:\Users\JACK\AppData\Roaming\Rime\en_dicts\cn_en_source.txt"  # 輸入的txt文件路徑
    code_table_path = r"C:\Users\JACK\Downloads\quick5.dict.csv"  # 碼表文件路徑
    output_csv_path = "cn_en2.txt"  # 輸出的csv文件路徑

    result_df = convert_file(input_txt_path, code_table_path, output_csv_path)
    print(f"處理完成，結果已保存到 {output_csv_path}")
    print("\n前5行結果預覽：")
    print(result_df.head())
