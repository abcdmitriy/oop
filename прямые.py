import matplotlib.pyplot as plt

class Solution:
    def __init__(self, text): #инициализатор
        self.text = text

    def get_read(self): #читаем файл
        list_lines = []
        with open(self.text, 'r') as file:
            for line in file:
                list_lines.append(line.strip())
        return list_lines

    def get_slovar(self):  # создаем словарь координат с их порядковым номером
        slovar = {}
        list_lines = self.get_read()
        for line in list_lines:
            if line:
                value_line, key = line.rsplit(' ', 1)  # разделяем строчки на ключ и на координаты
                values = value_line.strip('()').split(', ')  # убираем ненужные штуки
                my_values = []
                for value in values:
                    float_value = float(value)
                    my_values.append(float_value)
                slovar[int(key)] = my_values
        return slovar

    def get_coordinates(self, key):
        slovar = self.get_slovar()
        if key in slovar:
            return slovar[key]
        else:
            return 'Такого отрезка нет'

    def get_coordinates_x(self, key):
        coordinates = self.get_coordinates(key)
        if coordinates == 'Такого отрезка нет':
            return 'Такого отрезка нет'
        return coordinates[::2]

    def get_coordinates_y(self, key):
        coordinates = self.get_coordinates(key)
        if coordinates == 'Такого отрезка нет':
            return 'Такого отрезка нет'
        return coordinates[1::2]

    def get_graph(self, key): #прямая на графике
        coordinates = self.get_coordinates(key)
        if coordinates == 'Такого отрезка нет':
            return 'Такого отрезка нет'

        lx = self.get_coordinates_x(key)
        ly = self.get_coordinates_y(key)

        plt.xlim(-0.1, 1.4)
        plt.ylim(-0.1, 1.4)
        plt.plot([0, 0, 1, 1, 0], [0, 1, 1, 0, 0], linewidth=2, color='b') #рисуем квадрат

        plt.scatter(lx, ly, color='r') #рисуем точки
        plt.plot(lx, ly, linewidth=1, color='r') #рисуем наш отрезок

        plt.grid()
        plt.show()

    def get_rav(self, key): #определяем вид отрезка
        coordinates = self.get_coordinates(key)
        if coordinates == 'Такого отрезка нет':
            return 'Такого отрезка нет'

        kab_x = [] #вертикальный отрезок
        kab_y = [] #горизонтальный отрезок
        kab = [] #наклонный отрезок
        x1 = coordinates[0]
        y1 = coordinates[1]
        x2 = coordinates[2]
        y2 =coordinates[3]

        if x1 == x2:
            kab_x.append(x1)
            return kab_x

        if y1 == y2:
            kab_y.append(y1)
            return kab_y

        k = (y1 - y2) / (x1 - x2)
        b = ((x1 * y2) - (y1 * x2)) / (x1 - x2)

        kab.append(round(k, 3))
        kab.append(round(b, 3))

        return kab

    def get_urav(self):
        urav = {
                'kab_x': [],  # список для вертикальных линий
                'kab_y': [],  # список для горизонтальных линий
                'kab': []  # список для наклонных линий
                }

        keys = self.get_slovar().keys()  #получаем все ключи из словаря

        for key in keys:
            coordinates = self.get_coordinates(key)
            coefficients = self.get_rav(key)  # получаем коэффициенты для каждой прямой

            if len(coefficients) == 1:
                if coefficients[0] == coordinates[0]:
                    urav['kab_x'].append(coefficients[0])
                else:
                    urav['kab_y'].append(coefficients[0])
            else:
                urav['kab'].append(coefficients)

        return urav

    def get_point(self):
        urav = self.get_urav()
        kab_x = urav['kab_x']  # Вертикальные линии
        kab_y = urav['kab_y']  # Горизонтальные линии
        kab = urav['kab']  # Обычные линии
        intersections = []

        # Пересечения вертикальных и горизонтальных линий
        for x in kab_x:  # x — координаты вертикальных линий
            for y in kab_y:  # y — координаты горизонтальных линий
                if x < 1 and y < 1:  # Проверяем, что обе координаты меньше 1
                    intersections.append((x, y))  # Точка пересечения (x, y)

        # Пересечения вертикальных и наклонных линий
        for x in kab_x:  # x — координаты вертикальных линий
            for k, b in kab:  # k и b для наклонных линий
                y = k * x + b
                if x < 1 and y < 1:  # Проверяем, что обе координаты меньше 1
                    intersections.append((x, y))  # Точка пересечения (x, y)

        # Пересечения горизонтальных и наклонных линий
        for y in kab_y:  # y — координаты горизонтальных линий
            for k, b in kab:  # k и b для наклонных линий
                if k != 0:  # Проверяем, что k не равен 0, чтобы избежать деления на ноль
                    x = (y - b) / k
                    if x < 1 and y < 1:  # Проверяем, что обе координаты меньше 1
                        intersections.append((x, y))  # Точка пересечения (x, y)

        # Пересечения двух наклонных линий
        for i in range(len(kab)):
            for j in range(i + 1, len(kab)):
                k1, b1 = kab[i]
                k2, b2 = kab[j]
                if k1 != k2:  # Предотвращаем пересечение параллельных линий
                    x = (b2 - b1) / (k1 - k2)
                    y = k1 * x + b1
                    if x < 1 and y < 1:  # Проверяем, что обе координаты меньше 1
                        intersections.append((x, y))  # Точка пересечения (x, y)

        return intersections

    def find_repeated_points(self):
        intersections = self.get_point()  # Получаем все точки пересечения
        point_count = {}

        # Подсчитываем вхождения каждой точки
        for point in intersections:
            if point in point_count:
                point_count[point] += 1
            else:
                point_count[point] = 1

        # Находим точки, которые повторяются 3 и более раз
        repeated_points = [point for point, count in point_count.items() if count >= 3]

        if repeated_points:
            print("Точки, которые повторяются 3 и более раз:")
            for point in repeated_points:
                print(point)
        else:
            print("Таких точек не найдено.")

    def get_p(self, key):
        coordinates = self.get_coordinates(key)
        x1 = coordinates[0]
        x2 = coordinates[2]
        y1 = coordinates[1]
        y2 = coordinates[3]

        # Проверяем условия для x1 и y1
        if x1 == 0.0 and (0.0 <= y1 <= 1.0):
            if (0 <= x2 <= 1) and y2 == 1:
                return 'правовверх'

            if (0 <= x2 <= 1) and y2 == 0.0:
                return 'правониз'

        elif x1 == 1.0 and (0 <= y1 <= 1):
            if (0 <= x2 <= 1) and y2 == 1:
                return 'левовверх'

            if (0 <= x2 <= 1) and y2 == 0.0:
                return 'левониз'

        # Проверка для обратных условий по x2 и y2
        if x2 == 0.0 and (0.0 <= y2 <= 1.0):
            if (0 <= x1 <= 1) and y1 == 1:
                return 'правовверх'

            if (0 <= x1 <= 1) and y1 == 0.0:
                return 'правониз'

        elif x2 == 1.0 and (0 <= y2 <= 1):
            if (0 <= x1 <= 1) and y1 == 1:
                return 'левовверх'

            if (0 <= x1 <= 1) and y1 == 0.0:
                return 'левониз'

        if (0 < y1 < 1) and (0 < y2 < 1) and ((x1 == 0.0 and x2 == 1.0) or (x2 == 0.0 and x1 == 1.0)):
            return 'праволево'

        if (0 < x1 < 1) and (0 < x2 < 1) and ((y1 == 0.0 and y2 == 1.0) or (y2 == 0.0 and y1 == 1.0)):
            return 'низвверх'

        return None

    def get_area(self, key):
        coordinates = self.get_coordinates(key)
        x1 = coordinates[0]
        x2 = coordinates[2]
        y1 = coordinates[1]
        y2 =coordinates[3]
        lol = self.get_p(key)

        if lol == 'правовверх':
            if x1 == 0.0:
                return 0.5 * x2 * (1 - y1)
            else:
                return 0.5 * x1 * (1 - y2)

        if lol == 'правониз':
            if x1 == 0.0:
                return 0.5 * x2 * y1
            else:
                return 0.5 * x1 * y2

        if lol == 'левовверх':
            if x1 == 1.0:
                return 0.5 * (1 - x2) * (1 - y1)
            else:
                return 0.5 * (1 - x1) * (1 - y2)

        if lol == 'левониз':
            if x1 == 1.0:
                return 0.5 * (1 - x2) * y1
            else:
                return 0.5 * (1 - x1) * y2

        if lol == 'низвверх':
            return (x1 + x2) * 0.5

        if lol == 'праволево':
            return (y1 + y2) * 0.5


fufiks = Solution('text.фуфик')
print(fufiks.get_urav())

