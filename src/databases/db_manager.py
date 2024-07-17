# db/db_manager.py
import pymysql
from settings import DB_CONFIG


class DBManager:
    def __init__(self):
        """
        데이터베이스를 연결합니다.

        :raise Exception: 연결을 여는 중에 오류가 발생할 경우 발생합니다.
        """

        self.connection = pymysql.connect(**DB_CONFIG)

    def execute_query(self, query: str, params: tuple = None):
        """
        전달받은 쿼리를 실행하고 결과를 반환합니다.

        :param str query: 실행할 SQL 쿼리입니다.
        :param tuple params: 쿼리에 사용할 파라미터입니다.
        :return list: 쿼리 결과를 반환합니다.
        :raise HTTPException: 요청 실행 중 오류가 발생할 경우 발생합니다.
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.fetchall()

    def insert_data(self, query: str, params: tuple):
        """
        전달받은 쿼리를 사용하여 데이터를 삽입합니다.

        :param str query: 실행할 SQL 쿼리입니다.
        :param tuple params: 쿼리에 사용할 파라미터입니다.
        :return int: 마지막으로 삽입된 행의 ID를 반환합니다.
        :raise HTTPException: 요청 실행 중 오류가 발생할 경우 발생합니다.
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid

    def update_data(self, query: str, params: tuple):
        """
        전달받은 쿼리를 사용하여 데이터를 업데이트합니다.

        :param str query: 실행할 SQL 쿼리입니다.
        :param tuple params: 쿼리에 사용할 파라미터입니다.
        :return int: 영향을 받은 행의 수를 반환합니다.
        :raise HTTPException: 요청 실행 중 오류가 발생할 경우 발생합니다.
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount

    def delete_data(self, query: str, params: tuple):
        """
        전달받은 쿼리를 사용하여 데이터를 삭제합니다.

        :param str query: 실행할 SQL 쿼리입니다.
        :param tuple params: 쿼리에 사용할 파라미터입니다.
        :return int: 영향을 받은 행의 수를 반환합니다.
        :raise HTTPException: 요청 실행 중 오류가 발생할 경우 발생합니다.
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount

    def close_connection(self):
        """
        데이터베이스 연결을 닫습니다.

        :raise Exception: 연결을 닫는 중에 오류가 발생할 경우 발생합니다.
        """

        self.connection.close()
