# utils/file_utils.py

def save_report_to_txt(lines, filename="report.txt"):
    """
    Сохраняет список строк в текстовый файл
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return False