import os
import pandas as pd

# Определяем возможные названия столбцов
name_columns = ['название', 'товар', 'наименование', 'продукт']
price_columns = ['цена', 'розница']
weight_columns = ['вес', 'масса', 'фасовка']


# Функция для загрузки данных из прайс-листов
def load_price_lists(directory):
    data = []
    for filename in os.listdir(directory):
        if 'price' in filename and filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path, delimiter=',', encoding='utf-8')
            # Фильтруем нужные столбцы
            df_filtered = df[[col for col in df.columns if col in name_columns + price_columns + weight_columns]]
            data.append((filename, df_filtered))
    return data


# Функция для поиска товаров
def search_products(data, query):
    results = []
    for filename, df in data:
        for index, row in df.iterrows():
            for name_col in name_columns:
                if name_col in row and pd.notna(row[name_col]) and query.lower() in str(row[name_col]).lower():
                    price = row[price_columns[0]] if price_columns[0] in row else row[price_columns[1]]
                    weight = None
                    for weight_col in weight_columns:
                        if weight_col in row and pd.notna(row[weight_col]):
                            weight = row[weight_col]
                            break  # Прекращаем цикл, как только нашли первый подходящий столбец
                    if weight > 0:  # Проверяем, что вес больше 0, чтобы избежать деления на ноль
                        price_per_kg = price / weight
                        results.append((row[name_col], price, weight, filename, price_per_kg))
    return sorted(results, key=lambda x: x[4])  # Сортируем по цене за кг


# Функция для вывода результатов в HTML
def output_to_html(results):
    html_content = ('<html>'
                    '<body>'
                    '<head>'
                    '<title>Позиции продуктов</title>'
                    '</head>'
                    '<table border="1">'
                    '<tr>'
                    '<th>№</th>'
                    '<th>Наименование</th>'
                    '<th>Цена</th>'
                    '<th>Вес</th>'
                    '<th>Файл</th>'
                    '<th>Цена за кг.</th>'
                    '</tr>')
    for i, (name, price, weight, filename, price_per_kg) in enumerate(results, start=1):
        html_content += (f'<tr>'
                         f'<td>{i}</td>'
                         f'<td>{name}</td>'
                         f'<td>{price}</td>'
                         f'<td>{weight}</td>'
                         f'<td>{filename}</td>'
                         f'<td>{price_per_kg:.2f}</td>'
                         f'</tr>')
    html_content += '</table></body></html>'

    with open('results.html', 'w', encoding='utf-16') as f:
        f.write(html_content)


# Основная функция
def main():
    directory = "./data_file"  # Путь к директории с прайс-листами
    data = load_price_lists(directory)

    while True:
        query = input("Введите фрагмент названия товара для поиска (или 'exit' для выхода): ")
        if query.lower() == 'exit':
            print("Работа завершена.")
            break

        results = search_products(data, query)
        if results:
            output_to_html(results)
            print("Результаты поиска сохранены в results.html.")
            for i, (name, price, weight, filename, price_per_kg) in enumerate(results, start=1):
                print(f"{i}   {name:<30} {price:<5} {weight:<5} {filename} {price_per_kg:.2f}")
        else:
            print("Товары не найдены.")


if __name__ == "__main__":
    main()
