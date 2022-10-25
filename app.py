from flask import Flask,render_template,request
from utils import DBUtils, get_page
import math

app = Flask(__name__)
db = DBUtils()


@app.route('/', defaults={'page':1})
@app.route('/<page>')
def home(page):
    datas={}
    perpage = 10
    page = int(page)
    startat = (page-1) * perpage
    show_shouye_status = 0
    if page > 1:
        show_shouye_status = 1

    args = request.args
    print(args)

    filter_string = ''

    filtered_args = [ (k, v) for k, v in args.items() if v !='' ]
    print(filtered_args)
    if filtered_args:
        # 如果只有一个搜索条件
        if len(filtered_args) == 1:
            filter_string = "WHERE {} = '{}'".format(filtered_args[0][0],filtered_args[0][1])
        # 如果有多个条件，则进行拼接
        else:
            temp_string = ["{} = '{}'".format(item[0], item[1]) for item in filtered_args]
            filter_string = 'WHERE ' + ' AND '.join(temp_string)

    if filter_string:
        allsql = "SELECT count(*) FROM shipping {}".format(filter_string) 
        sql = "SELECT * FROM shipping  {} LIMIT {} OFFSET {}".format(filter_string, perpage, startat)
    else:
        allsql = "SELECT count(*) FROM shipping "
        sql = "SELECT * FROM shipping  LIMIT {} OFFSET {}".format(perpage, startat)
    
    port_sql = "select distinct(port_id) from port order by port_id"
    port_list = db.query(port_sql)
    print(port_list)

    shippings = db.query(allsql)
    total_items = shippings[0][0]
    total_pages = int(math.ceil(total_items / perpage))
    print('total_items {} -  total_pages {} '.format(total_items,total_pages))
    dic = get_page(total_pages, page)
    datas = {
                'page': page,
                'total': total_pages,
                'perpage': perpage,
                'show_shouye_status': show_shouye_status,
                'dic_list': dic
                }
    results = db.query(sql)
    
    return render_template('home.html', results = results, datas = datas, port_list=port_list)


if __name__ == '__main__':
    app.run(port=5001,debug=True)