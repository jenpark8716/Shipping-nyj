from flask import Flask,render_template,request, jsonify
from utils import DBUtils, get_page
import math

app = Flask(__name__)
db = DBUtils()


@app.route('/destinations', defaults={'page':1})
@app.route('/destinations/<page>', methods=['GET', 'POST'])
def destinations(page):
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
        # allsql = "SELECT count(*) FROM (SELECT dp.city AS DestinationPort, dp.country, string_agg(DISTINCT dpro.item, ', '), SUM(dpro.price * ft.order_quantity) FROM shipping ft LEFT JOIN port dp ON ft.to_port = dp.port_id LEFT JOIN product_ship dpro ON ft.product_id = dpro.product_id GROUP BY port_id ORDER BY port_id) as foo {}".format(filter_string) 
        sql = "SELECT * FROM (SELECT dp.country, dp.city AS city,  string_agg(DISTINCT dpro.item, ', '), SUM(dpro.price * ft.order_quantity) FROM shipping ft LEFT JOIN port dp ON ft.to_port = dp.port_id LEFT JOIN product_ship dpro ON ft.product_id = dpro.product_id GROUP BY port_id ORDER BY port_id) as foo {} ".format(filter_string)
    else:
        # allsql = "SELECT count(*) FROM (SELECT dp.city AS DestinationPort, dp.country, string_agg(DISTINCT dpro.item, ', '), SUM(dpro.price * ft.order_quantity) FROM shipping ft LEFT JOIN port dp ON ft.to_port = dp.port_id LEFT JOIN product_ship dpro ON ft.product_id = dpro.product_id GROUP BY port_id ORDER BY port_id) as foo "
        sql = "SELECT * FROM (SELECT dp.country, dp.city AS city,  string_agg(DISTINCT dpro.item, ', '), SUM(dpro.price * ft.order_quantity) FROM shipping ft LEFT JOIN port dp ON ft.to_port = dp.port_id LEFT JOIN product_ship dpro ON ft.product_id = dpro.product_id GROUP BY port_id ORDER BY port_id) as foo "

    #get city list
    city_sql = "select distinct(city) from port order by city"
    city_list = db.query(city_sql)
    print('city_list', city_list)

    #get country list
    country_sql = "select distinct(country) from port order by country"
    country_list = db.query(country_sql)
    print('city_list', country_list)

    results = db.query(sql)
    return render_template('destinations.html', results = results, city_list=city_list, country_list = country_list)

@app.route('/get_chart_data')
def get_chart_data():
    sql = "SELECT * FROM (SELECT dp.country, dp.city AS DestinationPort,  string_agg(DISTINCT dpro.item, ', '), SUM(dpro.price * ft.order_quantity) FROM shipping ft LEFT JOIN port dp ON ft.to_port = dp.port_id LEFT JOIN product_ship dpro ON ft.product_id = dpro.product_id GROUP BY port_id ORDER BY port_id) as foo "
    results = db.query(sql)
    x_cities = []
    y_products = []
    y_revenues = []

    for result in results:
        x_cities.append(result[1])
        y_products.append(len(result[2].split(",")))
        y_revenues.append(result[3])
    return jsonify({'x_cities': x_cities, 'y_products':y_products, 'y_revenues':y_revenues})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/shipinfo', defaults={'page':1})
@app.route('/shipinfo/<page>', methods=['GET'])
def shipinfo(page):
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
        sql = "select * from (SELECT ft.ship_id, string_agg(DISTINCT dp.region, ', ') as Regions_Travelled_to, string_agg(DISTINCT dd.month, ', ') AS Months_Travelled, SUM(dpro.price * ft.order_quantity) AS total_cost FROM shipping ft LEFT JOIN date AS dd ON ft.date = dd.date LEFT JOIN product_ship AS dpro ON ft.product_id = dpro.product_id LEFT JOIN port dp ON ft.to_port = dp.port_id GROUP BY ft.ship_id ORDER BY ft.ship_id) as f  {}".format(filter_string)
    else:
        
        sql = "SELECT ft.ship_id, string_agg(DISTINCT dp.region, ', ') as Regions_Travelled_to, string_agg(DISTINCT dd.month, ', ') AS Months_Travelled, SUM(dpro.price * ft.order_quantity) AS total_cost FROM shipping ft LEFT JOIN date AS dd ON ft.date = dd.date LEFT JOIN product_ship AS dpro ON ft.product_id = dpro.product_id LEFT JOIN port dp ON ft.to_port = dp.port_id GROUP BY ft.ship_id ORDER BY ft.ship_id;"

    #get city list
    ship_id_sql = "select distinct(ship_id) from shipment order by ship_id"
    ship_id_list = db.query(ship_id_sql)
    print('ship_id_list', ship_id_list)


    results = db.query(sql)
    return render_template('shipinfo.html', results = results, ship_id_list=ship_id_list)

@app.route('/', defaults={'page':1})
@app.route('/<page>', methods=['GET', 'POST'])
def home(page):
    datas={}
    perpage = 10
    page = int(page)
    startat = (page-1) * perpage
    show_shouye_status = 0
    if page > 1:
        show_shouye_status = 1

    args = request.args
    print('args', args)

    filter_string = ''

    filtered_args = [ (k, v) for k, v in args.items() if v !='' ]
    print('filtered_args', filtered_args)
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
    print('port_list', port_list)

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
    app.run(port=5000,debug=True)