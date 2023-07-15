import random
import math
import matplotlib.pyplot as plt

txt_path = 'C:/Users/79531/Downloads/file.txt'

def from_16_to_10(value):
    hex_num = value  # шестнадцатеричное число
    dec_num = int(hex_num, 16)  # преобразуем в десятичное
    return dec_num

def parse_txt_file(path):
    parsed_data = []
    section = {}

    with open(path, 'r') as file:
        while True:
            # считываем строку
            line = file.readline()
            # прерываем цикл, если строка пустая

            if not line:
                parsed_data.append(section)
                break

            if line.find('Function Name:') != -1:

                if section != {}:
                    parsed_data.append(section)

                section = {
                    'name': [],
                    'address': [],
                    'callers': []
                }
                section['name'].append(line.replace("\n", ""))

            elif line.find('Address Range:') != -1:
                left_border_index = line.find(':')
                right_border_index = line.find('\n')

                list_of_address = line[left_border_index +
                                1:right_border_index].split('-')
                list_of_address = [from_16_to_10(el.replace(" ", ""))
                            for el in list_of_address]

                section['address'].append(list_of_address)

            elif line.find('Callers:') != -1:
                pass
            else:
                if line.find('-') == -1:
                    left_border_index = line.find('(')
                    right_border_index = line.find(')')

                    section['callers'].append(from_16_to_10(
                        line[left_border_index+1:right_border_index]))
                    
    return parsed_data

points = []

for list_el in parse_txt_file(txt_path):
    for caller in list_el['callers']:
        points.append((list_el['address'][0][0], caller))

#print(points)

# Количество кластеров
k = 2

# Цвета кластеров
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Инициализируем центры кластеров случайными точками
centers = random.sample(points, k)

# Инициализируем пустые списки для кластеров
clusters = [[] for _ in range(k)]

# Функция расстояния между двумя точками
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 +
                     (point1[1] - point2[1]) ** 2)

# Функция для нахождения ближайшего центра кластера для заданной точки
def closest_center(point):
    min_distance = float('inf')
    closest_center_index = None
    for i in range(k):
        d = distance(point, centers[i])
        if d < min_distance:
            min_distance = d
            closest_center_index = i
    return closest_center_index

# Функция для обновления центров кластеров
def update_centers():
    for i in range(k):
        x = sum(point[0] for point in clusters[i]) / len(clusters[i])
        y = sum(point[1] for point in clusters[i]) / len(clusters[i])
        centers[i] = (x, y)

# Функция для визуализации кластеров
def plot_clusters():
    plt.figure()
    plt.xlabel('To')
    plt.ylabel('From')
    for i in range(k):
        cluster = clusters[i]
        plt.scatter([point[0] for point in cluster],
                    [point[1] for point in cluster],
                    color=colors[i])
        radius = max(distance(point, centers[i]) for point in cluster)
        # Используем условие, чтобы точки строго попадали в круг
        circle = plt.Circle(centers[i], radius + 2, color=colors[i], fill=False)
        for point in cluster:
            if distance(point, centers[i]) > radius:
                print("Warning: point", point, "is outside the circle!")
        plt.gca().add_artist(circle)
    plt.show()

# Алгоритм K-means
while True:
    # Разбиваем точки на кластеры
    for point in points:
        closest_center_index = closest_center(point)
        clusters[closest_center_index].append(point)

    # Если кластеры не изменились, заканчиваем алгоритм
    old_centers = centers.copy()
    update_centers()
    if old_centers == centers:
        break

    # Очищаем списки кластеров
    clusters = [[] for _ in range(k)]

# Визуализируем итоговые кластеры
plot_clusters()

