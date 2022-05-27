from pathlib import Path

import cv2
import imutils

from utils.Enums import FlipType


def readImage(path: Path):
    """
    Получить изображение

    :param path: путь до изображения
    """
    cv2.imread(str(path))


def saveImage(path: Path, image):
    """
    Сохранить изображение

    :param path: путь, куда сохранить изображение
    :param image: изображение для сохранения
    """
    cv2.imwrite(str(path), image)


def showImage(image):
    """Создать новое окно с фотографией"""
    cv2.imshow("img", image)
    cv2.waitKey(0)


def imageToGrayscale(image):
    """Перевод RGB фото к Grayscale"""
    image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image_grayscale


def flipImage(image, flipType: FlipType):
    """
    Отразить фотографию по выбранной оси

    :param image: исходное изображение
    :param flipType: по вертикали; по горизонтали; по обоим осям
    :return: отраженное изображение
    """
    flippedImage = cv2.flip(image, flipType.value)

    return flippedImage


def rotateImage(image, angle: int):
    """
    Повернуть изображение на указанный угол

    :param image: исходное изображение
    :param angle: угол для поворота
    :return: повернутое изображение
    """
    rotatedImage = imutils.rotate_bound(image, angle)

    return rotatedImage


def createStringToWrite(imagePath: Path, availableRects: list):
    """
    Создать строку для записи в файл

    :param imagePath: путь к исходному изображению
    :param availableRects: список прямоугольников на фотографии
    :return: строка с путем к изображению и найденными прямоугольниками
    """
    stringToWrite = str(imagePath)
    if availableRects:
        stringToWrite = " ".join((stringToWrite, str(len(availableRects))))

    for rect in availableRects:
        stringToWrite = " ".join(
            (stringToWrite, str(rect.x), str(rect.y), str(rect.w), str(rect.h)))
    stringToWrite += "\n"

    return stringToWrite


def writeToFile(path: Path, text: str):
    """
    Записать текст в файл

    :param path: конечный путь к файлу
    :param text: текст для записи
    """

    with open(str(path), "a") as f:
        f.write(text)
