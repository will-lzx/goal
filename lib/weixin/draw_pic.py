#*- coding: utf-8*-
import io

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from urllib.request import urlopen


def draw(low_img, headimg, author_name, goal_create_time, goal_content, penalty, two_dimension, save_img):

    font = ImageFont.truetype('/var/www/goal/static/images/SourceHanSansCN-Bold.otf', 24)
    im1 = Image.open(low_img)

    width, height = im1.size

    image_bytes = urlopen(headimg).read()

    data_stream = io.BytesIO(image_bytes)

    im2 = Image.open(data_stream)

    im2 = im2.resize((80, 80), PIL.Image.ANTIALIAS)

    im2_width, im2_height = im2.size

    #new_png = transparent('/Users/zhixiangliu/Documents/code/goal/static/images/getqrcode.png', '/Users/zhixiangliu/Documents/code/goal/static/images/getqrcode2.png')

    new_png = create_two_dimension(two_dimension)
    im3 = Image.open(new_png)

    # 在图片上添加文字 1
    draw_handle = ImageDraw.Draw(im1)
    draw_handle.bitmap((20, 20), im2, (0, 0, 0))

    draw_handle.text((130, 38), author_name + '定下小目标', (0, 0, 0), font)

    draw_handle.text((130, 75),  str(goal_create_time), (0, 0, 0), font)

    content_font = ImageFont.truetype('/var/www/goal/static/images/SourceHanSansCN-Bold.otf', 80)

    w, h = content_font.getsize(goal_content)
    draw_handle.text((width/2 - w/2, 200), goal_content, (0, 0, 0), content_font)

    w, h = content_font.getsize(penalty)
    draw_handle.text((width/2 - w/2, 650), penalty, (0, 0, 0), content_font)

    draw_handle.bitmap((52, height-152), im3, (0, 0, 0))

    draw_handle = ImageDraw.Draw(im1)

    # 保存
    im1.save(save_img)


def create_two_dimension(save_img):
    import qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=1,
    )
    qr.add_data("http://182.61.21.208/weixin/create1/")
    qr.make(fit=True)

    img = qr.make_image()
    img.save(save_img)
    face_image = PIL.Image.open(save_img)
    face_image = face_image.resize((115, 115), PIL.Image.ANTIALIAS)
    face_image.save(save_img)

    return save_img


if __name__ == '__main__':
    low_img = '/Users/zhixiangliu/Documents/code/goal/static/images/kanshu.jpg'
    headimg = '/Users/zhixiangliu/Documents/code/goal/static/images/shengji.png'
    author_name = '刘志祥'
    goal_content = '我的微目标'
    penalty = '裸奔'
    two_dim = '/Users/zhixiangliu/Documents/code/goal/static/images/qrcode.jpg'
    save_img = '/Users/zhixiangliu/Documents/code/goal/static/images/rand.jpg'
    goal_create_time = '2016-10-23 10:00:00'
    goal = draw(low_img, headimg, author_name, goal_create_time, goal_content, penalty, two_dim, save_img)
    print('')
