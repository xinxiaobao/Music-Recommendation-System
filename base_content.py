import pandas as pd
import numpy as np 


# extract song tags from user data
def tag_extrat(user, n):
    user_tag = {}
    for i, tag in user['tag_name'].items():
        if tag in user_tag:
            user_tag[tag] += int(user.loc[i]['tag_count'])
        elif tag != '\\N':
            user_tag[tag] = int(user.loc[i]['tag_count'])

    max_value = max(user_tag.values())
    tag_rank = sorted(user_tag.items(), key=lambda x:x[1], reverse=True)
    
    user_tag = {}
    for tag, num in tag_rank[:n]:
        user_tag[tag] = num/max_value
    return user_tag

# merge tags 
def tag_merge(tag1, tag2):
    for i in tag2:
        if i in tag1.keys():
            tag1[i] += tag2[i]
        else:
            tag1[i] = tag2[i]
    return tag1

# extract favorite  artists from user data
def artist_extrat(user, n):
    user_artist = {}
    for i, artist in user['artist'].items():
        if artist in user_artist:
            user_artist[artist] += 1
        elif artist != '\\N':
            user_artist[artist] = 1
   
    artist_rank = sorted(user_artist.items(), key=lambda x:x[1], reverse=True)
    user_artist = []
    for artist, num in artist_rank[:n]:
        user_artist.append(artist)
    return user_artist

# extract user features (favorite  artists & songs tags) from user data
def user_feature(user_favourites, user_histories):
    artists = artist_extrat(user_histories, 20)
    tag1 = tag_extrat(user_favourites, 5)
    tag2 = tag_extrat(user_histories, 5)
    tags = tag_merge(tag1, tag2)

    # print('----- user favorite tags ---------')
    # print(tags)
    # print('\n')
    # print('------ user favorite artists')
    # print(artists)

    return artists, tags


# content-based recommendation system
def rs_content(songs, artists, tags):
    rs_songs_1 = songs[songs['artist_name'].isin(artists)][['song_id', 'song_name', 'artist_name']]
    rs_songs_2 = rs_songs_1.drop_duplicates('song_id', keep ='first', inplace = False)
    rs_songs_2['rs_score'] = None   

    rs_songs_2 = rs_songs_2.iloc[:800, :]
    
    songs_1 = songs[songs['artist_name'].isin(artists)]
    songs_2 = songs_1[songs_1['tag_name'].isin(tags)]

    index = 0
    for song_id in rs_songs_2['song_id']:
        rs_score = 0
        for tag in tags.keys():
            rs_score += (songs_2[(songs_2['song_id'] == song_id) & (songs_2['tag_name'])]['tag_count'] * tags[tag])

        rs_songs_2.iloc[index, 3] = sum(rs_score)
        index += 1
    
    rs_songs_2.sort_values("rs_score",ascending = False , inplace=True)
    return np.array(rs_songs_2.iloc[:50, :3])

# content-based recommendation system for cold start
def rs_content_cold(songs, artists, n = 10):
    rs_songs_1 = songs[songs['artist_name'].isin(artists)][['song_id', 'song_name', 'artist_name']]
    rs_songs_2 = rs_songs_1.drop_duplicates('song_id', keep ='first', inplace = False)
    rs_songs = []
    for artist in artists:
        temp = rs_songs_2[rs_songs_2['artist_name'] == artist][:n]
        for re_song in np.array(temp):
            rs_songs.append(re_song)
    return rs_songs

