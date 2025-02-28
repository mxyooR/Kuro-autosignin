import os
import random

import cv2
import torch
import ddddocr
import open_clip
import numpy as np
import pydash as _
from loguru import logger
from PIL import Image, ImageFile
from sentence_transformers import util

from utils import pathUtils
from utils.pathUtils import TMP_BACKGROUND_PATH, PICTURE_PATH, TMP_PATH, PROJECT_PATH

# image processing model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, x, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-16-plus-240",
    pretrained="laion400m_e32",
    cache_dir=os.path.join(PROJECT_PATH, "cache"),
)
model.to(device)


# 将RGBA改为RGB（有些图片只有透明度没有颜色，所以需要处理下）
def qweada(oriPath, dstPath):
    try:
        img2 = cv2.imdecode(np.fromfile(oriPath, dtype=np.uint8), -1)

        b, g, r, a = cv2.split(img2)
        aa = a[:, :, np.newaxis]
        new = np.concatenate((aa, aa, aa), axis=2)
        im = Image.fromarray(new)
        im.save(dstPath)
    except:
        return


# 分割图片
def cut_image(image: ImageFile, point: list, dstPath):
    images = image.crop(tuple(point))
    images.save(dstPath, "PNG")


def clean_background():
    backgroundList = os.listdir(TMP_BACKGROUND_PATH)
    for background in backgroundList:
        backgroundPath = os.path.join(TMP_BACKGROUND_PATH, background)
        os.remove(backgroundPath)


def process_picture():
    clean_background()
    # 处理题目图片
    for i in range(3):
        oriPath = os.path.join(PICTURE_PATH, f"que_{i}.png")
        dstPath = os.path.join(TMP_PATH, f"que_{i}.png")
        pathUtils.mk_dir(dstPath)
        qweada(oriPath, dstPath)

    # 切割图片
    det = ddddocr.DdddOcr(det=True, ocr=False, show_ad=False)
    target_path = os.path.join(PICTURE_PATH, f"target.png")

    with open(target_path, "rb") as f:
        image = f.read()

    bboxes = det.detection(image)
    target_img = Image.open(target_path)
    for bbox in bboxes:
        bboxDstPath = os.path.join(
            TMP_PATH, "background", f"{'_'.join([str(i) for i in bbox])}.png"
        )
        pathUtils.mk_dir(bboxDstPath)
        cut_image(target_img, bbox, bboxDstPath)


def imageEncoder(img):
    img1 = Image.fromarray(img).convert("RGB")
    img1 = preprocess(img1).unsqueeze(0).to(device)
    img1 = model.encode_image(img1)
    return img1


# 计算相似度
def generateScore(image1, image2):
    test_img = cv2.imread(image1, cv2.IMREAD_UNCHANGED)
    data_img = cv2.imread(image2, cv2.IMREAD_UNCHANGED)
    img1 = imageEncoder(test_img)
    img2 = imageEncoder(data_img)
    cos_scores = util.pytorch_cos_sim(img1, img2)
    score = round(float(cos_scores[0][0]) * 100, 2)
    return score


def cal_score(quePath):
    logger.debug("Start calculate")
    backgroundList = os.listdir(TMP_BACKGROUND_PATH)
    items = []
    for background in backgroundList:
        backgroundPath = os.path.join(TMP_BACKGROUND_PATH, background)
        score = generateScore(quePath, backgroundPath)
        item = {"corrd": background.replace(".png", "").split("_"), "score": score}
        logger.debug(item)
        items.append(item)

    aim_cord = [int(i) for i in _.max_by(items, "score").get("corrd")]
    logger.info(f"aim_cord ==> {aim_cord}")
    return aim_cord


def random_select_point(corrd):
    x_distance = (corrd[2] - corrd[0]) // 2
    y_distance = (corrd[3] - corrd[1]) // 2
    centerPoint = [
        corrd[0] + x_distance + random.random(),
        corrd[1] + y_distance + +random.random(),
    ]
    return centerPoint


def get_points():
    return [
        random_select_point(cal_score(os.path.join(TMP_PATH, "que_0.png"))),
        random_select_point(cal_score(os.path.join(TMP_PATH, "que_1.png"))),
        random_select_point(cal_score(os.path.join(TMP_PATH, "que_2.png"))),
    ]
