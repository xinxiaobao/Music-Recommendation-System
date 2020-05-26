import time
from concurrent.futures import ThreadPoolExecutor

import config
import json
from netease.first_param import first_param
from netease.request_data import request_data
from my_tools.database_tool import database_tool
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()


class user_ranklist_songs:
    """
    ranklist class

    """

    def get_user_ranklist_songs_thread(self, user_list: list, thread_count=10, thread_inteval_time=2,
                                       rank_max=config.rank_max):
        """
        threads to get ranklist
        """
        try:
            success_count = 0
            with ThreadPoolExecutor(thread_count) as executer:
                future_list = []
                for user_id in user_list:
                    future = executer.submit(self.get_user_ranklist_songs,
                                             user_id[0], config.rank_type_all, rank_max)
                    future_list.append(future)
                    time.sleep(thread_inteval_time)
                for future in future_list:
                    if future.result()[0]:
                        success_count += 1
            return True
        except Exception as e:
            logger.error("get_user_ranklist_songs_thread failed", "user_id_list_length:{},error_type:{},error:{}"
                         .format(len(user_list), type(e), e))
        return False

    def get_user_ranklist_songs(self, user_id=config.user_id, rank_type=config.rank_type, rank_max=config.rank_max):


        _first_param = first_param().get_first_param_ranklist(user_id=user_id, rank_type=rank_type)
        json_data = None
        try:
            content = request_data().get_request_data(first_param=_first_param[1], url=config.url_user_rank)
            if content[0]:
                if rank_type == config.rank_type_all:
                    json_data = json.loads(content[1])["allData"]
                elif rank_type == config.rank_type_week:
                    json_data = json.loads(content[1])["weekData"]
            else:
                return False, None
        except KeyError as e:
            logger.warning(
                "get_user_ranklist_songs get failed, Maybe the guy's ranklist is hidden,can you see it in the webpage ?",
                "user_id:{},rank_type:{},ranklist_url:https://music.163.com/#/user/songs/rank?id={} ,error_type:{},error:{}"
                    .format(user_id, rank_type, user_id, type(e), e))
            return False, None
        except Exception as e:
            logger.error("get_user_ranklist_songs get failed", "user_id:{},rank_type:{},error_type:{},error:{}"
                         .format(user_id, rank_type, type(e), e))
            return False, None
        ranklist_id = str(user_id) + "r" + str(rank_type)
        song_success_count = 0
        rank_list = []
        user_rank_list = []
        song_list = []
        artist_list = []
        artist_song_list = []
        song_rank_list = []
        user_song_list = []
        try:
            # ranklist_id rank_type rank_date
            rank_list.append([
                ranklist_id,
                rank_type,
                int(round(time.time() * 1000))
            ])
            # user_id ranklist_id
            user_rank_list.append([
                user_id,
                ranklist_id
            ])
            while song_success_count < rank_max and song_success_count < len(json_data):
                song_id = json_data[song_success_count]["song"]["id"]
                song_score = json_data[song_success_count]["score"]
                # print(json_data)
                # print('#############################')
                # print(json_data[song_success_count])
                # print('#############################')
                # print(song_score)

                # song_id song_name
                song_list.append([
                    song_id,
                    json_data[song_success_count]["song"]["name"]
                ])
                # song_id ranklist_id song_score
                song_rank_list.append([
                    song_id,
                    ranklist_id,
                    song_score
                ])
                # 多个歌手
                artist_count = 0
                for artist in json_data[song_success_count]["song"]["ar"]:
                    # artist_id artist_name
                    artist_list.append([
                        artist["id"],
                        artist["name"]
                    ])
                    # artist_id song_id sort
                    artist_song_list.append([
                        artist["id"],
                        song_id,
                        artist_count
                    ])
                    artist_count += 1
                # user_id song_id ranklist_all/week_score
                user_song_list.append([
                    user_id,
                    song_id,
                    song_score
                ])
                song_success_count += 1
        except Exception as e:
            logger.error("get_user_ranklist_songs parse failed",
                         "user_id:{},rank_type:{},error_type:{},song_success_count:{},error:{}".
                         format(user_id, rank_type, song_success_count, type(e), e))
            return False, None
        try:
            _database_tool = database_tool()
            _database_tool.insert_many_ranklist(rank_list)
            _database_tool.insert_many_song(song_list)
            _database_tool.insert_many_artist(artist_list)
            _database_tool.commit()
            _database_tool.insert_many_user_ranklist(user_rank_list)
            _database_tool.insert_many_song_ranklist(song_rank_list)
            _database_tool.insert_many_artist_song(artist_song_list)
            _database_tool.insert_many_user_song_column(
                column="rank_all_score" if rank_type == config.rank_type_all else "rank_week_score",
                data_list=user_song_list)
            _database_tool.commit()
            _database_tool.close()
        except Exception as e:
            logger.error("get_user_ranklist_songs save failed",
                         "user_id:{},rank_type:{},song_count_success,error_type:{},error:{}"
                         .format(user_id, rank_type, song_success_count, type(e), e))
            return False, None
        logger.info("get_user_ranklist_songs success",
                    "user_id:{},rank_type:{},song_success_count:{}".format(user_id, rank_type, song_success_count))
        return True, (rank_list, song_list, artist_list, user_rank_list, song_rank_list, artist_song_list)

