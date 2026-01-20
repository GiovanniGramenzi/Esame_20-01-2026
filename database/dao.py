from database.DB_connect import DBConnect
from model.artist import Artist
from model.connessione import Connessione

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_nodes(album_min,artist_dict):

        conn = DBConnect.get_connection()
        result =[]
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT artist_id
                FROM album
                GROUP BY artist_id
                HAVING COUNT(*)>=%s
                """
        cursor.execute(query,(album_min,))
        for row in cursor:
            artist=artist_dict[row['artist_id']]
            result.append(artist)

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def get_connessioni(album_min):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query="""select least(ga1.artist_id,ga2.artist_id)as a1_id,greatest(ga1.artist_id,ga2.artist_id) as a2_id,count(*) as generi
                 from (select a.artist_id,t.genre_id
                          from track t,album a
                          where a.id=t.album_id
                          group by  a.artist_id,t.genre_id
                          having count(a.id)>=%s)ga1,
                          (select a.artist_id,t.genre_id
                          from track t,album a
                          where a.id=t.album_id
                          group by  a.artist_id,t.genre_id
                          having count(a.id)>=%s)ga2
                 where ga1.genre_id=ga2.genre_id and ga1.artist_id<ga2.artist_id
                 group by a1_id,a2_id
                """
        cursor.execute(query,(album_min,album_min))
        for row in cursor:
            result.append(Connessione(row['a1_id'],row['a2_id'],row['generi']))
        cursor.close()
        conn.close()
        return result




