# from cf import *
from collaborative_filtering import *
from base_content import *

import random
import pandas as pd

from data_acquire_store.recommender.sql2df import *
from data_acquire_store.netease.user_data import *
import random

# user_id input()
# user_id = int(input('please enter your user id:'))
# user_id = 254430201 
user_id = 326122206

# flag = True
flag = False

if flag: # for cold start
    artists = ['李荣浩', '周杰伦', '五月天', '周华健', '林忆莲']
    songs = pd.read_csv('song_detail.csv')

    rs_songs_cold = rs_content_cold(songs, artists, n = 5)
    output = random.sample(list(rs_songs_cold), 10)
    print(output)

else:
    music_records_list = music_records_list()
    if str(user_id) in music_records_list:
        user_favourite_list=code_favourite_list(user_id)
        user_ranklist = code_ranklist(user_id)
        user_music_record=code_music_records(user_id)

    else:
        u = user_data()
        u.get_user_target(user_id)

        user_favourite_list=code_favourite_list(user_id)
        user_ranklist = code_ranklist(user_id)
        user_music_record=code_music_records(user_id)

    # Collaborative filtering system - pc
    rs_songs_cf = recommend('music_record.csv', user_id, dataframe = user_music_record)


    # content recomment system - xb
    songs = pd.read_csv('song_detail.csv')
    artists, tags = user_feature(user_favourite_list, user_ranklist)
    rs_songs_cont = rs_content(songs, artists, tags)

    output_songs = []
    if len(rs_songs_cf) > 5:
        output_songs.extend(random.sample(list(rs_songs_cf), 5))
        output_songs.extend(random.sample(list(rs_songs_cont), 5))
    else:
        output_songs.extend(list(rs_songs_cf))
        output_songs.extend(random.sample(list(rs_songs_cont), 10 -len(rs_songs_cf)))

    print(output_songs) 

