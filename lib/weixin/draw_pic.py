import PIL
import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


def draw(low_img, headimg, author_name, goal_content, penalty, two_dimension, save_img):
    # 设置字体，如果没有，也可以不设置
    # font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 13)
    im1 = Image.open(low_img)

    im2 = Image.open(headimg)

    im3 = Image.open('/var/www/goal/static/images/getqrcode.jpeg')

    # 在图片上添加文字 1
    draw_handle = ImageDraw.Draw(im1)
    draw_handle.bitmap((200, 600), im2, (255, 255, 0))

    draw_handle.text((600, 800), author_name + "的小目标", (255, 255, 0))
    draw_handle.text((700, 800), goal_content, (255, 255, 0))

    draw_handle.text((800, 800), '如完不成则自罚', (255, 255, 0))

    draw_handle.text((900, 800), penalty, (255, 255, 0))

    draw_handle.bitmap((1000, 800), im3, (255, 255, 0))

    show_content1 = '长按识别二维码吗围观监督TA的小目标'

    draw_handle.text((1200, 800), show_content1, (255, 255, 0))

    show_content2 = '世界会向那些有目标和远见的人让路'

    draw_handle.text((1400, 800), show_content2, (255, 255, 0))

    draw_handle = ImageDraw.Draw(im1)

    # 保存
    im1.save(save_img)