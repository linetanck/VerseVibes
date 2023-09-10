import nltk
import random
from nltk.sentiment import SentimentIntensityAnalyzer
import uuid
from PIL import Image, ImageDraw, ImageFilter

def input():
    input_list = []
    text = open('input/sonnet_list.txt', 'r') # change filename here
    for line in text:
        line = line.strip() # removes the /n at each linebreak
        input_list.append(str(line))
    return input_list

def sentiment(input_list):
    sia = SentimentIntensityAnalyzer() # load/ instantiate sentiment analyzer
    num=0
    dict_values = {}
    for i in input_list:
        num += 1
        list_line_values = []
        temp_dict = sia.polarity_scores(i)
        # exracting only the numerical values from the sentiment analysis
        list_line_values.append(temp_dict['neg'])
        list_line_values.append(temp_dict['neu'])
        list_line_values.append(temp_dict['pos'])
        list_line_values.append(temp_dict['compound'])
        dict_values[num]=list_line_values
    return dict_values

def bg_color(dict_values):
    average_list=[]
    def average(list):
        return sum(list) / len(list)

    for k in dict_values.values():
        average_list.append(k[3])

    if average(average_list) >= 0.05: # positive sentiment according to VADER documentation
        bg_col1 = int(255 * average(average_list)) # R value
        bg_col2 = random.randint(0, 60)  # G value
        bg_col3 = random.randint(0, 60)  # B value
    if average(average_list) > -0.05 and average(average_list) < 0.05: # neutral sentiment
        bg_col1 = random.randint(0, 60)
        bg_col2 = int(255 * abs(average(average_list)))
        bg_col3 = random.randint(0, 60)
    if average(average_list) <= -0.05: # negative sentiment
        bg_col1 = random.randint(0, 60)
        bg_col2 = random.randint(0, 60)
        bg_col3 = int(255 * abs(average(average_list)))
    return bg_col1, bg_col2, bg_col3

def generate(bg_col1, bg_col2, bg_col3):
    run_id = uuid.uuid1()
    print(f'Processing with ID: {run_id}')

    image = Image.new('RGB', (3500, 2500), (bg_col1,bg_col2,bg_col3))
    width, height = image.size

    number_of_dots = len(dict_values)

    draw_image = ImageDraw.Draw(image)

    for j in dict_values.values():
        if j[0] == 1.0:
            col1 = 255
            col2 = 0
            col3 = 0
        elif j[2] == 1.0:
            col1 = 0
            col2 = 255
            col3 = 0
        else:
            if j[3] >= 0.05: # positive sentiment
                col1 = int(255 * j[3])
                col2 = random.randint(0, 60)
                col3 = random.randint(0, 60)
            if j[3] > -0.05 and j[3] < 0.05: # neutral sentiment
                col1 = random.randint(0, 60)
                col2 = int(255 * abs(j[3]))
                col3 = random.randint(0, 60)
            if j[3] <= -0.05: # negative sentiment
                col1 = random.randint(0, 60)
                col2 = random.randint(0, 60)
                col3 = int(255 * abs(j[3]))
        for i in range(number_of_dots):
            boundingbox_width = random.randint(700, 8000)
            boundingbox_height = random.randint(700, 8000)
            position_x = random.randint(0, width)
            position_y = random.randint(0, height)
            dot_shape = [
                (position_x, position_y),
                (position_x + boundingbox_width, position_y + boundingbox_height)]
        draw_image.ellipse(dot_shape, fill=(col1, col2, col3))
    image = image.filter(ImageFilter.GaussianBlur(radius=200))
    image.show()
    image.save(f'./output/{run_id}.png')

input = input()
dict_values = sentiment(input)
bg_col1, bg_col2, bg_col3 = bg_color(dict_values)
generate(bg_col1, bg_col2, bg_col3)