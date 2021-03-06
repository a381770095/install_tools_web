#!/usr/bin/env python3

#- * -coding: utf - 8 - * -#@Author: Yang#@ Time: 2017 / 11 / 06 1: 04
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
_letter_cases = "abcdefghjkmnpqrstuvwxy"#小写字母, 去除可能干扰的i, l, o, z
_upper_cases = _letter_cases.upper()# 大写字母
_numbers = ''.join(map(str, range(10)))# 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))


def create_validate_code(size = (200, 40),
                         chars = init_chars,
                         img_type = "png",
                         mode = "RGB",
                         # fg_color = (18, 18, 18),
                         font_size = 32,
                         font_path = './111.ttf',
                         length = 4,
                         draw_lines = True, #是否划干扰线
                         n_line = (1, 5),   #干扰线的条数范围,格式元组,默认为(1, 2)
                         draw_points = True,  # 是否画干扰点
                         point_chance = 1 ):   #干扰点出现的概率,大小范围[0, 100]
    bg_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    fg_color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    width, height = size    # 宽, 高
    img = Image.new(mode, size, bg_color)# 创建图形
    draw = ImageDraw.Draw(img) # 创建画笔


    def get_chars():
        return random.sample(chars,length)

    def create_lines():
        line_num = random.randint(*n_line)# 干扰线条数
        for i in range(line_num): #起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))# 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill = (0, 0, 0))

    def create_points():
        chance = min(100, max(0, int(point_chance)))# 大小限制在[0, 100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill = (0, 0, 0))

    def create_strs():
        c_chars = get_chars()
        strs = ' %s '%' '.join(c_chars)# 每个字符前后以空格隔开
        font = ImageFont.truetype(font_path, font_size)

        font_width, font_height = font.getsize(strs)
        draw.text(((width - font_width) / 2,(height - font_height) / 3),
                  strs,
                  fg_color,
                  font,
                  )
        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()
    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,0.001,
              float(random.randint(1, 2)) / 500]
    # img = img.transform(size, Image.PERSPECTIVE, params)# 创建扭曲
    # img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)# 滤镜, 边界加强（ 阈值更大）

    return img, strs


if __name__ == '__main__':
    img, str = create_validate_code()
    img.save('./test.png', 'png')