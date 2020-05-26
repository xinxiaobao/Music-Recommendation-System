import time
from concurrent.futures import ThreadPoolExecutor

import config
import sys
from my_tools.database_tool import database_tool
from netease.user_ranklist_songs import user_ranklist_songs
from netease.playlist_songs import playlist_songs
# from netease.song_comments import song_comments
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()


class user_data:
    """
    user threads

    hot playlist->hot song->hot comment ->user
    1. user->user ranklist-> song,artist
    2. user->playlist -> song,artist

    """

    def get_playlist_songs(self, playlist_id):

        _database_tool = database_tool()
        _database_tool.insert_many_playlist([[playlist_id, '', 0, 0, '']])
        _database_tool.commit()
        _database_tool.close()
        playlist_songs().get_playlist_songs_by_playlist_id(playlist_id=playlist_id,
                                                           playlist_type=config.normal_playlist,
                                                           playlist_songs_max=sys.maxsize)

    def get_song_comments(self, song_start, song_count):

        song_list = database_tool().select_list_limit(table="song", start=song_start, count=song_count)
        if song_list[0]:
            for song in song_list[1]:
                song_comments().get_song_comments_hot(song_id=song[0], song_comments_hot_max=1000, thread_count=10,
                                                      thread_inteval_time=2)

    def get_user_songs(self, user_start, user_count, thread_count=20, thread_inteval_time=5):

        user_list = database_tool().select_list_limit(table="user", start=user_start, count=user_count)[1]
        try:
            success_count = 0
            _user_ranklist_songs = user_ranklist_songs()
            _playlist_songs = playlist_songs()
            with ThreadPoolExecutor(thread_count) as executer:
                future_list = []
                for user in user_list:
                    future_rank_all = executer.submit(_user_ranklist_songs.get_user_ranklist_songs,
                                                      user[0], config.rank_type_all, config.all_rank_max)
                    future_rank_week = executer.submit(_user_ranklist_songs.get_user_ranklist_songs,
                                                       user[0], config.rank_type_week, config.week_rank_max)
                    future_playlist = executer.submit(_playlist_songs.get_playlist_songs_by_user_id, user[0])
                    future_list.append(future_rank_all)
                    future_list.append(future_rank_week)
                    future_list.append(future_playlist)
                    time.sleep(thread_inteval_time)
                for future in future_list:
                    if future.result()[0]:
                        success_count += 1
            return True
        except Exception as e:
            logger.error("get_user_songs failed", "error_type:{},error:{}"
                         .format(type(e), e))

    def get_user_target(self, user, thread_count=20, thread_inteval_time=5):

        try:
            success_count = 0
            _user_ranklist_songs = user_ranklist_songs()
            _playlist_songs = playlist_songs()
            with ThreadPoolExecutor(thread_count) as executer:
                future_list = []

                if user:
                    future_rank_all = executer.submit(_user_ranklist_songs.get_user_ranklist_songs,
                                                      user, config.rank_type_all, config.all_rank_max)
                    future_rank_week = executer.submit(_user_ranklist_songs.get_user_ranklist_songs,
                                                       user, config.rank_type_week, config.week_rank_max)
                    future_playlist = executer.submit(_playlist_songs.get_playlist_songs_by_user_id, user)
                    future_list.append(future_rank_all)
                    future_list.append(future_rank_week)
                    future_list.append(future_playlist)
                    time.sleep(thread_inteval_time)
                for future in future_list:
                    if future.result()[0]:
                        success_count += 1
            return True
        except Exception as e:
            logger.error("get_user_songs failed", "error_type:{},error:{}"
                         .format(type(e), e))


