# *- coding: utf-8*-

import io

import qrcode

import PIL
import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from urllib.request import urlopen
import os

from goal.settings import STATIC_ROOT


def draw(low_img, headimg, author_name, goal_create_time, goal_content, penalty, two_dimension_link, save_img):

    font = ImageFont.truetype('/var/www/goal/static/images/SourceHanSansCN-Bold.otf', 24)
    #font = ImageFont.truetype('/Users/zhixiangliu/Documents/code/goal/static/images/SourceHanSansCN-Bold.otf', 24)
    im1 = Image.open(low_img)

    width, height = im1.size

    tmp_img = os.path.join('/var/www/goal/static/tmp/', str(time.time()) + '.jpg')
    #tmp_img = os.path.join('/Users/zhixiangliu/Documents/code/goal/static/images', str(time.time()) + '.jpg')

    im2 = convert_img(headimg, tmp_img)

    remove_img_file(tmp_img)

    im3 = create_two_dimension(two_dimension_link)
    #im3 = Image.open(new_png)

    # 在图片上添加文字 1
    draw_handle = ImageDraw.Draw(im1)
    im1.paste(im2, (34, 26))

    draw_handle.text((140, 36), author_name + '定下小目标', (100, 100, 100), font)

    draw_handle.text((140, 75),  str(goal_create_time), (100, 100, 100), font)

    content_font = ImageFont.truetype('/var/www/goal/static/images/SourceHanSansCN-Bold.otf', 74)
    #content_font = ImageFont.truetype('/Users/zhixiangliu/Documents/code/goal/static/images/SourceHanSansCN-Bold.otf', 80)

    w, h = content_font.getsize(goal_content)

    if len(goal_content) > 7:
        goal_content1 = goal_content[0: int(len(goal_content)/2)]
        goal_content2 = goal_content[int(len(goal_content) / 2):]
        w1, h1 = content_font.getsize(goal_content1)
        w2, h2 = content_font.getsize(goal_content2)

        draw_handle.text((width / 2 - w1 / 2, 200), goal_content1, (0, 0, 0), content_font)
        draw_handle.text((width / 2 - w2 / 2, 300), goal_content2, (0, 0, 0), content_font)

    else:
        draw_handle.text((width/2 - w/2, 200), goal_content, (0, 0, 0), content_font)

    if len(penalty) > 6:
        content_font = ImageFont.truetype('/var/www/goal/static/images/SourceHanSansCN-Bold.otf', 58)
    else:
        content_font = ImageFont.truetype('/var/www/goal/static/images/SourceHanSansCN-Bold.otf', 80)

    w, h = content_font.getsize(penalty)

    draw_handle.text((width/2 - w/2, 600), penalty, (0, 0, 0), content_font)

    draw_handle.bitmap((52, height-144), im3, (255, 255, 255))

    draw_handle = ImageDraw.Draw(im1)

    # 保存
    im1.save(save_img)


def draw_xuanyao(low_img, save_img, two_dimension_link):
    im1 = Image.open(low_img)

    width, height = im1.size

    im2 = create_two_dimension(two_dimension_link)

    draw_handle = ImageDraw.Draw(im1)

    draw_handle.bitmap((52, height - 144), im2, (255, 255, 255))

    im1.save(save_img)


def create_two_dimension(two_dimension_link):

    random_str = str(time.time())

    tmp_img = os.path.join(STATIC_ROOT, 'save_images', random_str + '.jpg')
    #tmp_img = os.path.join('/Users/zhixiangliu/Documents/code/goal/static/images', str(time.time()) + '.jpg')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=1,
    )
    qr.add_data(two_dimension_link)
    qr.make(fit=True)

    img = qr.make_image()
    img.save(tmp_img)
    face_image = PIL.Image.open(tmp_img)
    face_image = face_image.resize((115, 115), PIL.Image.ANTIALIAS)

    return face_image


def convert_img(headimg, save_img):
    image_bytes = urlopen(headimg).read()

    data_stream = io.BytesIO(image_bytes)
    print(data_stream)

    im = Image.open(data_stream)
    im.save(save_img)

    card = Image.new("RGBA", (800, 600), (255, 255, 255))
    img = Image.open(save_img).convert("RGBA")
    x, y = img.size
    card.paste(img, (0, 0, x, y))
    card = img.resize((80, 80), PIL.Image.ANTIALIAS)

    return card


def remove_img_file(src):
    try:
        os.remove(src)
    except Exception as ex:
        print('remove file failed, ', ex)


if __name__ == '__main__':
    value_dict = {'1': 1, '2': 3, '3': 2}

    low_img = '/Users/zhixiangliu/Documents/code/goal/static/images/done_dushu.jpg'

    save_img = '/Users/zhixiangliu/Documents/code/goal/static/images/rand.jpg'

    two_dimension_link = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI4NjkxMDg5Mw==&scene=124#wechat_redirect'

    draw_xuanyao(low_img, save_img, two_dimension_link)

    low_img = '/Users/zhixiangliu/Documents/code/goal/static/images/dushu.jpg'
    headimg = 'http://wx.qlogo.cn/mmopen/ajNVdqHZLLCCzGDKibYicjyeVcylKsWQANxnlNxcyZQPFF3ItyUD6iawVcEBXHiadenx57wkqmouqyzIopl4gZVydQ/0'
    author_name = '刘志祥'
    goal_content = '我的微目标'
    penalty = '裸奔'
    two_dim = '/Users/zhixiangliu/Documents/code/goal/static/images/qrcode.jpg'
    save_img = '/Users/zhixiangliu/Documents/code/goal/static/images/rand.jpg'
    goal_create_time = '2016-10-23 10:00:00'
    goal_id = 214
    goal = draw(low_img, headimg, goal_id, author_name, goal_create_time, goal_content, penalty, two_dim, save_img)
    print('')
