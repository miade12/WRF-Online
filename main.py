# importing Flask and other modules
from flask import Flask, request, render_template, url_for, redirect
from typing import Optional
import os


app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=["GET", "POST"])
def dom():

    return render_template("index.html")


@app.route('/wps', methods=["GET", "POST"])
def wps():

    global sd
    sd = request.form.get("start_date")
    global ed
    ed = request.form.get("end_date")
    global isec
    isec = request.form.get("interval_seconds")
    #forecastHour hesaplamaları
    forecastHour = ""
    saat = int(int(isec)/3600)
    if saat < 10:
        forecastHour = "00" + str(saat)
    elif saat < 100:
        forecastHour = "0" + str(saat)
    else:
        forecastHour = str(saat)

    get_data = 'cd /home/miade/Build_WRF/DATA/ && wget ' \
               'https://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs' \
               '.{tarih}/{saatBaslangici}/atmos/gfs.t{saatBaslangici}z.pgrb2.1p00.f{forecastHour}'.\
        format(tarih=sd.split("_")[0].replace("-", ""), saatBaslangici=sd.split("_")[1].split(":")[0], forecastHour=forecastHour)
    
    os.system(get_data)
    get_data2 = 'cd /home/miade/Build_WRF/DATA/ && wget ' \
               'https://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs' \
               '.{tarih}/{saatBaslangici}/atmos/gfs.t{saatBaslangici}z.pgrb2.1p00.f000'. \
        format(tarih=sd.split("_")[0].replace("-", ""), saatBaslangici=sd.split("_")[1].split(":")[0])

    os.system(get_data2)

    familiar = 'cd /home/miade/Build_WRF/WPS-4.3/util/ && ./g2print.exe ' \
               '/home/miade/Build_WRF/DATA/gfs* >& g2print.log'
    os.system(familiar)
    gfsvtables = 'cd /home/miade/Build_WRF/WPS-4.3/ && ln -sf ungrib/Variable_Tables/Vtable.GFS Vtable'
    os.system(gfsvtables)
    linkgribdata = 'cd /home/miade/Build_WRF/WPS-4.3/ && ./link_grib.csh /home/miade/Build_WRF/DATA/gfs '
    os.system(linkgribdata)

    with open("/home/miade/Build_WRF/WPS-4.3/namelist.wps", "w") as fo:
        fo.write("&share\n")
        fo.write("wrf_core = 'ARW' ,\n")
        fo.write("max_dom = 1,\n")
        fo.write("start_date = '{}' ,\n".format(sd))
        fo.write("end_date = '{}' ,\n".format(ed))
        fo.write("interval_seconds = {} ,\n".format(isec))
        fo.write("/\n")
        fo.write("&geogrid\n"
              "parent_id = 1,\n"
              "parent_grid_ratio = 1,\n"
              " i_parent_start    =   1,\n"
              " j_parent_start    =   1,\n"
              " e_we              =  91,\n"
              " e_sn              =  100,\n"
              " geog_data_res = 'default',\n"
              " dx = 27000,\n"
              " dy = 27000,\n"
              " map_proj = 'mercator',\n"
              " ref_lat   =  28.00,\n"
              " ref_lon   = -75.00,\n"
              " truelat1  =  30.0,\n"
              " truelat2  =  60.0,\n"
              " stand_lon = -75.0,\n"
              " geog_data_path = '/home/miade/Build_WRF/WPS_GEOG'\n"
              "/\n"
              "&ungrib\n"
              " out_format = 'WPS',\n"
              " prefix = 'FILE',\n"
              "/\n"
              "&metgrid\n"
              " fg_name = 'FILE'\n"
              "/")
        fo.close()

        os.system("cd /home/miade/Build_WRF/WPS-4.3/ && ./ungrib.exe")

    return render_template('wps.html')


@app.route('/domain', methods=["GET", "POST"])
def domain():
    e_we = request.form.get("e_we")
    e_sn = request.form.get("e_sn")
    dx = request.form.get("dx")
    dy = request.form.get("dy")
    ref_lat = request.form.get("ref_lat")
    ref_lon = request.form.get("ref_lon")
    truelat1 = request.form.get("truelat1")
    truelat2 = request.form.get("truelat2")
    stand_lon = request.form.get("stand_lon")
    with open("/home/miade/Build_WRF/WPS-4.3/namelist.wps", "w") as fo:
        fo.write("&share\n")
        fo.write("wrf_core = 'ARW' ,\n")
        fo.write("max_dom = 1,\n")
        fo.write("start_date = '{}' ,\n".format(sd))
        fo.write("end_date = '{}' ,\n".format(ed))
        fo.write("interval_seconds = {} ,\n".format(isec))
        fo.write("/\n")
        fo.write("&geogrid \n"
                 "parent_id = 1,\n"
                 "parent_grid_ratio = 1,\n"
                 " i_parent_start    =   1, \n"
                 " j_parent_start    =   1,\n"
                 " e_we              =  {e_we} ,\n"
                 " e_sn              =  {e_sn} ,\n"
                 " geog_data_res = 'default',\n"
                 " dx = {dx} ,\n"
                 " dy = {dy},\n"
                 " map_proj = 'mercator',\n"
                 " ref_lat   =  {ref_lat},\n"
                 " ref_lon   = {ref_lon},\n"
                 " truelat1  =  {truelat1},\n"
                 " truelat2  =  {truelat2},\n"
                 " stand_lon = {stand_lon},\n"
                 " geog_data_path = '/home/miade/Build_WRF/WPS_GEOG'\n"
                 "/\n"
                 "&ungrib\n"
                 " out_format = 'WPS',\n"
                 " prefix = 'FILE',\n"
                 "/\n"
                 "&metgrid\n"
                 " fg_name = 'FILE'\n"
                 "/\n".format(e_we=e_we, e_sn=e_sn, dx=dx, dy=dy, ref_lat=ref_lat, ref_lon=ref_lon, truelat1=truelat1, truelat2=truelat2, stand_lon=stand_lon))
        fo.close()
        os.system("cd /home/miade/Build_WRF/WPS-4.3/ && ./geogrid.exe")
    return render_template('geogrid_ncl.html')


@app.route('/wrf', methods=["GET", "POST"])
def wrf():
    pass
    return render_template('wrf.html')


app.run(port=5000)


"""


    
    
    
    
        sd = request.form.get("start_date")
        ed = request.form.get("end_date")
        isec = request.form.get("interval_seconds")
        get_data = 'cd /home/miade/Build_WRF/DATA/matthew && curl ' \
                   'https://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs' \
                   '.{}/06/atmos/gfs.t06z.pgrb2.0p25.f001'.format(sd)
        os.system(get_data)
        os.system("/home/miade/Build_WRF/WPS-4.3/util/g2print.exe /home/miade"
                  "/Build_WRF/DATA/matthew >& g2print.log")
        os.system("ln -sf /home/miade/Build_WRF/WPS-4.3/ungrib/Variable_Tables/Vtable.GFS Vtable")
        os.system("/home/miade/Build_WRF/WPS-4.3/link_grib.csh /home/miade/Build_WRF/DATA/matthew/gfs")

        file = open('home/miade/Build_WRF/WPS-4.3/namelist.wps', "w")
        print("&share")
        print("wrf_core = 'ARW' ,")
        print("max_dom = 1,")
        print("start_date = '{}' ,".format(sd), file=file)
        print("end_date = '{}' ,".format(ed), file=file)
        print("interval_seconds = '{}' ,".format(isec), file=file)
        print("&geogrid "
              "parent_id = 1,"
              "parent_grid_ratio = 1,"
              " i_parent_start    =   1, "
              " j_parent_start    =   1,"
              " e_we              =  91,"
              " e_sn              =  100,"
              " geog_data_res = 'default',"
              " dx = 27000,"
              " dy = 27000,"
              " map_proj = 'mercator',"
              " ref_lat   =  28.00,"
              " ref_lon   = -75.00,"
              " truelat1  =  30.0,"
              " truelat2  =  60.0,"
              " stand_lon = -75.0,"
              " geog_data_path = '../WPS_GEOG'"
              "/"
              "&ungrib"
              " out_format = 'WPS',"
              " prefix = 'FILE',"
              "/"
              "&metgrid"
              " fg_name = 'FILE'"
              "/")
        os.system("./ungrib.exe")

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



<!DOCTYPE html>
<html>
<head>
  <title>WRF-Online</title>
  <style>
    body {
    background-color: rgb(228, 237, 232);
    }

    .header {
    font-size: 40px;
    }

  </style>

</head>
  <body>
  <div style="text-align:center; color: white;background-color:rgb(22,8,90);">
   <p class="header" > WRF-Online</p>
  </div>
    <form method="post" action="http://127.0.0.1:5000/wps" >
      <center>
        <h3>Unpack input GRIB data</h3>
        <table>

          <tbody>

            <tr>Start Date &nbsp &nbsp &nbsp &nbsp &nbsp<input type="text"
                                             id="start_date"
                                             name="start_date"
                                             value="2016-10-06_00:00:00">(yyyy-mm-dd_HH:mm:ss)</tr>
            <br>
            <br>
            <tr>End Date &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp<input type="text"
                                          id="end_date"
                                          name="end_date"
                                          value="2016-10-06_00:00:00"> (yyyy-mm-dd_HH:mm:ss) </tr>
            <br>
            <br>
            <tr>Interval seconds &nbsp<input type="text"
                                                    id="interval_seconds"
                                                    name="interval_seconds"
                                                    value="21600"></tr>
            <br>
            <br>
             <tr><input value="Run ungrib.exe" type="submit"
                                                name="ungrib.exe"
                                                id="ungrib.exe" ></tr>
          </tbody>
        </table>



      </center>




    </form>

  <footer>

  <div align="center"><img style="width:10%;padding-top:10%;" src="/static/itulogo.png" alt="logo"></div>
  </footer>
  </body>
</html>



"""


