import pandas as pd
import json
from xml.etree import ElementTree as ET


items_csv = pd.read_csv('data/raw/items.csv')


with open('data/raw/items.json', 'r') as f:
    items_json = json.load(f)

items_json = pd.DataFrame(items_json['items'])


items_xml = ET.parse('data/raw/items.xml')
items_xml = pd.DataFrame([
    {subchild.tag: subchild.text for subchild in child}
    for child in items_xml.getroot()
])


def normalize_items(df):
    df = df.copy()

    df['id'] = pd.to_numeric(
        df['id'],
        errors='coerce'
    ).astype('Int64')

    df['value'] = df['value'].astype(str).str.replace(',', '.')
    df['value'] = pd.to_numeric(
        df['value'],
        errors='coerce'
    )

    df['updated_at'] = pd.to_datetime(
        df['updated_at'],
        format='mixed',
        errors='coerce'
    )

    clean_active = (
        df['active']
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace('.0', '', regex=False)
    )

    df['active'] = clean_active.map(
        {
            'true': True,
            'yes': True,
            '1': True,
            'да': True,
            'false': False,
            'no': False,
            '0': False,
            'нет': False
        }
    ).fillna(False)

    df['name'] = df['name'].str.strip().str.lower()
    df['category'] = df['category'].str.strip().str.lower()

    df = df.drop_duplicates()
    df = df.dropna(subset=['id'])

    return df


csv_normalized = normalize_items(items_csv)
json_normalized = normalize_items(items_json)
xml_normalized = normalize_items(items_xml)


df = pd.concat(
    [
        csv_normalized,
        json_normalized,
        xml_normalized
    ],
    ignore_index=True
)


df = df.sort_values(
    by=['id', 'updated_at'],
    ascending=True,
    na_position='first'
)

df = df.drop_duplicates(
    subset='id',
    keep='last'
).reset_index(drop=True)


df.to_csv(
    'data/processed/normalized_items.csv',
    index=False
)

df.to_json(
    'data/processed/normalized_items.json',
    orient='records',
    indent=4,
    date_format='iso',
    date_unit='s',
    force_ascii=False,
    default_handler=str
)

df.to_xml(
    'data/processed/normalized_items.xml',
    index=False,
    root_name='items',
    row_name='item'
)


print('Сохранены нормализованные объединенные файлы в трех форматах:')
print('- data/processed/normalized_items.csv')
print('- data/processed/normalized_items.json')
print('- data/processed/normalized_items.xml')

print(df.head())