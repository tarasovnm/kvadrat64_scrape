import re

# Очисить значения столбцов 'Площадь', 'Жилая', 'Кухня', 'Цена', 'Высота потолков', 'Этаж/этажей в доме' 
# 'Вторичное жилье', 'Год постройки', 'Дата сдачи' от текста

def parse_rooms(flat_string):
    rooms_pattern = r'\d{1,2}'
    flat_string = str(flat_string)
    match = re.search(rooms_pattern, flat_string) 
    return int(match[0]) if match else 0

def parse_area(area_string):
    area_pattern = r'\d+\.?\d*'
    area_string = str(area_string)
    match = re.search(area_pattern, area_string)
    return float(match[0]) if match else 0.0

def parse_price(price_string):
    price_pattern = r'\d+'
    price_string = str(price_string)
    match = re.search(price_pattern, price_string.replace(' ', '')) 
    return float(match[0]) if match else 0.0

def parse_ceiling_height(height_string):
    height_pattern = r'\d+\.\d+'
    height_string = str(height_string).replace(',','.')
    match = re.search(height_pattern, height_string) 
    return float(match[0]) if match else 0.0

def parse_floor(floor_string):
    right_pattern = r'\d+\/\d+'
    floor_pattern = r'\d+'
    floor_string = str(floor_string)
    if re.search(right_pattern, floor_string):
        match = re.findall(floor_pattern, floor_string)
        return int(match[0]) if match else 0
    else:
        return 0
    
def parse_num_of_floors(floor_string):
    right_pattern = r'\d+\/\d+'
    floor_pattern = r'\d+'
    floor_string = str(floor_string)
    if re.search(right_pattern, floor_string):
        match = re.findall(floor_pattern, floor_string)
        return int(match[1]) if match else 0
    else:
        return 0
    
def parse_year(year_string):
    year_pattern = r'\d{4}'
    match = re.search(year_pattern, year_string) 
    return int(match[0]) if match else 0