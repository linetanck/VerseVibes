import nltk
import random
from nltk.sentiment import SentimentIntensityAnalyzer
import uuid
from PIL import Image, ImageDraw, ImageFilter

def input():
    input_list = []
    text = open('input/example_all_too_well.txt', 'r', encoding='utf8') # Change filename here
    for line in text:
        line = line.strip() # Removes the /n at each linebreak
        input_list.append(str(line))
    return input_list

def sentiment(input_list):
    sia = SentimentIntensityAnalyzer() # Load/ instantiate sentiment analyzer
    line_index=0
    sentiment_values = {}
    for i in input_list:
        line_index += 1
        list_line_values = []
        temp_dict = sia.polarity_scores(i)
        list_line_values.append(temp_dict['neg']) # Exracting only the numerical values from the sentiment analysis
        list_line_values.append(temp_dict['neu'])
        list_line_values.append(temp_dict['pos'])
        list_line_values.append(temp_dict['compound'])
        sentiment_values[line_index]=list_line_values
    return sentiment_values

def bg_color(sentiment_values): # Determining the background colour values
    average_list=[]
    def average(list):
        return sum(list) / len(list)

    for i in sentiment_values.values():
        average_list.append(i[3])

    if average(average_list) >= 0.05: # Positive sentiment according to VADER documentation
        bg_col1 = int(255 * average(average_list)) # R value
        bg_col2 = random.randint(0, 60)  # G value
        bg_col3 = random.randint(0, 60)  # B value
    if average(average_list) > -0.05 and average(average_list) < 0.05: # Neutral sentiment according to VADER documentation
        bg_col1 = random.randint(0, 60)
        bg_col2 = int(255 * abs(average(average_list)))
        bg_col3 = random.randint(0, 60)
    if average(average_list) <= -0.05: # Negative sentiment according to VADER documentation
        bg_col1 = random.randint(0, 60)
        bg_col2 = random.randint(0, 60)
        bg_col3 = int(255 * abs(average(average_list)))
    return bg_col1, bg_col2, bg_col3

def generate(bg_col1, bg_col2, bg_col3): # Generating the artwork
    run_id = uuid.uuid1()
    print(f'Find your art with Processing ID: {run_id}')

    image = Image.new('RGB', (3500, 2500), (bg_col1,bg_col2,bg_col3))
    width, height = image.size

    number_of_dots = len(sentiment_values)

    draw_image = ImageDraw.Draw(image)

    for j in sentiment_values.values():
        if j[0] == 1.0:
            col1 = 255
            col2 = 0
            col3 = 0
        elif j[2] == 1.0:
            col1 = 0
            col2 = 255
            col3 = 0
        else:
            if j[3] >= 0.05:
                col1 = int(255 * j[3])
                col2 = random.randint(0, 60)
                col3 = random.randint(0, 60)
            if j[3] > -0.05 and j[3] < 0.05:
                col1 = random.randint(0, 60)
                col2 = int(255 * abs(j[3]))
                col3 = random.randint(0, 60)
            if j[3] <= -0.05:
                col1 = random.randint(0, 60)
                col2 = random.randint(0, 60)
                col3 = int(255 * abs(j[3]))
        for k in range(number_of_dots):
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
sentiment_values = sentiment(input)
bg_col1, bg_col2, bg_col3 = bg_color(sentiment_values)
generate(bg_col1, bg_col2, bg_col3)