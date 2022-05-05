import pandas as pd
import sqlite3
from sqlalchemy import create_engine

df = pd.read_csv("parser/all_categories_info.csv")
df[['Calories', 'Measure_kkal']] = df['Калорийность'].str.split(' ', expand=True)
df[['Proteins', 'Measure_prot']] = df['Белки'].str.split(' ', expand=True)
df[['Fats', 'Measure_fats']] = df['Жиры'].str.split(' ', expand=True)
df[['Carbohydrates', 'Measure_carb']] = df['Углеводы'].str.split(' ', expand=True)
df = df.drop(columns=['Калорийность', 'Белки', 'Жиры', 'Углеводы'])

df['Product'] = df['Продукт']
df['Calories'] = df['Calories'].str.replace(',', '.')
df['Proteins'] = df['Proteins'].str.replace(',', '.')
df['Fats'] = df['Fats'].str.replace(',', '.')
df['Carbohydrates'] = df['Carbohydrates'].str.replace(',', '.')

df.astype({'Calories':'float64',
                'Proteins':'float64',
                'Fats':'float64',
                'Carbohydrates':'float64'}).dtypes


engine = create_engine("sqlite:///products.db")
"""
conn = sqlite3.connect('products')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS products '
          '(type, product, '
          'calories, measure_kkal,'
          'proteins, measure_prot,'
          'fats, Measure_fats,'
          'carbohydrates, measure_carb)')

conn.commit()
"""
data = pd.DataFrame(df, columns=['Type', 'Product', 'Calories', 'Measure_kkal',
                                 'Proteins', 'Measure_prot',
                                 'Fats', 'Measure_fats',
                                 'Carbohydrates', 'Measure_carb'])
data.to_sql('products', engine, if_exists='replace', index=False)
#print(df.shape)