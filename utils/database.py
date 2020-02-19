import pandas as pd

class DataBase:
  """
  Класс, который отвечает за взаимодействие с БД
  """

  def __init__(self):
    super().__init__()
    self.filename = 'apartments.csv'

  def open_connection(self):
    self.db = pd.read_csv(self.filename)


  def close_connection(self):
    self.db.to_csv('apartments.csv', index=None, header=True)


  def add_item(self, item):
    self.db = self.db.append(item, ignore_index=True)


  def is_in_db(self, item_url):
    selected_rows = self.db.loc[self.db['url'] == item_url]
    if selected_rows.shape[0] > 0:
      return True
    else:
      return False


  def clear(self):
    self.db = self.db.iloc[ 0:5 , : ]

  def find_by_url(self, item_url):
    pass


  def remove_by_url(self):
    pass


  def info(self):
    print('База данных на основе CSV')
    print(f'Размер таблицы: {self.db.shape[0]} элементов с {self.db.shape[1]} характеристиками')
    print(self.db.head())

