import re


def process_text_file(input_filename, output_filename_match, output_filename_unmatch):
    """
    讀取輸入文字檔，將包含數字、英文字母或符號的行寫入一個檔案，
    將純中文的行寫入另一個檔案。

    Args:
        input_filename (str): 輸入文字檔的檔名
        output_filename_match (str): 包含數字、英文或符號的行的輸出檔名
        output_filename_unmatch (str): 純中文行的輸出檔名
    """
    # 用於匹配中文字符的正則表達式
    chinese_pattern = re.compile(r"^[\u4e00-\u9fff\s]+$")

    try:
        # 初始化計數器和儲存列表
        matched_lines = []
        unmatched_lines = []
        matched_count = 0
        unmatched_count = 0
        total_lines = 0

        # 讀取和處理檔案
        print("開始處理檔案...")
        with open(input_filename, "r", encoding="utf-8") as input_file:
            # 逐行讀取檔案
            for line in input_file:
                total_lines += 1
                # 去除行末換行符
                line = line.strip()

                # 跳過空行
                if not line:
                    continue

                # 檢查是否為純中文
                if chinese_pattern.match(line):
                    unmatched_lines.append(line + "\n")
                    unmatched_count += 1
                else:
                    matched_lines.append(line + "\n")
                    matched_count += 1

                # 每處理10000行顯示進度
                if total_lines % 10000 == 0:
                    print(f"已處理 {total_lines} 行...")

        # 寫入包含數字、英文或符號的行
        with open(output_filename_match, "w", encoding="utf-8") as output_file:
            output_file.writelines(matched_lines)

        # 寫入純中文的行
        with open(output_filename_unmatch, "w", encoding="utf-8") as output_file:
            output_file.writelines(unmatched_lines)

        # 輸出處理結果
        print("\n處理完成！")
        print(f"總共處理了 {total_lines} 行")
        print(f"包含數字、英文或符號的行數：{matched_count}")
        print(f"純中文行數：{unmatched_count}")
        print(f"包含數字、英文或符號的行已寫入：{output_filename_match}")
        print(f"純中文的行已寫入：{output_filename_unmatch}")

    except FileNotFoundError:
        print(f"錯誤：找不到輸入檔案 '{input_filename}'")
    except Exception as e:
        print(f"處理過程中發生錯誤：{str(e)}")


# 使用你提供的檔案路徑
# input_file = r"C:\Users\JACK\AppData\Roaming\Rime\cn_dicts\wiki.txt"
# output_file_match = "wiki_mix.txt"    # 包含數字、英文或符號的行
# output_file_unmatch = "wiki_cn.txt"   # 純中文的行
input_file = r"C:\Users\JACK\AppData\Roaming\Rime\cn_dicts\anime.dict.yaml"
output_file_match = "moe_mix.txt"  # 包含數字、英文或符號的行
output_file_unmatch = "moe_cn.txt"  # 純中文的行

# 執行處理
process_text_file(input_file, output_file_match, output_file_unmatch)
