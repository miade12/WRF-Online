# importing Flask and other modules

from flask import Flask, request, render_template
import os

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def wps():
    if request.method == "POST":
        sd = request.form.get("start_date")
        ed = request.form.get("end_date")
        isec = request.form.get("interval_seconds")
        go_file = "mkdir /home/miade/Desktop/test/{}".format(sd)

        file = open('/home/miade/PycharmProjects/WRF-Online/wrf_statics/test_namelist_wps.py', "w")
        print("start_date = '{}' ".format(sd), file=file)
        print("end_date = '{}' ".format(ed), file=file)
        print("interval_seconds = '{}' ".format(isec), file=file)

        os.system("mkdir /home/miade/Desktop/test/DATA")

    return render_template('index.html')


@app.route('/wps', methods=["GET", "POST"])
def wrf():
    if request.method == "POST":

        os.system("mkdir /home/miade/Desktop/test/DATA")

    return render_template('wps.html')


@app.route('/wrf', methods=["GET", "POST"])
def wrf2():
    if request.method == "POST":
        os.system("mkdir /home/miade/Desktop/test/DATA")
    return render_template('wrf.html')


"""


@app.route('/wps', methods=["GET", "POST"])
def wrf():
    if request.method == "POST":

        os.system("mkdir /home/miade/Desktop/test/DATA")

    return render_template('wrf.html')


@app.route('/wps/wrf', methods=["GET", "POST"])
def wrf():
    if request.method == "POST":
        os.system("mkdir /home/miade/Desktop/test/DATA")
    return render_template('wrf.html')
    
    
 get_data = "cd /home/miade/Desktop/test/DATA && wget " \
                   "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.{}/00/atmos/gfs.t00z.atmf007.nc".format(sd)
                   os.system(get_data)
                   
                   yukarıdaki satırları html sayfaları tamamlandıktan sonra ekle.!
    
       
fin = open('/home/miade/PycharmProjects/WRF-Online/wrf_statics/test_namelist_wps.py', 'wt')
        
        for line in fin:
            fin.write(line.replace('{}', sd))

fo.print('start_date = '{}' /n2 end_date = {}').format(sd,ed)
isec = request.form.get("interval_second")

WPS verileri
max_dom = 1
start_date = '2016-10-06_00:00:00',
end_date = '2016-10-08_00:00:00',
interval_seconds = 21600,
prefix = 'FILE',


max_dom = 1 
parent_id = 1,
parent_grid_ratio = 1,
i_parent_start = 1,
j_parent_start = 1,
e_we = 91,
e_sn = 100,
geog_data_res = 'default',
dx = 27000,
dy = 27000,
map_proj = 'mercator',
ref_lat = 28.00,
ref_lon = -75.00,
truelat1 = 30.0,
truelat2 = 60.0,
stand_lon = -75.0,
geog_data_path = 'Your WPS_GEOG data location' 

"""

"""
WRF verileri

run_days = 0,
run_hours = 48,
run_minutes = 0,
run_seconds = 0,
start_year = 2016,
start_month = 10,
start_day = 06,
start_hour = 00,
end_year = 2016,
end_month = 10,
end_day = 08,
end_hour = 00,
interval_seconds = 21600
input_from_file = .true.,
history_interval = 180,
frames_per_outfile = 1,
restart = .false.,
restart_interval = 1440,
time_step = 150,
max_dom = 1,
e_we = 91,
e_sn = 100,
e_vert = 45,
num_metgrid_levels = 32
dx = 27000,
dy = 27000,
"""

app.run(port=5000)
