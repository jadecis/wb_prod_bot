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
            return cur.fetchone()
        
    def get_user_settings(self, user_id):
        self.connection.ping()
        with self.connection.cursor() as cur:
            cur.execute("""SELECT 
                            sales.name AS name_sale, setting_users.market, setting_users.catalog, remain.value AS remain, sales.xs, sales.ys, setting_users.page
                            FROM setting_users
                            LEFT JOIN sales ON setting_users.size_sale = sales.id
                            LEFT JOIN remain ON setting_users.remaining = remain.id
                            WHERE user_id=%s""", (user_id, ))
            return cur.fetchone()
        
        
    def get_gds(self, query, page):
        self.connection.ping()
        with self.connection.cursor() as cur:
            try:
                N=10
                offset= (page-1)*N
                cur.execute(f"{query}\nORDER BY prod_id LIMIT %s OFFSET %s",
                            (N, offset, ))
                return cur.fetchall()
            except: 
                return False
    
    def get_catalog_ids(self):
        self.connection.ping()
        with self.connection.cursor() as cur:
            cur.execute(f"SELECT wb_id FROM catalog")
            return cur.fetchall()
        
    def set_page(self, user_id):
        self.connection.ping()
        with self.connection.cursor() as cur:
            cur.execute(f"UPDATE setting_users SET page=1 WHERE user_id=%s", (user_id, ))
            
    def user_launch(self, user_id=None):
        self.connection.ping()
        with self.connection.cursor() as cur:
            if user_id:
                return cur.execute(f"UPDATE subscribers SET launch=1 WHERE user_id=%s", (user_id, ))
            cur.execute(f"UPDATE subscribers SET launch=0 WHERE id > 0")
            
