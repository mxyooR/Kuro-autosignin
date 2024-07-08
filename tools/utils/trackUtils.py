# -*- coding: utf-8 -*-
import random

from loguru import logger


def __ease_out_expo(sep):
    if sep == 1:
        return 1
    else:
        return 1 - pow(2, -10 * sep)


def GetSlideTrackTime(distance: int):
    """
    According to the distance , generating the track and get the time
    :param distance: The distance of this slide
    :return: The time of this slide
    """

    if not isinstance(distance, int) or distance < 0:
        raise ValueError(f"distance类型必须是大于等于0的整数: distance: {distance}, type: {type(distance)}")

    slideTrack = [
        [random.randint(-50, -10), random.randint(-50, -10), 0],
        [0, 0, 0],
    ]

    count = 30 + int(distance / 2)
    # Init slice time
    t = random.randint(50, 100)

    _x = 0
    _y = 0
    for i in range(count):
        # Distance of slice
        x = round(__ease_out_expo(i / count) * distance)
        # time of slice
        t += random.randint(10, 20)
        if x == _x:
            continue
        slideTrack.append([x, _y, t])
        _x = x
    slideTrack.append(slideTrack[-1])
    logger.debug(f'Get trackInfo ==> {slideTrack}')
    return slideTrack[-1][-1]