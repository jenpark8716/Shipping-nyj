import os
import psycopg2

def get_page(total, p):
	show_page = 6      		   # 显示的页码数
	pageoffset = 3             # 偏移量
	start = 1                  #分页条开始
	end = total                #分页条结束

	if total > show_page:
		if p > pageoffset:
			start = p - pageoffset
			if total > p + pageoffset:
				end = p + pageoffset
			else:
				end = total
		else:
			start = 1
			if total > show_page:
				end = show_page
			else:
				end = total
		if p + pageoffset > total:
			start = start - (p + pageoffset - end)
	print('total - page - showpage - start - end: {} - {} - {} - {} - {}'.format(total,p, show_page,start,end))
	dic = range(start, end + 1)
	return dic


class DBUtils:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5432
        self.user = 'jen'
        self.pwd = '1513'
        self.db = 'Shipping'
        self.db_url = "postgresql://jen:1513@localhost:5432/Shipping"
    def get_con(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Error! :{}".format(e))
        return self.conn, self.cur

    def close_db(self, conn, cur):
        try:
            cur.close()
            conn.close()
        except Exception as e:
            print("Error! :{}".format(e))

    def query(self, sql, *args):
        conn, cursor = self.get_con()
        print(sql)
        cursor.execute(sql, *args)
        res = cursor.fetchall()
        self.close_db(conn, cursor)
        return res

