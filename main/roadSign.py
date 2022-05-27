import json
import time
from pathlib import Path

import cv2

from models.Rectangle import Rectangle
from utils.UtiltsFunc import showImage


def function(json_object, name):
    return [obj for obj in json_object if obj['objects'] == name][0]['points']

def main():
    dataset_directory = Path("G:\\4thCOURSE\\Diploma\\DATA\\RoadSignDataset\\VID_20220514_164632.mp4\\ann\\")
    for annotation in dataset_directory.iterdir():
        with open(annotation, "r") as rf:
            data = json.load(rf)

            objects = "objects"
            if objects not in data:
                print("Key {} not exist".format(objects))
                return

            for itemKeys, itemValues in data.items():
                if itemKeys == objects:

                    for objectsValues in itemValues:
                        for objectKeys, objectValues in objectsValues.items():
                            if objectKeys == "points":
                                for pointsKeys, pointsValues in objectValues.items():
                                    if pointsKeys == "exterior":
                                        x, y = pointsValues[0]
                                        wx, hy = pointsValues[1]

                                        w = wx - x
                                        h = hy - y
                                        # for corner in pointsValues:
                                        #     for point in corner:
                                        #         print(point, end=" ")

                                        print(x, y, w, h)

    # dataset_directory = Path("G:\\4thCOURSE\\Diploma\\DATA\\RoadSignDataset\\VID_20220514_164632.mp4\\img\\")
    # for image in dataset_directory.iterdir():
    #     print(image)

    """
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00000.png 1 535 395 405 237
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00025.png 1 542 445 452 291
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00050.png 1 664 382 462 300
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00075.png 1 763 285 425 288
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00100.png 1 804 314 426 319
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00125.png 1 733 227 438 369
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00150.png 1 807 155 464 470
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00175.png 1 749 241 567 576
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00200.png 1 643 416 623 563
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00225.png 1 730 453 581 481
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00250.png 1 721 454 452 363
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00275.png 1 734 505 388 280
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00300.png 1 613 403 444 211
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00325.png 1 529 340 471 201
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00350.png 1 554 421 512 285
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00375.png 1 609 418 597 340
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00400.png 1 756 367 477 427
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00425.png 1 609 408 507 496
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00450.png 1 613 445 506 326
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00475.png 1 700 385 483 271
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00500.png 1 865 429 449 282
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00525.png 1 928 451 487 265
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00550.png 1 869 374 502 294
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00575.png 1 813 308 581 386
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00600.png 1 826 385 552 428
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00625.png 1 736 402 494 424
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00650.png 1 765 399 494 392
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00675.png 1 802 331 488 328
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00700.png 1 752 367 457 323
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00725.png 1 752 437 392 310
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00750.png 1 732 463 423 264
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00775.png 1 708 320 483 216
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00800.png 1 638 331 485 221
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00825.png 1 804 346 462 228
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00850.png 1 870 321 464 239
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00875.png 1 774 408 371 228
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00900.png 1 852 343 331 212
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00925.png 1 893 328 353 255
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00950.png 1 827 350 364 275
    G:\4thCOURSE\Diploma\DATA\RoadSignDataset\VID_20220514_164632.mp4\img\frame_00975.png 1 758 341 378 268
    """


def detect():
    # url = "https://carnovato.ru/wp-content/uploads/2014/07/znak-avarijnoj-ostanovki-novogo-obrazca-2.jpg"
    # req = urlopen(url)
    # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    # image = cv2.imdecode(arr, -1)
    image = cv2.imread("roadsign.png")

    cascade_roadsign = cv2.CascadeClassifier("cascade_roadsign_v3.xml")

    areas = cascade_roadsign.detectMultiScale(image)
    if len(areas) > 0:
        for area in areas:
            rect = Rectangle(area[0], area[1], area[2], area[3])
            cv2.rectangle(image, (rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h), (0, 0, 255), 1)

    showImage(image)


if __name__ == '__main__':
    t_start = time.time()

    # main()
    detect()

    print("Time spent: {}".format(time.time() - t_start))
