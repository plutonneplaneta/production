# generate_reports.py

from services.report_service import generate_stock_report, generate_transfer_report
from utils.file_utils import save_report_to_txt


def run_reports():
    # Генерация отчёта по остаткам
    stock_report = generate_stock_report()
    save_report_to_txt(stock_report, "stock_report.txt")
    print("✅ Отчёт по остаткам сохранён как 'stock_report.txt'")

    # Генерация отчёта по перемещениям
    transfer_report = generate_transfer_report()
    save_report_to_txt(transfer_report, "transfer_report.txt")
    print("✅ Отчёт по перемещениям сохранён как 'transfer_report.txt'")


if __name__ == "__main__":
    run_reports()