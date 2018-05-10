# -*- coding: utf-8 -*-

import cv2

try:
    # Загрузка изображения.
    img_in = cv2.imread('test.jpg', 0)

    # Устранение шумов для того, чтобы легче было искать нужные объекты.
    # Точность регулируется вторым аругментом.
    ret, img_thresh = cv2.threshold(img_in, 150, 255, cv2.THRESH_BINARY)

    # Поиск контуров.
    img_out, contours, hierarchy = cv2.findContours(
        img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    # Списки для разделения контуров на оксиды и сульфиды.
    oxides = []
    sulphides = []

    # Сортировка контуров.
    # Из-за недостатка опыта/знаний подбирал руками числа, поэтому
    # не совсем логичные условия. Может быть, часть проблемы заключена
    # в разрешении изображения.
    for contour in contours:
        approx = cv2.approxPolyDP(
            contour, 0.01*cv2.arcLength(contour, True), True
        )
        area = cv2.contourArea(contour)

        # По идее, в оксиды должны попадать контуры с кол-вом вершин > 8,
        # но на конкретном изображении это не работает. Вполне вероятно, что
        # здесь моя недоработка и выбранный подход не является оптимальным.
        if (len(approx) > 1) and (area < 21):
            oxides.append(contour)
        else:
            sulphides.append(contour)

    # Первый элемент в списке - контур изображения. Не смог обойти это без
    # падения точности контуринга.
    sulphides.pop(0)

    # Расчет долей.
    oxides_to_sulphides = len(oxides) / len(sulphides)
    sulphides_to_oxides = len(sulphides) / len(oxides)

    # Нанесение найденных контуров на оригинальное изображение.
    img_out = cv2.drawContours(img_in, oxides, -1, (255, 255, 255), 1)
    img_out = cv2.drawContours(img_in, sulphides, -1, (0, 255, 255), 1)

    # Нанесение надписей с результатами на изображение.
    # Так сложно, потому что метод putText не распознает \n как спецсимвол.
    to_display = 'Oxides to sulphides: {0};\nSulphides to oxides: {1};'.format(
        round(oxides_to_sulphides, 3), round(sulphides_to_oxides, 3)
    )
    y0, dy = img_in.shape[0] - 30, 20
    for i, line in enumerate(to_display.split('\n')):
        y = y0 + i * dy
        cv2.putText(
            img_out, line, (5, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 0), 1, cv2.LINE_AA
        )

    # Вывод итогового изображения на экран.
    cv2.imshow('This is a test', img_out)
    cv2.waitKey(0)
except Exception as ex:
    print('Whoops, something\'s wrong!\n' + str(ex))
