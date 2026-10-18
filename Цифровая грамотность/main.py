#___________СЧЁТ_____
# import os
# import random
# from docxtpl import DocxTemplate
# from docx import Document
#
# companies = ['ООО "Ромашка"', 'ИП Иванов А.А.', 'ЗАО "Вектор"', 'ООО "Альфа-Трейд"', 'ПАО "ГазМяс"']
# sellers = ['Смирнов В.В.', 'Петров П.П.', 'Сидоров И.И.', 'Кузнецов А.Б.']
# addresses = ['г. Москва, ул. Пушкина, д. 10', 'г. Санкт-Петербург, Невский пр-т, д. 5']
# months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня']
# product_titles = ['Бумага А4', 'Ручка шариковая', 'Степлер', 'Карандаш', 'Тетрадь 48л']
#
# final_doc = Document()
#
# print("Генерируем 20 чеков...")
#
# for i in range(1, 21):
#     tpl = DocxTemplate("tmp.docx")
#
#     products_count = random.randint(2, 5)
#     products = []
#     general_sum = 0
#
#     for _ in range(products_count):
#         amount = random.randint(1, 20)
#         price = random.randint(50, 1500)
#         prod_sum = amount * price
#         general_sum += prod_sum
#
#         products.append({
#             'title': random.choice(product_titles),
#             'code': str(random.randint(10000, 99999)),
#             'unit': 'шт.',
#             'amount': amount,
#             'price': price,
#             'sum': prod_sum
#         })
#
#     context = {
#         'company': random.choice(companies),
#         'check_number': f"{random.randint(1000, 9999)}-{i}",
#         'day': str(random.randint(1, 28)).zfill(2),
#         'month': random.choice(months),
#         'year': str(random.randint(20, 24)),
#         'seller': random.choice(sellers),
#         'address': random.choice(addresses),
#         'ORGN': str(random.randint(1000000000000, 9999999999999)),
#         'products': products,
#         'general_sum': general_sum
#     }
#
#     temp_filename = f"temp_{i}.docx"
#     tpl.render(context)
#     tpl.save(temp_filename)
#
#     temp_doc = Document(temp_filename)
#     for element in temp_doc.element.body:
#         final_doc.element.body.append(element)
#
#     if i < 20:
#         final_doc.add_page_break()
#
#     os.remove(temp_filename)
#
# output_file = "checks.docx"
# final_doc.save(output_file)
#
# print(f"Готово! '{output_file}'")


# #####ПРИГЛАШЕНИЕ########
# import os
# from docx import Document
# from docx.shared import Inches, Pt, RGBColor
# from docx.enum.text import WD_ALIGN_PARAGRAPH
# from docx.enum.table import WD_TABLE_ALIGNMENT
# from PIL import Image, ImageDraw
#
# def create_dummy_images():
#     """Вспомогательная функция для создания картинок подписи и печати, если их нет"""
#     if not os.path.exists("signature.png"):
#         img = Image.new('RGBA', (200, 80), color=(255, 255, 255, 0))
#         d = ImageDraw.Draw(img)
#         d.text((10, 30), "Подпись", fill=(0, 0, 139))
#         img.save("signature.png")
#
#     if not os.path.exists("stamp.png"):
#         img = Image.new('RGBA', (150, 150), color=(255, 255, 255, 0))
#         d = ImageDraw.Draw(img)
#         d.ellipse([5, 5, 145, 145], outline=(0, 0, 139), width=3)
#         d.text((35, 65), "М.П. ПЕЧАТЬ", fill=(0, 0, 139))
#         img.save("stamp.png")
#
# create_dummy_images()
#
# # Создаем новый документ Word
# doc = Document()
#
# # 1. Заголовок первого уровня
# title = doc.add_heading('ПОВЕСТКА / ПРИГЛАШЕНИЕ', level=1)
# title.alignment = WD_ALIGN_PARAGRAPH.CENTER
#
# # 2. Подзаголовок (второй уровень)
# subtitle = doc.add_heading('Официальное уведомление', level=2)
# subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
#
# # 3. Основной параграф с жирным и курсивным текстом
# p1 = doc.add_paragraph()
# p1.add_run("Уважаемый(-ая) ").font.color.rgb = RGBColor(50, 50, 50)
# p1.add_run("{{ name }}").bold = True  # Тег для docxtpl
# p1.add_run(", проживающий(-ая) по адресу: ")
# p1.add_run("{{ address }}").italic = True  # Тег для docxtpl
#
# p2 = doc.add_paragraph()
# p2.add_run("Вам надлежит явиться в назначенный срок для прохождения мероприятий, связанных с уточнением данных персонального учета.")
#
# # 4. Заголовок третьего уровня
# doc.add_heading('Детали визита', level=3)
#
# # 5. Таблица с информацией
# table = doc.add_table(rows=3, cols=2)
# table.alignment = WD_TABLE_ALIGNMENT.CENTER
# table.style = 'Table Grid'
#
# # Заполнение таблицы (с тегами docxtpl)
# table.cell(0, 0).text = "Дата явки:"
# table.cell(0, 1).text = "{{ date }}"
# table.cell(1, 0).text = "Время явки:"
# table.cell(1, 1).text = "{{ time }}"
# table.cell(2, 0).text = "Место проведения:"
# table.cell(2, 1).text = "{{ location }}"
#
# doc.add_paragraph() # Отступ
#
# # 6. Ненумерованный (маркированный) список
# doc.add_paragraph('При себе в обязательном порядке иметь следующие документы:', style='List Bullet')
# doc.add_paragraph('Паспорт гражданина РФ', style='List Bullet')
# doc.add_paragraph('Настоящее приглашение / повестку', style='List Bullet')
# doc.add_paragraph('Документы, подтверждающие право на льготы (при наличии)', style='List Bullet')
#
# # 7. Блок подписи и печати (Таблица без границ для аккуратной верстки)
# doc.add_heading('Подтверждение и заверение', level=3)
#
# sig_table = doc.add_table(rows=2, cols=2)
# sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
#
# # Левая ячейка — Текст и подпись
# cell_left = sig_table.cell(0, 0)
# p_sig = cell_left.paragraphs[0]
# p_sig.add_run("Военный комиссар:\n").bold = True
# p_sig.add_run("Иванов И.И. / ________________")
#
# # Вставляем подпись
# p_img1 = cell_left.add_paragraph()
# p_img1.add_run().add_picture("signature.png", width=Inches(1.5))
#
# # Правая ячейка — Место для печати
# cell_right = sig_table.cell(0, 1)
# p_stamp_title = cell_right.paragraphs[0]
# p_stamp_title.add_run("Место для печати:").italic = True
#
# p_img2 = cell_right.add_paragraph()
# p_img2.add_run().add_picture("stamp.png", width=Inches(1.2))
#
# # Сохраняем документ-шаблон
# doc.save("invitation_template.docx")
# print("Шаблон 'invitation_template.docx' успешно создан!")


#_____ПРИГЛАШЕНИЕ_2________
# import os
#
# from docxtpl import DocxTemplate
# invitees = [
#     {
#         "name": "Иванов Алексей Сергеевич",
#         "address": "г. Москва, ул. Ленина, д. 12, кв. 45",
#         "date": "15 октября 2026 г.",
#         "time": "09:00",
#         "location": "Военный комиссариат № 1, Каб. 102",
#     },
#     {
#         "name": "Петров Дмитрий Владимирович",
#         "address": "г. Москва, ул. Тверская, д. 8, кв. 12",
#         "date": "15 октября 2026 г.",
#         "time": "10:00",
#         "location": "Военный комиссариат № 1, Каб. 102",
#     },
#     {
#         "name": "Сидоров Михаил Александрович",
#         "address": "г. Москва, пр-т Мира, д. 105, кв. 78",
#         "date": "15 октября 2026 г.",
#         "time": "11:00",
#         "location": "Военный комиссариат № 1, Каб. 104",
#     },
#     {
#         "name": "Смирнов Артем Игоревич",
#         "address": "г. Москва, ул. Арбат, д. 15, кв. 3",
#         "date": "16 октября 2026 г.",
#         "time": "09:00",
#         "location": "Военный комиссариат № 1, Каб. 102",
#     },
#     {
#         "name": "Кузнецов Илья Николаевич",
#         "address": "г. Москва, ул. Гагарина, д. 40, кв. 91",
#         "date": "16 октября 2026 г.",
#         "time": "10:00",
#         "location": "Военный комиссариат № 1, Каб. 105",
#     },
#     {
#         "name": "Васильев Роман Олегович",
#         "address": "г. Москва, ул. Кирова, д. 3, кв. 14",
#         "date": "16 октября 2026 г.",
#         "time": "11:00",
#         "location": "Военный комиссариат № 1, Каб. 102",
#     },
#     {
#         "name": "Попов Егор Андреевич",
#         "address": "г. Москва, ул. Садовая, д. 22, кв. 5",
#         "date": "17 октября 2026 г.",
#         "time": "09:30",
#         "location": "Военный комиссариат № 1, Каб. 101",
#     },
#     {
#         "name": "Соколов Максим Витальевич",
#         "address": "г. Москва, ш. Энтузиастов, д. 50, кв. 112",
#         "date": "17 октября 2026 г.",
#         "time": "10:30",
#         "location": "Военный комиссариат № 1, Каб. 101",
#     },
#     {
#         "name": "Михайлов Кирилл Денисович",
#         "address": "г. Москва, ул. Новая, д. 7, кв. 33",
#         "date": "17 октября 2026 г.",
#         "time": "11:30",
#         "location": "Военный комиссариат № 1, Каб. 104",
#     },
#     {
#         "name": "Новиков Никита Сергеевич",
#         "address": "г. Москва, ул. Зеленая, д. 19, кв. 60",
#         "date": "18 октября 2026 г.",
#         "time": "09:00",
#         "location": "Военный комиссариат № 1, Каб. 102",
#     },
#     {
#         "name": "Федоров Павел Романович",
#         "address": "г. Москва, ул. Школьная, д. 2, кв. 18",
#         "date": "18 октября 2026 г.",
#         "time": "10:00",
#         "location": "Военный комиссариат № 1, Каб. 102",
#     },
#     {
#         "name": "Морозов Андрей Евгеньевич",
#         "address": "г. Москва, ул. Лесная, д. 88, кв. 4",
#         "date": "18 октября 2026 г.",
#         "time": "11:00",
#         "location": "Военный комиссариат № 1, Каб. 103",
#     },
#     {
#         "name": "Волков Степан Максимοвич",
#         "address": "г. Москва, ул. Полевая, д. 11, кв. 27",
#         "date": "19 октября 2026 г.",
#         "time": "09:00",
#         "location": "Военный комиссариат № 1, Каб. 102",
#     },
#     {
#         "name": "Алексеев Глеб Викторович",
#         "address": "г. Москва, ул. Речная, д. 5, кв. 82",
#         "date": "19 октября 2026 г.",
#         "time": "10:00",
#         "location": "Военный комиссариат № 1, Каб. 105",
#     },
#     {
#         "name": "Лебедев Владислав Юрьевич",
#         "address": "г. Москва, ул. Южная, д. 31, кв. 9",
#         "date": "19 октября 2026 г.",
#         "time": "11:00",
#         "location": "Военный комиссариат № 1, Каб. 102",
#     },
# ]
#
# # Папка для сохранения готовых документов
# output_dir = "Generated_Invitations"
# os.makedirs(output_dir, exist_ok=True)
#
# # 2. Цикл генерации документов на основе шаблона
# for person in invitees:
#     # Загружаем шаблон, созданный в первой задаче
#     doc = DocxTemplate("invitation_template.docx")
#
#     # Передаем данные человека в контекст
#     doc.render(person)
#
#     # Формируем безопасное имя файла (ФИО.docx)
#     filename = f"{person['name']}.docx"
#     filepath = os.path.join(output_dir, filename)
#
#     # Сохраняем индивидуальный документ на диск
#     doc.save(filepath)
#
# print(
#     f"Готово! Сгенерированы {len(invitees)} документы в '{output_dir}'."
# )


#___Лекция_3_____
import numpy as np
import pandas as pd
import seaborn as sns

df = sns.load_dataset('titanic')

print('ГЛАВА 1: Задания для самостоятельной работы')


print('Задание 1.2: Первые 10 строк')
print(df.head(10), '\n')

print('Задание 1.3: Размер датасета (строк, столбцов)')
print(df.shape, '\n')

print('Задание 1.4: Список всех столбцов ---')
print(df.columns.tolist(), '\n')

print('Задание 1.5: Пропущенные значения в столбцах')
print(df.isnull().sum(), '\n')

print('Задание 1.6: Средний возраст пассажиров')
print(df['age'].mean(), '\n')

print('Задание 1.7: Количество пассажиров в каждом классе')
print(df['pclass'].value_counts(), '\n')

print('Задание 1.8: Описательные статистики')
print(df.describe(), '\n')

print('Задание 1.9: Доля выживших среди всех пассажиров')
print(df['survived'].value_counts(normalize=True), '\n')


print('ГЛАВА 2: Задания для самостоятельной работы')


df_tasks = df.copy()

df_tasks = df_tasks.rename(
    columns={'sex': 'gender', 'pclass': 'passenger_class'}
)
print('Задание 2.1: После переименовывания столбцов')
print(df_tasks[['gender', 'passenger_class']].head(2), '\n')

df_tasks['fare_in_rub'] = df_tasks['fare'] * 100
print('Задание 2.2: Добавлен столбец fare_in_rub')
print(df_tasks[['fare', 'fare_in_rub']].head(2), '\n')

df_tasks = df_tasks.drop(
    columns=['deck', 'embark_town', 'alone'], errors='ignore'
)
print('Задание 2.3: Удалены указанные столбцы. Остались:')
print(df_tasks.columns.tolist(), '\n')



print('ГЛАВА 3: Задания для самостоятельной работы')


print('Задание 3.1: Первые 10 строк (gender, age, fare)')
print(df_tasks.loc[:9, ['gender', 'age', 'fare']], '\n')

print('Задание 3.2: Пассажиры с билетом дороже 200')
print(df_tasks[df_tasks['fare'] > 200], '\n')

print('Задание 3.3: Мужчины младше 20 лет, не выжившие')
print(
    df_tasks[
        (df_tasks['gender'] == 'male')
        & (df_tasks['age'] < 20)
        & (df_tasks['survived'] == 0)
    ].head(),
    '\n',
)

print('Задание 3.4: Количество пассажиров из Queenstown')
print(df['embark_town'].value_counts().get('Queenstown', 0), '\n')

print('Задание 3.5: Результат через query()')
print(df.query('embarked == "C" and age > 30 and pclass == 2').head(), '\n')

print('Задание 3.6: Топ-10 самых молодых пассажиров')
print(df_tasks.sort_values('age').head(10)[['gender', 'age', 'fare']], '\n')

print('Задание 3.7: Возраст [25; 35] и билет > 50 ')
print(
    df_tasks[
        df_tasks['age'].between(25, 35) & (df_tasks['fare'] > 50)
    ].head(),
    '\n',
)

print(
    'Задание 3.8: Женщины 3 класса > 18 лет, отсортированные по цене (топ-10)'
)
result = (
    df_tasks[
        (df_tasks['gender'] == 'female')
        & (df_tasks['passenger_class'] == 3)
        & (df_tasks['age'] > 18)
    ]
    .sort_values('fare', ascending=False)
    .head(10)
)
print(result[['gender', 'passenger_class', 'age', 'fare', 'survived']])