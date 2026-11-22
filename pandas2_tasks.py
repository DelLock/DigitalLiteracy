# pandas2: главы 4, 5, 6 — задания для самостоятельной работы
import os
import numpy as np
import pandas as pd
import seaborn as sns

df = sns.load_dataset('titanic')
os.makedirs('data_output', exist_ok=True)

# ======================================================================
# ГЛАВА 4. Чтение и запись данных (4.7)
# ======================================================================
print('\n=== Глава 4 ===')

# 1. CSV без индекса, разделитель ';', пропуски -> 'missing'
df.to_csv('data_output/titanic_missing.csv', sep=';', index=False, na_rep='missing')

# 2. Читаем файл, 'missing' -> NaN
df_missing = pd.read_csv('data_output/titanic_missing.csv', sep=';', na_values=['missing'])
print('4.2:', df_missing.shape)
print(df_missing.isna().sum().head())

# 3. Excel только с survived, sex, age, fare; пропуски в age -> среднее
small = df[['survived', 'sex', 'age', 'fare']].copy()
small['age'] = small['age'].fillna(small['age'].mean())
small.to_excel('data_output/titanic_small.xlsx', index=False)
print('4.3: пропусков в age =', small['age'].isna().sum())

# 4. Excel с тремя листами: All, Survived, Died
with pd.ExcelWriter('data_output/titanic_3sheets.xlsx') as writer:
    df.to_excel(writer, sheet_name='All', index=False)
    df[df['survived'] == 1].to_excel(writer, sheet_name='Survived', index=False)
    df[df['survived'] == 0].to_excel(writer, sheet_name='Died', index=False)
sheets = pd.read_excel('data_output/titanic_3sheets.xlsx', sheet_name=None)
print('4.4:', {name: s.shape for name, s in sheets.items()})

print('\n=== Глава 5 ===')

# 1. Количество и доля пропусков в каждом столбце
na_count = df.isnull().sum()
na_share = (na_count / len(df)).round(3)
print('5.1:')
print(pd.DataFrame({'пропусков': na_count, 'доля': na_share}).sort_values('пропусков', ascending=False))

# 2. Только столбцы с пропусками, и сколько их
cols_with_na = df.columns[df.isnull().any()].tolist()
df_only_na = df[cols_with_na]
print('5.2:', len(cols_with_na), 'столбцов ->', cols_with_na)

# 3. Сколько строк без единого пропуска
rows_no_na = len(df.dropna())
print('5.3: строк без пропусков =', rows_no_na)

# 4. Удалить строки, где пропущен age
df_age_ok = df.dropna(subset=['age'])
print('5.4: осталось строк =', len(df_age_ok))

# 5. Удалить столбцы с пропусками
df_no_na_cols = df.dropna(axis=1)
print('5.5: осталось столбцов =', df_no_na_cols.shape[1])

# 6. Заполнить age медианой, сравнить среднее до и после
mean_before = df['age'].mean()
age_filled = df['age'].fillna(df['age'].median())
mean_after = age_filled.mean()
print(f'5.6: средний возраст до = {mean_before:.2f}, после = {mean_after:.2f}')

# ======================================================================
# ГЛАВА 6. Преобразование данных (6.6)
print('\n=== Глава 6 ===')
t = df.copy()

# 1. sex_ru через map()
t['sex_ru'] = t['sex'].map({'male': 'мужчина', 'female': 'женщина'})
print('6.1:')
print(t[['sex', 'sex_ru']].head())

# 2. is_child через apply(axis=1): True, если возраст < 15
t['is_child'] = t.apply(lambda row: bool(pd.notna(row['age']) and row['age'] < 15), axis=1)
print('6.2:')
print(t['is_child'].value_counts())

# 3. Сортировка по fare по убыванию, пропуски в конец
print('6.3:')
print(t.sort_values('fare', ascending=False, na_position='last')[['pclass', 'fare']].head())

# 4. Сортировка по pclass (возр.) и age (убыв.), первые 5 строк
print('6.4:')
print(t.sort_values(['pclass', 'age'], ascending=[True, False])[['pclass', 'age', 'sex']].head(5))
