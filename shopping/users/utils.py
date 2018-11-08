'''
author:梁晓伟
datetime:2018/11/7 9:13
Desc: utils
'''
import hashlib
import hmac
import string
import random
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter


from django.shortcuts import render
from django.conf import settings


# 工具模块
# 判断用户是否登录
def requirelogin(fn):
    def inner(request, *args, **kwargs):
        if request.session.has_key("loginUser"):
            # 此时用户登录了，正常运行，我们不参与
            return fn(request, *args, **kwargs)
        else:
            return render(request, "blog/login.html", {"msg": "你没有登录，该页面需要登录，请先登录！！"})
    return inner


def md5_hashlib(key):
    md5 = hashlib.md5(key.encode("utf-8"))
    md5.update(settings.HASH_KEY.encode("utf-8"))
    return md5.hexdigest()


def md5_hmac(key):
    md5 = hmac.new(key.encode("utf-8"), settings.HASH_KEY.encode("utf-8"), "MD5")
    return md5.hexdigest()


# 生成四位的随机字符串。
def getRandomChar(count=4):
    ran = string.ascii_lowercase + string.ascii_uppercase + string.digits
    char = ""
    for i in range(count):
        char += random.choice(ran)
    return char


# 生成一个随机的RGB颜色
def getRandomColor():
    return (random.randint(50,150), random.randint(50,150), random.randint(50,150))


def create_code():
    # 创建图片，模式，大小，背景色
    img = Image.new("RGB", (120, 30), (255, 255, 255))
    # 创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype('simfang.ttf', 25)

    code = getRandomChar()
    # 将生成的字符画在画布上
    for t in range(4):
        draw.text((30*t+5, 0), code[t], getRandomColor(), font)

    # 生成干扰点 增加识别的难度
    for _ in range(random.randint(0, 100)):
        # 位置颜色
        draw.point((random.randint(0, 120), random.randint(0, 30)), fill=getRandomColor())

    # 使用模糊滤镜使图片模糊
    # img = img.filter(ImageFilter.BLUR)
    return img, code


def removeHtml(content):
    pattern = r'</?(.*?)>'
    return re.sub(pattern, "", content)