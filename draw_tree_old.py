from PIL import Image, ImageDraw, ImageFont
import io
import base64


def scale(image, text_x_gain, text_y_gain, text_x_upper_label, text_y_upper_label, text_x_bottom_label, text_y_bottom_label, text_x_upper_proba, text_y_upper_proba, text_x_bottom_proba, text_y_bottom_proba, method=Image.ANTIALIAS):
    width, height = image.size
    offsetx = offset_x(text_x_gain, text_x_upper_label, text_x_bottom_label)
    offsety = offset_y(text_y_upper_label, text_y_bottom_label)
    back = Image.new(
        "RGBA", (width + offsetx, height + offsety), (255, 255, 255, 0))
    #print("a", text_x_gain + 50)
    #print("b", int(text_y_upper_label) / 2 + 10)

    back.paste(image, (text_x_gain + 50, int(text_y_upper_label) // 2 + 10))
    return back


def max_text_width(text):
    font = ImageFont.truetype("static/fonts/helvetica-neue-bold.ttf", 16, encoding="utf-8")
    max_width = 0
    lines = text.split("\n")
    for i in range(len(lines)):
        width = font.getsize(lines[i])[0]
        if width > max_width:
            max_width = width
    return max_width


def text_height(text):
    font = ImageFont.truetype("static/fonts/helvetica-neue-bold.ttf", 16, encoding="utf-8")
    height = 0
    lines = text.split("\n")
    for i in range(len(lines)):
        height += font.getsize(lines[i])[1]
    height += 7 * (len(lines) - 1)
    return height


def offset_x(text_x_gain, text_x_upper_label, text_x_bottom_label):
    offset = text_x_gain + 100
    if text_x_upper_label > text_x_bottom_label:
        offset += text_x_upper_label
    else:
        offset += text_x_bottom_label
    return offset


def offset_y(text_y_upper_label, text_y_bottom_label):
    offset = int(text_y_upper_label / 2) + int(text_y_bottom_label / 2) + 20
    return offset


def draw(gain, upper_label, bottom_label, upper_proba, bottom_proba, assess_type):
    
    gain = str(gain)
   

    upper_label = str(upper_label)
    bottom_label = str(bottom_label)
    upper_proba = str(upper_proba)
    bottom_proba = str(bottom_proba)
    imgdata = io.BytesIO()
    tree = Image.open('static/img/tree_choice.png').convert('RGBA')
    font = ImageFont.truetype("static/fonts/helvetica-neue-bold.ttf", 16, encoding="utf-8")
    font2 = ImageFont.truetype("static/fonts/helvetica-neue-bold.ttf", 24, encoding="utf-8")
    text_x_gain = max_text_width(gain)
    #print([text_x_gain])
    text_y_gain = text_height(gain)
    text_x_upper_label = max_text_width(upper_label)
    text_y_upper_label = text_height(upper_label)
    text_x_bottom_label = max_text_width(bottom_label)
    text_y_bottom_label = text_height(bottom_label)
    text_x_upper_proba = font.getsize(upper_proba)[0]
    text_y_upper_proba = font.getsize(upper_proba)[1]
    text_x_bottom_proba = font.getsize(bottom_proba)[0]
    text_y_bottom_proba = font.getsize(bottom_proba)[1]
    width, height = tree.size
    draw = ImageDraw.Draw(tree)
    if (assess_type == "PE" or assess_type == "CE" or assess_type == "CE_PV"):
        draw.text((200, 90), "B", font=font2, fill=(0,0,0,255))
    elif (assess_type == "LE_left"):
        draw.text((200, 90), "A", font=font2, fill=(0,0,0,255))
    elif (assess_type == "LE_right"):
        draw.text((200, 90), "B", font=font2, fill=(0,0,0,255))
    x = 190
    y = 15
    if (assess_type == "PE" or assess_type == "LE_left"):
        draw.text((x, y), upper_proba, font=font, fill=(255,0,0,255))
    else:
        draw.text((x, y), upper_proba, font=font, fill=(0,0,0,255))
    x = 190
    y = height - text_y_bottom_proba - 15
    draw.text((x, y), bottom_proba, font=font, fill=(0,0,0,255))
    tree = scale(tree, text_x_gain, text_y_gain, text_x_upper_label, text_y_upper_label, text_x_bottom_label,
                 text_y_bottom_label, text_x_upper_proba, text_y_upper_proba, text_x_bottom_proba, text_y_bottom_proba)
    draw = ImageDraw.Draw(tree)
    offsetx = offset_x(text_x_gain, text_x_upper_label, text_x_bottom_label)
    offsety = offset_y(text_y_upper_label, text_y_bottom_label)
    if (assess_type == "PE" or assess_type == "CE" or assess_type == "CE_PV"):
        draw.text((22, 0), "A", font=font2, fill=(0,0,0,255))
    x = 5
    y = int((height + offsety - text_y_gain) / 2)
    if (assess_type == "CE" or assess_type == "CE_PV"):
        draw.text((x, y), gain.decode("utf-8"), font=font, fill=(255,0,0,255))
    else:
        #print(([gain]))
        #print([gain_enc])
        draw.text((x, y), gain, font=font, fill=(0,0,0,255))        #        draw.text((x, y), gain.decode("utf-8"), font=font, fill=(0,0,0,255))

    if (assess_type == "PE" or assess_type == "CE" or assess_type == "CE_PV"):
        x=5
        y+=text_y_gain
        draw.text((x, y), " \nwith certainty", font=font, fill=(0,0,0,255))
    x = width + offsetx - text_x_upper_label - 50
    y = 10
    draw.text((x, y), upper_label, font=font, fill=(0,0,0,255))
    #    draw.text((x, y), upper_label.decode("utf-8"), font=font, fill=(0,0,0,255))

    x = width + offsetx - text_x_bottom_label - 50
    y = height + offsety - text_y_bottom_label - 10
    draw.text((x, y), bottom_label, font=font, fill=(0,0,0,255))
    #draw.text((x, y), bottom_label.decode("utf-8"), font=font, fill=(0,0,0,255))
    #tree.save(imgdata, format="png")
    #Image.open(imgdata)
    #imgdata = base64.b64encode(imgdata.getvalue())
    return imgdata

# query = {'type': 'tree', 'gain': '5100 EURO', 'upper_label': '10000 EURO', 'bottom_label': '200 EURO', 'upper_proba': '0.80', 'bottom_proba': '0.20', 'assess_type': 'PE'}
# photo=draw(query['gain'], query['upper_label'], query['bottom_label'], query['upper_proba'], query['bottom_proba'], query['assess_type'])

# Image.open(photo)

# im=Image.open(photo)
# im.show()