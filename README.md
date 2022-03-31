# 1C_task
Нахождение всех пересечений рёбер графа, нарисованного на png  
Программа написана на python и состоит из [основного файла с решением](\main.py) и [файла с геометрическими функциями](\geom.py)
## Решение

С помощью поиска в ширину ищем на черно-белой картинке чёрные точки, и после этого, проходим по соседям только один раз, чтобы уменьшить толщину линий. После рассматриваю все вершины по три, и если они не лежат на одной прямой (с некоторым округлением), одну из них делаем вершиной. В конце, смотрим на все пары вершин и ищем пересечения прямых.  

Программа протестирована на данном нам примере и еще нескольких, чтобы удостовериться в правильности решения.  Можно было добавить пользовательский ввод, но я, к сожалению, не успел.
