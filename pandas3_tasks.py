# pandas3: главы 7, 8 — задания для самостоятельной работы
import pandas as pd
import seaborn as sns

df = sns.load_dataset('titanic')

# ======================================================================
# ГЛАВА 7. Группировка и агрегация (7.7)
# ======================================================================
print('\n=== Глава 7 ===')

# 1. Количество пассажиров в каждом порту посадки
print('7.1:')
print(df.groupby('embark_town').size())

# 2. Средний возраст по классам
print('7.2:')
print(df.groupby('pclass')['age'].mean().round(2))

# 3. Средняя стоимость билета по классу и полу
print('7.3:')
print(df.groupby(['pclass', 'sex'])['fare'].mean().round(2))

# 4. Доля выживших по каждому порту посадки
print('7.4:')
print(df.groupby('embark_town')['survived'].mean().round(3))

# 5. filter(): порты, где средний возраст > 28
ports_old = df.groupby('embark_town').filter(lambda g: g['age'].mean() > 28)
print('7.5:', ports_old['embark_town'].unique().tolist(), '| строк:', len(ports_old))

# 6. filter(): группы [sex, pclass], где доля выживших > 0.7
groups_surv = df.groupby(['sex', 'pclass']).filter(lambda g: g['survived'].mean() > 0.7)
print('7.6:')
print(groups_surv.groupby(['sex', 'pclass'])['survived'].agg(['mean', 'size']).round(3))

# ======================================================================
# ГЛАВА 8. Объединение таблиц (8.4)
# ======================================================================
print('\n=== Глава 8 ===')

# 1. Делим на чётные и нечётные строки, склеиваем concat(axis=0) без ignore_index
even = df.iloc[::2]    # строки 0, 2, 4, ...
odd = df.iloc[1::2]    # строки 1, 3, 5, ...
print('8.1: чётных =', len(even), ', нечётных =', len(odd))

combined = pd.concat([even, odd], axis=0)
print('Форма:', combined.shape)
print('Индекс (первые 10):', combined.index[:10].tolist())
print('Индекс уникален:', combined.index.is_unique)
print('Индекс отсортирован:', combined.index.is_monotonic_increasing)
print('Порядок строк как в оригинале:', combined.index.equals(df.index))
# Строки те же, но порядок другой: сначала все чётные, потом все нечётные.
# Индекс сохранил исходные метки. Вернуть исходный порядок можно так:
print('После sort_index равно оригиналу:', combined.sort_index().equals(df))

# 2. То же через ignore_index=True
combined_ignore = pd.concat([even, odd], axis=0, ignore_index=True)
print('8.2: индекс (первые 10):', combined_ignore.index[:10].tolist())
print('Индекс = RangeIndex 0..n-1:', combined_ignore.index.equals(pd.RangeIndex(len(df))))
# Разница: без ignore_index сохраняются старые метки индекса (0, 2, 4, ..., 1, 3, 5, ...),
# с ignore_index=True старые метки теряются и индекс нумеруется заново 0..n-1.
# Порядок одинаковый (чётные, затем нечётные).
