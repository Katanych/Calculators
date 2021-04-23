import datetime as dt


class Calculator:
    """Родительский класс Калькулятор"""
    def __init__(self, limit):
        """Конструктор родительского класса
        
        Определяет свойства класса: денежный лимит (limit),
        пустой список для хранения записей (records).
        
        """
        self.limit = limit
        self.records = []

    def add_record(self, other):
        """Метод сохраняет новую запись"""
        self.records.append(other)

    def get_today_stats(self):
        """Метод возвращает сегодняшнюю сумму"""
        today = dt.date.today()
        return (sum([record.amount for record in self.records 
        if today == record.date]))

    def get_week_stats(self):
        """Метод возвращает сумму за последние 7 дней"""
        today = dt.date.today()
        week_ago = dt.timedelta(days=7)
        return (sum([record.amount for record in self.records 
        if today - week_ago <= record.date <= today]))

    def remained(self):
        """Метод возвращает остаток"""
        return self.limit - self.get_today_stats()


class Record:
    """Класс записи"""
    def __init__(self, amount, comment, date=None):
        """Конструктор записи
        
        Определяет свойства класса: количество (amount),
        комментарий (comment), дата заданная вручную или 
        сегодняшняя (date).
        
        """
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        

class CaloriesCalculator(Calculator):
    """Класс калькулятора калорий"""

    def get_calories_remained(self):
        """Метод полученных калорий
        
        Метод определяет, сколько еще калорий 
        можно/нужно получить сегодня.
        
        """
        remained = self.remained()
        if remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
            f'но с общей калорийностью не более {remained} кКал')
        return "Хватит есть!"


class CashCalculator(Calculator):
    """Класс калькулятора денег"""
    USD_RATE  = 75.0
    EURO_RATE = 85.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        """Метод потраченных денег
        Метод определяет, сколько еще денег можно 
        потратить сегодня в рублях, долларах или евро.
        
        """
        if self.remained() == 0:
            return "Денег нет, держись"

        currencies = {
            'eur': ('Euro', self.EURO_RATE),
            'usd': ('USD', self.USD_RATE),
            'rub': ('руб', self.RUB_RATE),
        }

        curr_name, curr_rate = currencies[currency]
        remained = round(self.remained() / curr_rate, 2)
            
        if remained > 0:
            return f"На сегодня осталось {remained} {curr_name}"
            
        negative_remained = abs(remained)
        return ("Денег нет, держись: твой долг - "
        f"{negative_remained} {curr_name}")