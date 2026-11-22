# pandas4: глава 10 — задания для самостоятельной работы
# (в главе 9 раздела с заданиями нет)
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset('titanic')

# Столбец booking_date: в pandas2 (раздел 6.5.6) он создаётся случайно,
# поэтому создаём его заново так же
np.random.seed(42)
df['booking_date'] = pd.to_datetime('1912-01-01') + pd.to_timedelta(
    np.random.randint(0, 100, size=len(df)), unit='D'
)

# 1. Линейный график дневного числа бронирований
daily = df['booking_date'].value_counts().sort_index()
plt.figure(figsize=(10, 4))
daily.plot(kind='line')
plt.title('Число бронирований по дням')
plt.xlabel('Дата')
plt.ylabel('Бронирований')
plt.tight_layout()
plt.show()

# 2. Столбчатая диаграмма: пассажиры по портам посадки
plt.figure(figsize=(6, 4))
df['embark_town'].value_counts().plot(kind='bar')
plt.title('Пассажиры по портам посадки')
plt.xlabel('Порт')
plt.ylabel('Количество')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 3. Горизонтальная диаграмма: доля выживших по классу
plt.figure(figsize=(6, 4))
df.groupby('pclass')['survived'].mean().plot(kind='barh')
plt.title('Доля выживших по классу')
plt.xlabel('Доля выживших')
plt.ylabel('Класс')
plt.tight_layout()
plt.show()

# 4. Гистограмма возраста (30 бинов) + красная пунктирная линия среднего
plt.figure(figsize=(7, 4))
df['age'].plot(kind='hist', bins=30, edgecolor='black')
plt.axvline(df['age'].mean(), color='red', linestyle='--',
            label=f"Среднее = {df['age'].mean():.1f}")
plt.title('Распределение возраста')
plt.xlabel('Возраст')
plt.legend()
plt.tight_layout()
plt.show()

# 5. Круговая диаграмма: доли пассажиров по порту посадки
plt.figure(figsize=(5, 5))
df['embark_town'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Доли пассажиров по портам посадки')
plt.ylabel('')
plt.tight_layout()
plt.show()

# 6. countplot: выживаемость по классу и полу (hue='sex')
# Две панели: слева погибшие (survived=0), справа выжившие (survived=1)
g = sns.catplot(data=df, x='pclass', hue='sex', col='survived', kind='count', height=4)
g.set_axis_labels('Класс', 'Количество')
g.set_titles('survived = {col_name}')
plt.tight_layout()
plt.show()
