import tweepy
import time
# NOTE: I put my keys in the keys.py to separate them
# from this main file.
# Please refer to keys_format.py to see the format.
from keys import *
import requests as req
# NOTE: flush=True is just for running this script
# with PythonAnywhere's always-on task.
# More info: https://help.pythonanywhere.com/pages/AlwaysOnTasks/
print('this is my twitter bot', flush=True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    def download_image(url):
        filename='mytweetimage.jpg'
        image_url = url
        image_response = req.get(image_url,stream = True)
        if image_response.status_code == 200:
            with open(filename, 'wb') as image_file:
                for chunk in image_response:
                    image_file.write(chunk)
        return filename
    since_id = last_seen_id
    mentions = api.mentions_timeline(since_id, tweet_mode='extended')
    #print(mentions)
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#tkbotwhatamifeeling' in mention.full_text.lower():
            print('found #tkbotwhatamifeeling', flush=True)
            print('responding back...', flush=True)
            dedicated_msg = ''
            x = mention.entities['media'][0]['media_url']
            print(x)
            fn = download_image(x)
            photo = open(fn, 'rb')
            msg = '@' + mention.user.screen_name + dedicated_msg
            filename = 'mytweetimage.jpg'
            #api.update_status('@' + mention.user.screen_name +
                  #dedicated_msg , mention.id)
            #api.update_with_media('mytweetimage.jpg', status=dedicated_msg)
            #api.update_with_media(data, status=msg)
    #plan --> send message --> read image, --> reply with image
            exp = process_img()
            dedicated_msg = 'You are feeling '+exp
            msg = '@' + mention.user.screen_name + dedicated_msg
            media_ids =[]
            response = api.media_upload(filename)
            media_ids.append(response.media_id)
            api.update_status(status  = msg, media_ids=media_ids )

import numpy as np
import tensorflow as tf
objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
y_pos = np.arange(len(objects))
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
def emotion_analysis(emotions):
    objects = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    y_pos = np.arange(len(objects))

def process_img():
    model_path = './model_filter_final.h5'
    model =  tf.keras.models.load_model(model_path)
    img = image.load_img('mytweetimage.jpg', grayscale=True, target_size=(48, 48))
    show_img=image.load_img('mytweetimage.jpg', grayscale=False,target_size=(200, 200))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis = 0)

    x /= 255
    custom = model.predict(x)
    #print(custom[0])
    emotion_analysis(custom[0])

    x = np.array(x, 'float32')
    x = x.reshape([48, 48]);
    m=0.000000000000000000001
    a=custom[0]
    for i in range(0,len(a)):
        if a[i]>m:
            m=a[i]
            ind=i
    print('Expression Prediction:',objects[ind])
    result = objects[ind]
    return result

while True:
    reply_to_tweets()
    time.sleep(15)