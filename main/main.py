import os
import time
from pathlib import Path

import cv2

from models.Rectangle import Rectangle
from utils.Enums import Action
from utils.Enums import DefectType, FlipType
from utils.Enums import Tone
from utils.UtiltsFunc import imageToGrayscale, showImage, writeToFile, rotateImage, flipImage, createStringToWrite, \
    saveImage

# ----------------------------------------------------------------------
# Инфо файл, где описано положение всех прямоугольников на каждом фото
infoFile = "info.txt"
backgroundFile = "background.txt"

POSITIVE = 0
NEGATIVE = 0
colorWhite_RGB = (255, 255, 255)
colorWhite_GRAY = 255

defectTypeList = [DefectType.POTHOLE.value, DefectType.CRACK.value]
toneList = [Tone.POSITIVE.value, Tone.NEGATIVE.value]


# ----------------------------------------------------------------------


def getAvailableMaskRectangles(image_defect, image_raw=None):
    """
    Получить список всех доступных(отфильтрованных) прямоугольников

    :param image_defect: фото с дефектом в оттенках серого
    :param image_raw: исходное фото
    """
    # Список доступных прямоугольников
    availableRects = []

    mask = cv2.inRange(image_defect, colorWhite_GRAY, colorWhite_GRAY)

    # Список координат ВСЕХ ТОЧЕК для каждого ДЕФЕКТА
    areas = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(areas) > 0:
        rectanglesList = []

        # Пройти по всем найденным областям
        for area in areas:
            # Получить начальные координаты + ширину и высоту найденной области
            x, y, w, h = cv2.boundingRect(area)
            # Преобразовать найденную область к прямоугольнику
            rectangle = Rectangle(x, y, w, h)

            # Минимально допустимая площадь для занесения их в список допустимых прямоугольников
            if rectangle.area() > 576:
                rectanglesList.append(rectangle)
                # cv2.rectangle(image_raw, (rectangle.x, rectangle.y), (rectangle.x + rectangle.w, rectangle.y + rectangle.h), (0, 0, 255), 1)

        # # TODO DELETE
        # deleteRect = Rectangle(12, 20, 1000, 600)
        # rectanglesList.append(deleteRect)
        # # cv2.rectangle(image_raw, (deleteRect.x, deleteRect.y), (deleteRect.x + deleteRect.w, deleteRect.y + deleteRect.h), (0, 0, 255), 1)
        # # TODO DELETE

        # Пройтись по списку прямоугольников с минимально допустимой площадью
        for rect in rectanglesList:
            """
            Создать список прямоугольников, исключая выбранный, чтобы проверить перекрывает ли этот прямоугольник любой 
            из других
            Пример: [rect1], [rect1, rect2, rect3, rect4, rect5] -> [rect2, rect3, rect4, rect5] 
            """
            validRects = [it for it in rectanglesList if it not in [rect]]

            # Если текущий прямоугольник перекрывается хоть одним, то не включать его в финальный список
            overlapped = False
            for challengerRect in validRects:
                if rect.isOverlapped(challengerRect):
                    overlapped = True

            if not overlapped:
                availableRects.append(rect)
                cv2.rectangle(image_raw, (rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h), (0, 0, 255), 1)

    # if image_raw is not None:
    #     showImage(image_raw)
    return availableRects


def getPathToSave(defectType: DefectType, tone: Tone, createSubDir: bool = True):
    """
    Получить:

    • Конечную папку для сохранения фотографии

    • Номер последнего сохраненного элемента

    :param defectType: Тип дефекта
    :param tone: Оттенок дефекта (позитивный, негативный)
    :param createSubDir: Создавать подпапку для фотографий
    :return: конечный путь и номер последнего созданного элемента
    """
    # Директория с дефектом: ..\CRACK\negative
    directory = Path(dataset_directory).joinpath(defectType.value, tone.value)

    # Если не существует, то создать
    if not directory.is_dir():
        os.makedirs(str(directory))

    # Количество созданный папок
    subDir_number = len(os.listdir(directory))

    if createSubDir:
        # Поддиректория с дефектом: ..\CRACK\positive\0\ (0_CRACK.png, 0_RAW.png)
        subDir = Path(directory).joinpath(str(subDir_number))
        # Если не существует, то создать
        if not subDir.is_dir():
            os.makedirs(str(subDir))
        return subDir, subDir_number
    else:
        return directory, subDir_number


def savePhotosByDefect(availableRects: list, defectType: DefectType, defectImage, rawImage):
    """
    Сохранить фото в зависимости от дефекта

    :param availableRects: доступные прямоугольники на фотографии
    :param defectType: тип дефекта
    :param defectImage: дефектное изображение
    :param rawImage: исходное изображение
    """
    finalDirPath: str
    element_lastNumber: int

    if availableRects:
        finalDirPath, element_lastNumber = getPathToSave(defectType=defectType,
                                                         tone=Tone.POSITIVE,
                                                         createSubDir=True)

        # Название фото с дефектом
        new_defectImage_name = "{}_{}.png".format(element_lastNumber, defectType.value)
        # Название фото без дефекта
        new_rawImage_name = "{}_{}.png".format(element_lastNumber, DefectType.RAW.value)

        # Сохранить фото с дефектом
        # cv2.imwrite(Path(finalDirPath).joinpath(new_defectImage_name), defectImage)
        saveImage(Path(finalDirPath).joinpath(new_defectImage_name), defectImage)
        # Сохранить фото без дефекта
        # cv2.imwrite(Path(finalDirPath).joinpath(new_rawImage_name), rawImage)
        saveImage(Path(finalDirPath).joinpath(new_rawImage_name), rawImage)

    # Сохранить фото (исходную) в папку без дефектов
    else:
        finalDirPath, element_lastNumber = getPathToSave(defectType=defectType,
                                                         tone=Tone.NEGATIVE,
                                                         createSubDir=False)

        # Название фото без дефекта
        new_rawImage_name = "{}_{}.png".format(element_lastNumber, DefectType.RAW.value)

        # Сохранить фото без дефекта
        # cv2.imwrite(Path(finalDirPath).joinpath(new_rawImage_name), rawImage)
        saveImage(Path(finalDirPath).joinpath(new_rawImage_name), rawImage)


def changeAndSaveImage(defectType: DefectType, defectImage, rawImage, action: Action):
    """
    Повернуть и сохранить фотографию

    :param defectType: тип дефекта
    :param defectImage: дефектное изображение
    :param rawImage: исходное изображение
    :param action
    """

    newDefectImage = None
    newRawImage = None

    if action == Action.ROTATE:
        # Повернуть дефектное изображение
        newDefectImage = rotateImage(defectImage, 90)
        # Повернуть исходное изображение
        newRawImage = rotateImage(rawImage, 90)
    elif action == Action.FLIP:
        # Отобразить дефектное изображение по горизонтали
        newDefectImage = flipImage(defectImage, FlipType.HORIZONTAL)
        # Отобразить исходное изображение по горизонтали
        newRawImage = flipImage(rawImage, FlipType.HORIZONTAL)

    if newDefectImage is None or newRawImage is None:
        print("Change image failed")
        exit(0)

    # Перевод дефектного изображения в оттенки серого
    newDefectImage_grayscale = imageToGrayscale(newDefectImage)
    # Получить все доступные прямоугольники на дефектном изображении
    availableNewDefectRects = getAvailableMaskRectangles(image_defect=newDefectImage_grayscale)

    # Сохранить фото
    savePhotosByDefect(availableRects=availableNewDefectRects,
                       defectType=defectType,
                       defectImage=newDefectImage,
                       rawImage=newRawImage)


def appendToTextFile(directoryToSave: Path, filename: str, relativeImagePath: Path, availableRects: list = []):
    """
    Сохранить строку в указанный файл
    
    :param directoryToSave: директория для сохранения файла
    :param filename: название файла, в который добавляется строка
    :param relativeImagePath: относительный путь к изображению
    :param availableRects: все имеющиеся прямоугольники на изображении
    """
    stringToWrite = createStringToWrite(relativeImagePath, availableRects)

    path = directoryToSave.joinpath(filename)
    writeToFile(path, stringToWrite)


def splitRawImages(imageDirectoryPath):
    """
    Разделить фото на позитивные(есть дефекты) и негативные(нет дефектов)

    :param путь к исходным фотографиям
    """

    crackImage = None
    potholeImage = None
    rawImage = None
    availableCrackRects = []
    availablePotholesRects = []

    # Пройтись по всем фотографиям в папке
    for image in os.listdir(imageDirectoryPath):
        imagePath = os.path.join(imageDirectoryPath, image)

        # Проверить присутствуют ли дефекты на фотографии с трещинами
        if image.find(DefectType.CRACK.value) != -1:
            crackImage = cv2.imread(imagePath)
            availableCrackRects = getAvailableMaskRectangles(image_defect=imageToGrayscale(crackImage))

        # Проверить присутствуют ли дефекты на фотографии с ямами
        elif image.find(DefectType.POTHOLE.value) != -1:
            potholeImage = cv2.imread(imagePath)
            availablePotholesRects = getAvailableMaskRectangles(image_defect=imageToGrayscale(potholeImage))

        # Получить оригинальную фотографию
        elif image.find(DefectType.RAW.value) != -1:
            rawImage = cv2.imread(imagePath)

    if rawImage is None:
        print("Raw image not found")
        return
    else:
        # ---ТРЕЩИНЫ---
        # Сохранить фото трещин в новую папку
        if crackImage is not None:
            savePhotosByDefect(availableRects=availableCrackRects,
                               defectType=DefectType.CRACK,
                               defectImage=crackImage,
                               rawImage=rawImage)

            if createRotatedCrackImages:
                changeAndSaveImage(defectType=DefectType.CRACK,
                                   defectImage=crackImage,
                                   rawImage=rawImage,
                                   action=Action.ROTATE)

            if createFlippedCrackImages:
                changeAndSaveImage(defectType=DefectType.CRACK,
                                   defectImage=crackImage,
                                   rawImage=rawImage,
                                   action=Action.FLIP)

        # ---ЯМЫ---
        # Сохранить фото ям в новую папку
        if potholeImage is not None:
            savePhotosByDefect(availableRects=availablePotholesRects,
                               defectType=DefectType.POTHOLE,
                               defectImage=potholeImage,
                               rawImage=rawImage)

            if createRotatedPotholeImages:
                changeAndSaveImage(defectType=DefectType.POTHOLE,
                                   defectImage=potholeImage,
                                   rawImage=rawImage,
                                   action=Action.ROTATE)

            if createFlippedPotholeImages:
                changeAndSaveImage(defectType=DefectType.POTHOLE,
                                   defectImage=potholeImage,
                                   rawImage=rawImage,
                                   action=Action.FLIP)

    print("Time split iteration: {}".format(time.time() - time_start))


def iterateOverRawDirectory(directoryPath: Path):
    """
    Пройтись по директориям в исходном датасете

    :param directoryPath: путь к исходному датасету
    """
    for directory in directoryPath.iterdir():

        if directory.is_dir():
            iterateOverRawDirectory(directory)
        else:
            splitRawImages(directoryPath)
            # Папка с фото найдена, вернуться на директорию выше
            return


def iterateOverFilteredDirectory(path: Path, appendToInfoFile: bool):
    """
    Пройтись по директории с отфильтрованными изображениями

    :param path: путь к директории с отфильтрованными изображениями
    :param appendToInfoFile: записывать информацию о фото в текстовый файл
    """

    # Пройтись по директориям с дефектами (..\CRACK, ..\POTHOLE)
    for defectPath in path.iterdir():
        # Название папки с дефектом (CRACK, POTHOLE)
        defectType = str(defectPath.relative_to(dataset_directory))
        # Если дефект один из списка доступных
        if defectType not in defectTypeList:
            print("Unexpected defect type while iterate filtered directory")
        else:
            # Пройтись по директориям с оттенками дефекта (..\CRACK\positive, ..\CRACK\negative)
            for tonePath in defectPath.iterdir():
                # Название папки с оттенками (positive, negative)
                tone = str(tonePath.relative_to(defectPath))
                # Если оттенок один из списка доступных
                if tone not in toneList:
                    print("Unexpected tone while iterate filtered directory")
                else:
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # Если папка с негативными (без дефектов) изображениями (negative)
                    if tone == Tone.NEGATIVE.value:
                        # iterateOverImageDirectory(directoryToIterate=tonePath,
                        #                           directoryToSave=defectPath,
                        #                           appendToInfoFile=appendToInfoFile,
                        #                           tone=tone)

                        for imagePath in tonePath.iterdir():
                            imageName = imagePath.relative_to(tonePath)

                            rawImagePath = None
                            # Если исходное изображение найдено
                            if not str(imageName.stem).endswith(DefectType.RAW.value):
                                print("Raw image not found in negative folder")
                            else:
                                # Исходное изображение
                                # rawImage = cv2.imread(str(imageName))
                                rawImagePath = imagePath

                                # Добавить информацию о изображении в текстовый файл?
                                if appendToInfoFile and rawImagePath is not None:
                                    # Относительный путь к изображению
                                    relativeImagePath = imagePath.relative_to(defectPath)
                                    appendToTextFile(directoryToSave=defectPath,
                                                     filename=backgroundFile,
                                                     relativeImagePath=rawImagePath)

                            print("Time iteration image directory: {}".format(time.time() - time_start))
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                    # ----------------------------------------------------------------------------
                    # Если папка с позитивными (с дефектами) изображениями (positive)
                    elif tone == Tone.POSITIVE.value:
                        # Пройтись по папкам с изображениями (..\CRACK\positive\0\, ..\CRACK\positive\1\,...)
                        # for imageDirectoryPath in tonePath.iterdir():
                        #     iterateOverImageDirectory(directoryToIterate=imageDirectoryPath,
                        #                               directoryToSave=defectPath,
                        #                               appendToInfoFile=appendToInfoFile,
                        #                               tone=tone)

                        for imageDirectoryPath in tonePath.iterdir():
                            rawImagePath = None
                            defectImagePath = None
                            for imagePath in imageDirectoryPath.iterdir():
                                imageName = imagePath.relative_to(imageDirectoryPath)

                                # Если изображение с дефектом найдено
                                if str(imageName.stem).endswith((DefectType.CRACK.value, DefectType.POTHOLE.value)):
                                    # Дефектное изображение
                                    defectImagePath = imagePath

                                if str(imageName.stem).endswith(DefectType.RAW.value):
                                    # Исходное изображение
                                    rawImagePath = imagePath

                            if (defectImagePath is not None) and (rawImagePath is not None):
                                defectImage = cv2.imread(str(defectImagePath))
                                rawImage = cv2.imread(str(rawImagePath))

                                # Добавить информацию о изображении в текстовый файл?
                                if appendToInfoFile:
                                    defectImage_grayscale = imageToGrayscale(defectImage)
                                    availableRects = getAvailableMaskRectangles(image_defect=defectImage_grayscale)

                                    # Относительный путь к изображению
                                    relativeImagePath = rawImagePath.relative_to(defectPath)
                                    appendToTextFile(directoryToSave=defectPath,
                                                     filename=infoFile,
                                                     relativeImagePath=relativeImagePath,
                                                     availableRects=availableRects)

                            print("Time iteration image directory: {}".format(time.time() - time_start))
                    # ----------------------------------------------------------------------------

                print("Time iteration over filtered directory: {}".format(time.time() - time_start))


def main():
    # Разделить фото на позитивные(есть дефекты) и негативные(нет дефектов)
    iterateOverRawDirectory(Path(datasetRaw_directory))

    # Создать текстовые файлы с позитивными и негативными изображениями
    iterateOverFilteredDirectory(path=Path(dataset_directory), appendToInfoFile=True)


def showPotholesOnImage(image):
    cascade_potholes = cv2.CascadeClassifier("cascade_v4_s25.xml")

    areas = cascade_potholes.detectMultiScale(image)

    rects = []
    if len(areas) > 0:
        for area in areas:
            # rect = Rectangle(area[0], area[1], area[2], area[3])
            # cv2.rectangle(image, (rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h), (0, 0, 255), 1)
            rect = Rectangle(area[0], area[1], area[2], area[3])
            if rect.area() > 10000:
                rects.append(rect)

    availableRects = []
    if rects:
        for rect in rects:
            validRects = [it for it in rects if it not in [rect]]

            # Если текущий прямоугольник перекрывается хоть одним, то не включать его в финальный список
            overlapped = False
            for challengerRect in validRects:
                if rect.isOverlapped(challengerRect):
                    overlapped = True

            if not overlapped:
                availableRects.append(rect)
                cv2.rectangle(image, (rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h), (0, 0, 255), 2)

    showImage(image)


def test():
    image = cv2.imread("test1.jpg")


    # # https://ruwest.ru/upload/iblock/b38/b38002b60e8d4889179154af15fa8c67.jpg
    # # https://dorogi-onf.ru/media/feedback/2017/07/16/20170605_213640.jpg.0x800_q85_crop.jpg
    # url = "https://dorogi-onf.ru/media/feedback/2017/07/16/20170605_213640.jpg.0x800_q85_crop.jpg"
    # req = urlopen(url)
    # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    # image = cv2.imdecode(arr, -1)

    if image is None:
        print("Image not found in folder")
        return

    showPotholesOnImage(image)



if __name__ == '__main__':
    time_start = time.time()

    # Исходная папка с фотографиями и масками
    datasetRaw_directory = "G:\\4thCOURSE\\Diploma\\DATA\\Dataset_raw\\"
    # Конечная папка с разделенными фотографиями
    dataset_directory = "G:\\4thCOURSE\\Diploma\\DATA\\Dataset\\"
    if not Path(dataset_directory).is_dir():
        os.mkdir(dataset_directory)

    # Создавать повернутые фотографии трещин
    createRotatedCrackImages = True
    # Создавать повернутые фотографии трещин
    createFlippedCrackImages = True
    # Создавать повернутые фотографии ям
    createRotatedPotholeImages = True
    # Создавать повернутые фотографии ям
    createFlippedPotholeImages = True

    # main()

    test()

    print("---FINISHED after {}---".format(time.time() - time_start))
