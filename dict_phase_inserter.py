import os
import sys
import configparser


def load_code_table(code_table_path):
    """載入速成碼表"""
    try:
        codes_dict = {}
        with open(code_table_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    codes_dict[parts[0]] = parts[1]
        return codes_dict
    except Exception as e:
        print(f"錯誤: 載入碼表失敗: {str(e)}")
        return {}


def is_chinese_or_mixed(phrase):
    """檢查詞語是否包含中文字符"""
    for char in phrase:
        if "\u4e00" <= char <= "\u9fff":
            return True
    return False


def has_english_or_digits(phrase):
    """檢查詞語是否包含英文或數字字符"""
    for char in phrase:
        if char.isascii() and (char.isalpha() or char.isdigit()):
            return True
    return False


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


def process_phrase(phrase, code_dict):
    """處理完整詞組"""
    result = []
    for char in phrase:
        if char.strip():  # 忽略空白字符
            code = process_character(char, code_dict)
            result.append(code)
    return "".join(result)


def append_to_file(file_path, phrase, code_dict):
    """將詞語添加到檔案最後一行"""
    try:
        # 檢查詞語是否為空
        if not phrase.strip():
            print("警告: 請輸入詞語")
            return False

        # 檢查詞語類型
        # contains_chinese = is_chinese_or_mixed(phrase)
        mix_true = has_english_or_digits(phrase)

        # 準備要寫入的內容
        if mix_true:
            # 中英混合詞語，需要處理編碼
            code = process_phrase(phrase, code_dict)
            content = f"{phrase}\t{code}\n"
        else:
            # 純中文詞語，直接添加
            content = f"{phrase}\n"

        # 寫入檔案
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"錯誤: 寫入檔案失敗: {str(e)}")
        return False


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path="config.ini"):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """載入配置"""
        if os.path.exists(self.config_path):
            self.config.read(self.config_path, encoding="utf-8")
        else:
            print(f"錯誤: 找不到配置檔案 {self.config_path}")
            sys.exit(1)

    def get_code_table_path(self):
        """獲取碼表路徑"""
        try:
            return self.config.get("Paths", "CodeTablePath")
        except:
            print("錯誤: 配置檔案中找不到碼表路徑")
            sys.exit(1)

    def get_target_file_path(self):
        """獲取目標檔案路徑"""
        try:
            return self.config.get("Paths", "TargetFilePath")
        except:
            print("錯誤: 配置檔案中找不到目標檔案路徑")
            sys.exit(1)


def main():
    # 初始化配置
    config_manager = ConfigManager()
    code_table_path = config_manager.get_code_table_path()
    target_file_path = config_manager.get_target_file_path()

    # 檢查路徑是否有效
    if not os.path.exists(code_table_path):
        print(f"錯誤: 碼表路徑無效: {code_table_path}")
        sys.exit(1)

    if not os.path.exists(target_file_path):
        print(f"錯誤: 目標檔案路徑無效: {target_file_path}")
        sys.exit(1)

    # 載入碼表
    code_dict = load_code_table(code_table_path)
    print(f"已載入碼表，共 {len(code_dict)} 個詞條")
    print(f"目標檔案: {target_file_path}")

    # 主循環
    print("\n=== 詞語插入器 ===")
    print("輸入 'exit' 或 'quit' 退出程式")

    while True:
        # 讀取輸入
        phrase = input("\n請輸入詞語: ").strip()

        # 檢查是否退出
        if phrase.lower() in ["exit", "quit"]:
            print("程式已退出")
            break

        # 檢查輸入是否為空
        if not phrase:
            print("警告: 請輸入詞語")
            continue

        # 添加詞語到檔案
        if append_to_file(target_file_path, phrase, code_dict):
            print(f"成功: 詞語 '{phrase}' 已添加到檔案")
        else:
            print("錯誤: 添加詞語失敗")


if __name__ == "__main__":
    main()
