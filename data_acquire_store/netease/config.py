
import json
import os
import random
import sys
import logging

"""
config 

"""

# customized personal setting===============================================

# target user information
# user_id = "474252223"
# user_name = "IsolationTom"

user_id = "1493673206"
user_name = "felixlukk"

# db information ----------------------------

# db username
database_user_name = "root"

# pd
database_user_pwd = "87968069"

# port
database_port = 3306

# ip
database_host = "127.0.0.1"

# database name
database_name = "netease_music"

# coding
database_charset = "utf8mb4"

# ranklist ----------------------------
# ranklist type

# week
rank_type_week = 1
# all
rank_type_all = 0
# all+week
rank_type_week_all = -1

# default type
rank_type = 1

# max number
week_rank_max = 100

# max number
all_rank_max = 100

rank_max = all_rank_max

# song ------------------------------

# song source type
song_source_default = 0
song_source_rank = 1
song_source_playlist = 2

# default type
song_source_type = song_source_default

# playlist ------------------------------

# type
normal_playlist = 4
# favourite
default_playlist = 5
# created
created_playlist = 6
# collected
collected_playlist = 7

playlist_type = 4

# max number of song
playlist_songs_max = sys.maxsize

# favourite list --------------------

# whether to crawl it
is_playlists_default = True

# max song
default_songs_max = sys.maxsize

# created list -------------------------

# whether to crawl
is_playlists_created = True

# max song
created_playlists_max = sys.maxsize
created_songs_max = sys.maxsize

# collected list -------------------------

# whether to crawl it
is_playlists_collected = True

# max song
collected_playlists_max = 5

collected_songs_max = sys.maxsize


# score rate --------------------

# all time score
factor_rank_all_score = 4
# late week score
factor_rank_week_score = 2.5
# playlist pop
factor_playlist_like_pop = 2
# created pop
factor_playlist_create_pop = 1
# colloected pop
factor_playlist_collect_pop = 0.5

# basic reqeuest(please not touch it)=================================================

# basic header
base_url = "http://music.163.com/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
host = "music.163.com"
language = "zh-CN,zh;q=0.9,en;q=0.8"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

# normal header
user_headers = {
    "User-Agent": user_agent,
    "Host": host,
    "Accept": accept,
    "Referer": base_url,
    "Accept-Language": language
}

# eapi header
user_headers_eapi = {
    'os': 'osx',
    'appver': '2.5.3',
    'requestId': str(random.randint(10000000, 99999999)),
    'clientSign': '',
}

# eapi common params
eapi_params = {
    'verifyId': 1,
    'os': 'OSX',
    'header': json.dumps(user_headers_eapi, separators=(',', ':'))
}

# test id
# song_id = "656405"
song_id = "1297729"

# test playlistid
# playlist_id = "13928655"
playlist_id = "2628960735"


# logger
logger_name = "logger"
logger_file = "default"
project_root = os.path.dirname(__file__)
logger_path = project_root + "/logger.log"
logger_formatter = "%(asctime)s %(levelname)s %(message)s"
logger_console_level = logging.DEBUG
logger_file_level = logging.DEBUG

# AES ================================================================



# total
aes_total = True

# offset
aes_offset = 0

# limit
aes_limit = 1000


aes_ranklist_type = -1


# request params -------------------------------

aes_param_error = -1
aes_param_comment = 1
aes_param_ranklist = 2
aes_param_search = 3

aes_first_param_type = aes_param_error


api_weapi = 0
api_eapi = 1
api_type = api_weapi

second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

# eapikey
eapikey = "e82ckenh8dichen8"

# key
first_key = forth_param
second_key = 16 * 'F'

# offset
iv = "0102030405060708"

# encSecKey
encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"

# url ================================================================

# url
url_user_rank = "https://music.163.com/weapi/v1/play/record"

# 用户主页歌单url
url_user_playlists = "https://music.163.com/weapi/user/playlist"

# 歌单url
url_playlist = "https://music.163.com/weapi/v3/playlist/detail"



def get_playlist_url(playlist_id):
    """
    歌单url + 歌单id
    :param playlist_id: 歌单id
    :return: 歌单url
    """
    return "https://music.163.com/playlist?id={}".format(playlist_id)

