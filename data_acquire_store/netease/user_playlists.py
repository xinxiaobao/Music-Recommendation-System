import config
import json
import sys
from my_tools.database_tool import database_tool
from netease.first_param import first_param
from netease.request_data import request_data
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()


class user_playlists:


    def get_user_playlists(self, user_id=config.user_id, created_playlists_max=config.created_playlists_max,
                           collected_playlists_max=config.collected_playlists_max,
                           is_playlists_default=config.is_playlists_default,
                           is_playlists_created=config.is_playlists_created,
                           is_playlists_collected=config.is_playlists_collected):
   
        _first_param = first_param().get_first_param_user_playlists(user_id=user_id)
        try:
            content = request_data().get_request_data(_first_param[1], url=config.url_user_playlists)
            if content[0]:
                json_playlists_data = json.loads(content[1])["playlist"]
            else:
                return False, None
        except Exception as e:
            logger.error("get_user_playlists get failed",
                         "user_id:{},error_type:{},error:{}".format(user_id, type(e), e))
            return False, None
        playlist_count = 0
        created_playlists_count = 0
        collected_playlists_count = 0
        playlist_list = []
        user_playlists_list = []
        tag_list = []
        playlist_tag_list = []
        try:
            while playlist_count < len(json_playlists_data):
                if is_playlists_default:
                    parse = self.__parser(user_id=user_id, playlist_count=playlist_count, data=json_playlists_data,
                                          playlist_type=config.default_playlist)
                    playlist_list.append(parse["playlist_list"])
                    user_playlists_list.append(parse["user_playlist_list"])
                    if len(parse["tag_list"]) != 0:
                        tag_list.extend(parse["tag_list"])
                        playlist_tag_list.extend(parse["playlist_tag_list"])
                    playlist_count += 1
                    is_playlists_default = False
                    continue

                elif is_playlists_created:
                    if playlist_count == 0:
                        playlist_count += 1
                        continue
                    elif str(json_playlists_data[playlist_count]["creator"]['userId']) == str(user_id):
                        if created_playlists_count < created_playlists_max:
                            parse = self.__parser(user_id=user_id, playlist_count=playlist_count,
                                                  data=json_playlists_data,
                                                  playlist_type=config.created_playlist)
                            playlist_list.append(parse["playlist_list"])
                            user_playlists_list.append(parse["user_playlist_list"])
                            if len(parse["tag_list"]) != 0:
                                tag_list.extend(parse["tag_list"])
                                playlist_tag_list.extend(parse["playlist_tag_list"])
                            created_playlists_count += 1
                        playlist_count += 1
                    else:
                        is_playlists_created = False
                    continue

                elif is_playlists_collected:
                    if str(json_playlists_data[playlist_count]["creator"]['userId']) != str(user_id):
                        if collected_playlists_count < collected_playlists_max:
                            parse = self.__parser(user_id=user_id, playlist_count=playlist_count,
                                                  data=json_playlists_data,
                                                  playlist_type=config.collected_playlist)
                            playlist_list.append(parse["playlist_list"])
                            user_playlists_list.append(parse["user_playlist_list"])
                            if len(parse["tag_list"]) != 0:
                                tag_list.extend(parse["tag_list"])
                                playlist_tag_list.extend(parse["playlist_tag_list"])
                            collected_playlists_count += 1
                    playlist_count += 1
                    continue
                break
        except Exception as e:
            logger.error("get_user_playlists parse failed",
                         "user_id:{},created_playlists_count:{},collected_playlists_count:{},error_type:{},error:{}"
                         .format(user_id, created_playlists_count, collected_playlists_count, type(e), e))
            return False, None
        try:
            _database_tool = database_tool()
            _database_tool.insert_many_playlist(playlist_list)
            _database_tool.insert_many_tag(tag_list)
            _database_tool.commit()
            _database_tool.insert_many_user_playlist(user_playlists_list)
            _database_tool.insert_many_playlist_tag(playlist_tag_list)
            _database_tool.commit()
            _database_tool.close()
        except Exception as e:
            logger.error("get user_playlist save failed",
                         "user_id:{},created_playlists_count:{},collected_playlists_count:{},error_type:{},error:{}"
                         .format(user_id, created_playlists_count, collected_playlists_count, type(e), e))
            return False, None
        logger.info("get user_playlist success",
                    "user_id:{},created_playlists_count:{},collected_playlists_count:{}"
                    .format(user_id, created_playlists_count, collected_playlists_count))
        return True, playlist_list, user_playlists_list

    def __parser(self, user_id, playlist_count, data, playlist_type):
 
        tag_list = []
        playlist_tag_list = []
        for ptag in data[playlist_count]["tags"]:
            tag_list.append([ptag])
            playlist_tag_list.append([
                data[playlist_count]["id"],
                ptag
            ])
        return {
            "playlist_list": [
                data[playlist_count]["id"],
                data[playlist_count]["name"],
                data[playlist_count]["trackCount"],
                data[playlist_count]["playCount"],
                data[playlist_count]["updateTime"]
            ],
            "user_playlist_list": [
                user_id,
                data[playlist_count]["id"],
                playlist_type
            ],
            "tag_list": tag_list,
            "playlist_tag_list": playlist_tag_list
        }
