import json

import config


class first_param:
    """
    decrypt first params

    """


    def get_first_param_ranklist(self, user_id=config.user_id, rank_type=config.rank_type):

        return True, """{{uid:"{}",type:"{}"}}""".format(user_id, rank_type)

    def get_first_param_user_playlists(self, user_id=config.user_id, limit=config.aes_limit, offset=config.aes_offset):

        return True, """{{uid:"{}",limit:"{}",offset:"{}"}}""".format(user_id, limit, offset)

    def get_first_param_playlist(self, playlist_id=config.playlist_id, n=100000, s=0):

        return True, """{{id:"{}",n:"{}",s:"{}"}}""".format(playlist_id, n, s)

