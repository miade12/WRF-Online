# importing Flask and other modules
from typing import Optional

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=["POST"])
def wps():
    if request.method == "POST":
        sd = request.form.get("start-date")
        with open("/home/miade/Desktop/test/test", "w") as fo:
            fo.write(sd)
        return render_template('index.html')


"""
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
