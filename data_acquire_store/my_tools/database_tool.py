from DBUtils.PooledDB import PooledDB
import pymysql
import config
from my_tools.logger_tool import loggler_tool
import sys
import time
import warnings

logger = loggler_tool()

# db config
database_host = config.database_host
database_port = config.database_port
database_user_name = config.database_user_name
database_user_pwd = config.database_user_pwd
database_name = config.database_name
database_charset = config.database_charset

# PooledDB
database_pool = PooledDB(
    # db modile
    creator=pymysql,
    # max number of connection
    maxconnections=10,
    # initial
    mincached=5,
    # initial number
    maxcached=0,
    # max number
    maxshared=10,
    # whether block 
    blocking=True,
    maxusage=None,
    # session list["set datestyle to ...", "set time zone ..."]
    setsession=[],
    # ping MySQL server
    # 如：0 = None = never, 1 = default = whenever it is requested,
    # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    ping=0,
    host=database_host,
    port=database_port,
    user=database_user_name,
    password=database_user_pwd,
    database=database_name,
    charset=database_charset
)


class database_tool:
    """
    connection db pool

    """

    def __init__(self):
        """
        initial

        """
        self.database_pool = database_pool
        self.connection = None
        self.__connect()

    def __connect(self):
        """
        connect

        """
        try:
            self.connection = database_pool.connection()
        except Exception as e:
            logger.error("database connect failed", "error_type:{},error:{}".format(type(e), e))

    def execute(self, sql, data_list=None, execute_type=2, return_type=0):
        """
        execute
        tyoe       execute_type        return_type
        insert single line        1                     0
        insert multip line        2                     0
        select single line        1                     1
        select multip line        1                     2
        update single line        1                     0

        :param sql: sql
        :param data_list: list (only for execute_type)
        :param execute_type:  1 single 2 mutiple(default)
        :param return_type: return 0 default 1 single 2 multiple
        :return: 执行状态
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                if self.connection is None:
                    self.__connect()
                cursor = self.connection.cursor()
                # execute sql
                if execute_type == 1:
                    result = cursor.execute(sql)
                elif execute_type == 2:
                    # only for insert
                    result = cursor.executemany(sql, data_list)
                # return
                if return_type == 1:
                    result = cursor.fetchone()
                elif return_type == 2:
                    result = cursor.fetchall()
                # logger.info("database execute success", "sql_count:{},sql:{}".format(len(data_list), sql))
                return True, result
            except pymysql.err.IntegrityError as e:
                # if duplicate key
                if e.args[0] == 1062:
                    logger.debug("database execute duplicate",
                                 "sql:{},error_type:{},error:{}".format(sql, type(e), e))
                # check constraint
                elif e.args[0] == 1452:
                    logger.warning("database execute need foreign key",
                                   "sql:{},error_type:{},error:{}".format(sql, type(e), e))
                else:
                    logger.error("database execute failed",
                                 "sql:{},error_type:{},error:{}".format(sql, type(e), e))
            except Exception as e:
                logger.error("database execute failed",
                             "sql:{},error_type:{},error:{}".format(sql, type(e), e))
        return False, None

    def commit(self):
        try:
            self.connection.commit()
            return True
        except Exception as e:
            logger.error("database commit failed", "error_type:{},error:{}".format(type(e), e))
            return False

    def close(self):
        try:
            self.connection.close()
            return True
        except Exception as e:
            logger.error("database conn close failed", "error_type:{},error:{}".format(type(e), e))
            return False

    # sql table actions -----------------

    def insert_many_user(self, data_list):
        self.execute(
            "insert into user(user_id,user_name) values(%s,%s) on duplicate key update user_id = user_id,user_name=user_name",
            data_list
        )

    def insert_many_ranklist(self, data_list):
        self.execute(
            "insert into ranklist(ranklist_id, ranklist_type,ranklist_date) values (%s,%s,%s) on duplicate key update ranklist_id = ranklist_id",
            data_list
        )

    def insert_many_song(self, data_list):
        self.execute(
            "insert into song(song_id,song_name) values (%s,%s) on duplicate key update song_id = song_id,song_name=song_name",
            data_list
        )

    def insert_many_tag(self, data_list):
        self.execute(
            "insert into tag(tag_name) values (%s) on duplicate key update tag_name=tag_name",
            data_list
        )

    def insert_many_playlist_tag(self, data_list):
        self.execute(
            "insert into playlist_tag(playlist_id,tag_name) values (%s,%s) on duplicate key update playlist_id=playlist_id",
            data_list
        )

    def insert_many_user_ranklist(self, data_list):
        self.execute(
            "insert into user_ranklist(user_id,ranklist_id) values (%s,%s) on duplicate key update user_id = user_id",
            data_list
        )

    def insert_many_song_ranklist(self, data_list):
        self.execute(
            "insert into song_ranklist(song_id,ranklist_id,song_score) values (%s,%s,%s) on duplicate key update song_id = song_id",
            data_list
        )

    def insert_many_playlist(self, data_list):
        self.execute(
            "insert into playlist(playlist_id,playlist_name,playlist_songs_total,playlist_play_count,playlist_update_date) values (%s,%s,%s,%s,%s)  on duplicate key update playlist_id = playlist_id",
            data_list
        )

    def insert_many_user_playlist(self, data_list):
        self.execute(
            "insert into user_playlist(user_id,playlist_id,playlist_type) values (%s,%s,%s) on duplicate key update user_id = user_id",
            data_list
        )

    def insert_many_song_playlist(self, data_list):
        self.execute(
            "insert into song_playlist(song_id,playlist_id,song_pop,playlist_type) values (%s,%s,%s,%s) on duplicate key update song_id = song_id",
            data_list
        )

    def insert_many_comment(self, data_list):
        self.execute(
            "insert into comment(comment_id, comment_type, comment_date, comment_content,comment_like_count) values (%s,%s,%s,%s,%s) on duplicate key update comment_id = comment_id",
            data_list
        )

    def insert_many_song_comment(self, data_list):
        self.execute(
            "insert into song_comment(song_id,comment_id) values (%s,%s) on duplicate key update song_id = song_id",
            data_list
        )

    def insert_many_user_comment(self, data_list):
        self.execute(
            "insert into user_comment(user_id,comment_id) values (%s,%s) on duplicate key update user_id = user_id",
            data_list
        )

    def insert_many_artist(self, data_list):
        self.execute(
            "insert into artist(artist_id,artist_name) values (%s,%s) on duplicate key update artist_id = artist_id",
            data_list
        )

    def insert_many_artist_song(self, data_list):
        self.execute(
            "insert into artist_song(artist_id,song_id,sort) values (%s,%s,%s) on duplicate key update artist_id = artist_id",
            data_list
        )

    def insert_many_song_tag(self, data_list):
        self.execute(
            "insert into song_tag(song_id,tag_name) values (%s,%s) on duplicate key update tag_count=tag_count+1",
            data_list
        )

    def insert_many_user_song_column(self, column, data_list):
        """
        insert into song to update score

        """
        for data in data_list:
            self.execute(
                "insert into user_song(user_id,song_id,{0}) values ({1},{2},{3}) on duplicate key update {0}={3}; "
                    .format(column, data[0], data[1], data[2]),
                execute_type=1, return_type=0
            )
            # self.execute(
            #     "update user_song "
            #     "set score =cast(rank_all_score*{0}+rank_week_score*{1}+playlist_like_pop*{2}+playlist_create_pop*{3}+playlist_collect_pop*{4} as signed) "
            #     "where user_id={5} and song_id={6};"
            #         .format(config.factor_rank_all_score,
            #                 config.factor_rank_week_score,
            #                 config.factor_playlist_like_pop,
            #                 config.factor_playlist_create_pop,
            #                 config.factor_playlist_collect_pop,
            #                 data[0], data[1]),
            #     execute_type=1, return_type=0
            # )

    #  ----------------------

    def update_song_hot_comment_count(self, song_id, song_hot_comment_count=0):
        self.execute(
            "update song set song_hot_comment_count={} where song_id={}"
                .format(song_hot_comment_count, song_id), execute_type=1
        )

    def update_song_default_comment_count(self, song_id, song_default_comment_count=0):
        self.execute(
            "update song set song_default_comment_count={} where song_id={}"
                .format(song_default_comment_count, song_id), execute_type=1
        )

    # select ---------------

    def select_list_limit(self, table, start=0, count=sys.maxsize):
        """
        :param start: offset
        :param count: limit
        :return:
        """
        return self.execute(
            sql="select * from {} limit {} offset {}"
                .format(table, count, start),
            execute_type=1, return_type=2
        )

    def select_list_by_column(self, table, column, value, is_value_str=False, start=0, count=sys.maxsize):
        """

        :param start: offset
        :param count: limit
        :param is_value_str
        :return:
        """
        return self.execute(
            sql="select * from {} where {}='{}' limit {} offset {}"
                .format(table, column, value, count,
                        start) if is_value_str else "select * from {} where {}='{}' limit {} offset {}"
                .format(table, column, value, count, start),
            execute_type=1, return_type=2
        )

    def select_by_column(self, table, column, value, is_value_str=False):
        """
        select one result, one condition
        """
        return self.execute(
            sql="select * from {} where {}='{}'"
                .format(table, column, value) if is_value_str else "select * from {} where {}={}"
                .format(table, column, value),
            execute_type=1, return_type=1
        )

    def select_user_list(self, table, is_value_str=False, start=0, count=sys.maxsize):
         """

        """
         return self.execute(
            sql="select user_id from {} limit {} offset {}"
                .format(table, count,
                        start) if is_value_str else "select user_id  from {} limit {} offset {}"
                .format(table, count, start),
            execute_type=1, return_type=2
        )
        # return self.execute(
        #     sql="select user_id from {} where {}='{}' limit {} offset {}"
        #         .format(table, column, value, count,
        #                 start) if is_value_str else "select * from {} where {}='{}' limit {} offset {}"
        #         .format(table, column, value, count, start),
        #     execute_type=1, return_type=2
        # )
        

def test(pool, data_list):
    pool.insert_many_song(data_list)
