# Задание 1
import argparse
import csv
import sys
import xlsxwriter


def parse_value(value: str):
    """Преобразует строку в int, float или оставляет str."""
    val_clean = value.strip()
    if not val_clean:
        return ""

    # Пробуем преобразовать в целое число
    try:
        return int(val_clean)
    except ValueError:
        pass

    # Пробуем преобразовать в число с плавающей точкой
    try:
        return float(val_clean.replace(",", "."))
    except ValueError:
        pass

    # Если не число, возвращаем исходную строку
    return val_clean


def convert_csv_to_xlsx(input_file, output_file, delimiter=","):
    try:
        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet()

        with open(input_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=delimiter)

            for row_idx, row in enumerate(reader):
                for col_idx, value in enumerate(row):
                    parsed_val = parse_value(value)

                    if isinstance(parsed_val, (int, float)):
                        worksheet.write_number(row_idx, col_idx, parsed_val)
                    else:
                        worksheet.write_string(row_idx, col_idx, parsed_val)

        workbook.close()
        print(f"Файл успешно сконвертирован: {output_file}")

    except Exception as e:
        print(f"Ошибка при конвертации: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Конвертер из CSV в XLSX формат."
    )
    parser.add_argument("input", help="Имя входного CSV файла")
    parser.add_argument("output", help="Имя выходного XLSX файла")
    parser.add_argument(
        "-d",
        "--delimiter",
        default=",",
        help='Разделитель в CSV файле (по умолчанию ",")',
    )

    args = parser.parse_args()
    convert_csv_to_xlsx(args.input, args.output, args.delimiter)


if __name__ == "__main__":
    main()
# Задание 2
#import csv
# from collections import defaultdict
# import xlsxwriter
#
#
# def analyze_grades(input_csv, output_xlsx):
#     groups_data = defaultdict(list)
#
#     # 1. Считывание данных из test_table.csv (разделитель запятая)
#     with open(input_csv, mode="r", encoding="utf-8") as f:
#         reader = csv.reader(f, delimiter=",")
#         for row in reader:
#             if not row or len(row) < 2:
#                 continue
#             # Структура строки: Группа, ФИО, Задание 1, ..., Задание 7
#             group = row[0].strip()
#             groups_data[group].append(row)
#
#     num_tasks = 7  # В файле test_table.csv ровно 7 заданий
#     task_headers = [f"Задание {i}" for i in range(1, num_tasks + 1)]
#
#     workbook = xlsxwriter.Workbook(output_xlsx)
#
#     # Оформление ячеек
#     header_format = workbook.add_format(
#         {"bold": True, "bg_color": "#D9E1F2", "border": 1, "align": "center"}
#     )
#     cell_format = workbook.add_format({"border": 1, "align": "left"})
#     num_format = workbook.add_format(
#         {"border": 1, "align": "center", "num_format": "0.00"}
#     )
#     int_format = workbook.add_format({"border": 1, "align": "center"})
#
#     for group_name, students in groups_data.items():
#         sheet_name = str(group_name)[:31]
#         worksheet = workbook.add_worksheet(sheet_name)
#
#         # Заголовки итоговой таблицы
#         table_headers = (
#             ["ФИО", "Группа"]
#             + task_headers
#             + ["Средний рейтинг", "Итоговая оценка"]
#         )
#         for col_idx, header in enumerate(table_headers):
#             worksheet.write(0, col_idx, header, header_format)
#
#         start_row = 1
#         for row_idx, student in enumerate(students, start=start_row):
#             group = student[0].strip()
#             name = student[1].strip()
#
#             # Преобразование текстовых баллов с запятыми в float
#             grades = []
#             for val in student[2 : 2 + num_tasks]:
#                 val_clean = val.strip().replace(",", ".")
#                 grades.append(float(val_clean) if val_clean else 0.0)
#
#             # Запись ФИО и группы
#             worksheet.write(row_idx, 0, name, cell_format)
#             worksheet.write(row_idx, 1, group, cell_format)
#
#             # Запись баллов за задания
#             for task_idx, grade in enumerate(grades):
#                 worksheet.write(row_idx, 2 + task_idx, grade, num_format)
#
#             # Формула вычисления среднего рейтинга
#             first_task_col = xlsxwriter.utility.xl_col_to_name(2)
#             last_task_col = xlsxwriter.utility.xl_col_to_name(1 + num_tasks)
#             avg_col = 2 + num_tasks
#             grade_col = avg_col + 1
#
#             row_num = row_idx + 1
#             avg_formula = f"=AVERAGE({first_task_col}{row_num}:{last_task_col}{row_num})"
#             worksheet.write_formula(
#                 row_idx, avg_col, avg_formula, num_format, 0
#             )
#
#             # Формула определения оценки на основе критериев
#             avg_cell = f"{xlsxwriter.utility.xl_col_to_name(avg_col)}{row_num}"
#             grade_formula = f"=IF({avg_cell}>=80, 5, IF({avg_cell}>=70, 4, IF({avg_cell}>=50, 3, 2)))"
#             worksheet.write_formula(
#                 row_idx, grade_col, grade_formula, int_format, 2
#             )
#
#         end_row = start_row + len(students) - 1
#
#         # --- Сводная строка средних баллов по каждому заданию ---
#         worksheet.write(end_row + 1, 0, "Средний балл", header_format)
#         worksheet.write(end_row + 1, 1, "", header_format)
#         for task_idx in range(num_tasks):
#             col_letter = xlsxwriter.utility.xl_col_to_name(2 + task_idx)
#             task_avg_formula = (
#                 f"=AVERAGE({col_letter}{start_row + 1}:{col_letter}{end_row + 1})"
#             )
#             worksheet.write_formula(
#                 end_row + 1, 2 + task_idx, task_avg_formula, num_format
#             )
#
#         # --- Таблица подсчета количества оценок для круговой диаграммы ---
#         summary_start_col = 2 + num_tasks + 3
#         worksheet.write(0, summary_start_col, "Оценка", header_format)
#         worksheet.write(0, summary_start_col + 1, "Кол-во", header_format)
#
#         grade_col_letter = xlsxwriter.utility.xl_col_to_name(2 + num_tasks + 1)
#         for idx, g in enumerate([5, 4, 3, 2]):
#             r = idx + 1
#             worksheet.write(r, summary_start_col, g, int_format)
#             count_formula = f"=COUNTIF({grade_col_letter}{start_row + 1}:{grade_col_letter}{end_row + 1}, {g})"
#             worksheet.write_formula(
#                 r, summary_start_col + 1, count_formula, int_format
#             )
#
#         # --- 1. Круговая диаграмма распределения оценок ---
#         pie_chart = workbook.add_chart({"type": "pie"})
#         pie_chart.add_series(
#             {
#                 "name": "Распределение оценок",
#                 "categories": [
#                     sheet_name,
#                     1,
#                     summary_start_col,
#                     4,
#                     summary_start_col,
#                 ],
#                 "values": [
#                     sheet_name,
#                     1,
#                     summary_start_col + 1,
#                     4,
#                     summary_start_col + 1,
#                 ],
#                 "data_labels": {"value": True, "percentage": True},
#             }
#         )
#         pie_chart.set_title({"name": f"Распределение оценок ({group_name})"})
#         worksheet.insert_chart(
#             "A" + str(end_row + 5), pie_chart, {"x_scale": 1.1, "y_scale": 1.1}
#         )
#
#         # --- 2. Гистограмма средней успеваемости по заданиям ---
#         bar_chart = workbook.add_chart({"type": "column"})
#         bar_chart.add_series(
#             {
#                 "name": "Средний балл",
#                 "categories": [sheet_name, 0, 2, 0, 1 + num_tasks],
#                 "values": [
#                     sheet_name,
#                     end_row + 1,
#                     2,
#                     end_row + 1,
#                     1 + num_tasks,
#                 ],
#                 "data_labels": {"value": True},
#             }
#         )
#         bar_chart.set_title({"name": "Средняя успеваемость по заданиям"})
#         bar_chart.set_x_axis({"name": "Задания"})
#         bar_chart.set_y_axis({"name": "Баллы"})
#         bar_chart.set_legend({"none": True})
#
#         worksheet.insert_chart(
#             "I" + str(end_row + 5), bar_chart, {"x_scale": 1.2, "y_scale": 1.1}
#         )
#
#     workbook.close()
#     print(f"Анализ файла '{input_csv}' успешно завершен! Результат в '{output_xlsx}'.")
#
#
# if __name__ == "__main__":
#     analyze_grades("test_table.csv", "test_table_analysis.xlsx")