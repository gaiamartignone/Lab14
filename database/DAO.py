from database.DB_connect import DBConnect
from model.Ordini import Ordini


class DAO:

    @staticmethod
    def getStores():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT store_id
                        FROM  stores
                        """

        cursor.execute(query,)

        for row in cursor:
            result.append(row['store_id'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(c):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * 
                    FROM  orders
                    where store_id=%s"""

        cursor.execute(query, (c,))

        for row in cursor:
            result.append(Ordini(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(store, day):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select o1.order_id as ord1, o2.order_id as ord2, t1.numitems1+t2.numitems2 as sum
                from orders o1, orders o2,
                (select it1.order_id as oi1, count(*) as numitems1
                from order_items it1 
                group by it1.order_id) t1,
                (select it2.order_id as oi2, count(*) as numitems2
                from order_items it2
                group by it2.order_id) t2
                where o1.store_id = o2.store_id
                and o1.store_id = %s
                and t1.oi1=o1.order_id
                and t2.oi2=o2.order_id
                and DATEDIFF(o1.order_date,o2.order_date)< %s
                and DATEDIFF(o1.order_date,o2.order_date) >0"""

        cursor.execute(query, (store, day,))

        for row in cursor:
            result.append((row['ord1'], row['ord2'],row['sum']))

        cursor.close()
        conn.close()
        return result