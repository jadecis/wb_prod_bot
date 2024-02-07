import pymysql

class Database():
    def __init__(self, host, port, password, name, user):
        self.connection= pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=name,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.connection.autocommit(True)
        
        
    def check_subscribe(self, user_id):
        self.connection.ping()
        with self.connection.cursor() as cur:
            cur.execute("SELECT * FROM subscribers WHERE user_id=%s", (user_id, ))
            return bool(len(cur.fetchone()))
        
    def get_user_settings(self, user_id):
        self.connection.ping()
        with self.connection.cursor() as cur:
            cur.execute("""SELECT 
                            sales.value AS sale, setting_users.market, setting_users.catalog, remain.value AS remain
                            FROM setting_users
                            LEFT JOIN sales ON setting_users.size_sale = sales.id
                            LEFT JOIN remain ON setting_users.remaining = remain.id
                            WHERE user_id=%s""", (user_id, ))
            return cur.fetchone()
        
    def get_gds(self, size_sale, catalog, remaining):
        self.connection.ping()
        with self.connection.cursor() as cur:
            cur.execute(f"""SELECT prod_id, name, cur_price, sale, value FROM gds
                        WHERE cat_id in %s and
                        sale {size_sale} and sale > 0 and
                        value >= %s LIMIT 100
                        """, (catalog, remaining, ))
            
        return cur.fetchall()
    
    def get_catalog_ids(self):
        self.connection.ping()
        with self.connection.cursor() as cur:
            cur.execute(f"SELECT wb_id FROM catalog")
            return cur.fetchall()