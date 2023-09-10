import nltk
import os

nltk.download('vader_lexicon')

directory = "output"
parent_dir = os. getcwd()
path = os.path.join(parent_dir, directory)
os.mkdir(path)
print("Directory '% s' created" % directory)

directory2 = "input"
parent_dir = os. getcwd()
path = os.path.join(parent_dir, directory2)
os.mkdir(path)
print("Directory '% s' created" % directory)

print("Setup complete, Add .txt file to input directory")