# importing Flask and other modules
from time import sleep

from flask import Flask, request, render_template, url_for, redirect, send_file
from typing import Optional
import os
import subprocess
from datetime import date
import threading

app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=["GET", "POST"])
def un():
    if request.method == "POST":
        global sd
        sd = request.form.get("start_date") # string şeklinde yyyy-aa-gg formatında
        global ed
        ed = request.form.get("end_date")
        global isec
        isec = request.form.get("interval_seconds")
        global gfs_baslangic_saati
        gfs_baslangic_saati = request.form.get("gfsBaslangicSaati")
        global gfs_bitis_saati
        gfs_bitis_saati= request.form.get("gfsBitisSaati")

        """""
        sd_year = sd.split("_")[0].replace("-", "")[0:4]
        sd_month = sd.split("_")[0].replace("-", "")[4:6]
        sd_days = sd.split("_")[0].replace("-", "")[6:8]
        sd_hours = sd.split("_")[1].replace("-", "")[0:2]
        d0 = date(int(sd_year), int(sd_month), int(sd_days))

        ed_year = ed.split("_")[0].replace("-", "")[0:4]
        ed_month = ed.split("_")[0].replace("-", "")[4:6]
        ed_days = ed.split("_")[0].replace("-", "")[6:8]
        ed_hours = ed.split("_")[1].replace("-", "")[0:2]
        d1 = date(int(ed_year), int(ed_month), int(ed_days))
        """""
        d0 = date(int(sd.split('-')[0]), int(sd.split('-')[1]), int(sd.split('-')[2]))
        d1 = date(int(ed.split('-')[0]), int(ed.split('-')[1]), int(ed.split('-')[2]))
        global fark_saat
        fark_saat = (int(gfs_bitis_saati) - int(gfs_baslangic_saati))
        global farkdate
        farkdate = d1 - d0
        hour = (farkdate.days)*24 + int(fark_saat)

        adimsayisi = int(isec)

        for i in range(0, int(hour)+int(adimsayisi), int(adimsayisi)):

            forecastHour = ""
            if int(i / 100) != 0:
               forecastHour = "f" + str(i)
            elif int(i / 10) != 0:
               forecastHour = "f0" + str(i)
            else:
               forecastHour = "f00" + str(i)

            get_data = 'cd /home/miade/Build_WRF/DATA/ && wget ' \
                       'https://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs' \
                       '.{tarih}/{saatBaslangici}/atmos/gfs.t{saatBaslangici}z.pgrb2.1p00.{forecastHour}'\
                       .format(tarih=sd.replace("-", ""), saatBaslangici=gfs_baslangic_saati,
                               forecastHour=forecastHour)
            os.system(get_data)


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
            fo.write("start_date = '{}' ,\n".format(sd+"_"+gfs_baslangic_saati+":00:00"))
            fo.write("end_date = '{}' ,\n".format(ed+"_"+gfs_bitis_saati+":00:00"))
            fo.write("interval_seconds = {} ,\n".format(str(int(isec)*3600)))
            fo.write("/\n")
            fo.write(
                "&geogrid\n"
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
                " ref_lat   =  60.00,\n"
                " ref_lon   = 45.00,\n"
                " truelat1  =  30.0,\n"
                " truelat2  =  60.0,\n"
                " stand_lon = 45.0,\n"
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
        return redirect(url_for('wps'))
    else:
        return render_template("index.html")


@app.route('/wps', methods=["GET", "POST"])
def wps():
    if request.method == "POST":
        global e_we
        e_we = request.form.get("e_we")
        global e_sn
        e_sn = request.form.get("e_sn")
        global dxdy
        dxdy = request.form.get("dxdy")
        global ref_lat
        ref_lat = request.form.get("ref_lat")
        global ref_lon
        ref_lon = request.form.get("ref_lon")
        global truelat1
        truelat1 = request.form.get("truelat1")
        global truelat2
        truelat2 = request.form.get("truelat2")
        global stand_lon
        stand_lon = request.form.get("stand_lon")
        with open("/home/miade/Build_WRF/WPS-4.3/namelist.wps", "w") as fo:
            fo.write("&share\n")
            fo.write("wrf_core = 'ARW' ,\n")
            fo.write("max_dom = 1,\n")
            fo.write("start_date = '{}' ,\n".format(sd+"_"+gfs_baslangic_saati+":00:00"))
            fo.write("end_date = '{}' ,\n".format(ed+"_"+gfs_bitis_saati+":00:00"))
            fo.write("interval_seconds = {} ,\n".format(str(int(isec)*3600)))
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
                     " map_proj = 'lambert',\n"
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
                     "/\n".format(e_we=e_we, e_sn=e_sn, dx=dxdy+"000", dy=dxdy+"000", ref_lat=ref_lat, ref_lon=ref_lon, truelat1=truelat1,
                                  truelat2=truelat2, stand_lon=ref_lon))
            fo.close()
        ncl_domain = 'cd /home/miade/PycharmProjects/WRF-Online/static &&' \
                     'ncl plotgrids_new.ncl'

        threading.Thread(target=os.system, args=(ncl_domain,)).start() #os.system(ncl_domain)
        sleep(10)
        return redirect(url_for('domain'))
    else:

        return render_template("wps.html")


@app.route('/domain', methods=["GET", "POST"])
def domain():
    if request.method == "POST":
        os.system("cd /home/miade/Build_WRF/WPS-4.3/ && ./geogrid.exe")
        os.system("cd /home/miade/Build_WRF/WPS-4.3/ && ./metgrid.exe")
        link_metgrid = "cd /home/miade/Build_WRF/WRF-4.3-ARW/test/em_real/ && " \
                       "ln -sf /home/miade/Build_WRF/WPS-4.3/met_em* /home/miade/Build_WRF/WRF-4.3-ARW/test/em_real/ "
        os.system(link_metgrid)
        return redirect(url_for('wrf'))

    else:
        return render_template("domain.html")


@app.route('/wrf', methods=["GET", "POST"])
def wrf():
    if request.method == "POST":
        if fark_saat < 0:
            run_days = farkdate.days - 1
            run_hours = 24 + fark_saat
        else:
            run_days = farkdate.days
            run_hours = fark_saat
        microphy = request.form.get("microphy")
        pbl = request.form.get("pbl")
        cumulus = request.form.get("cumulus")
        core = request.form.get("core")

        start_year = sd.split('-')[0]
        start_month = sd.split('-')[1]
        start_day = sd.split('-')[2]
        start_hour = gfs_baslangic_saati
        end_year = ed.split('-')[0]
        end_month = ed.split('-')[1]
        end_day = ed.split('-')[2]
        end_hour = gfs_bitis_saati
        interval_seconds = str(int(isec)*3600)

        with open("/home/miade/Build_WRF/WRF-4.3-ARW/test/em_real/namelist.input", "w") as fo:
            fo.write(
                "&time_control \n"
                "run_days = {run_days},\n"
                "run_hours = {run_hours},\n"
                "run_minutes = {run_minutes},\n"
                "run_seconds = {run_seconds},\n"
                "start_year = {start_year},\n"
                "start_month = {start_month},\n"
                "start_day = {start_day},\n"
                "start_hour = {start_hour},\n"
                "end_year = {end_year},\n"
                "end_month = {end_month},\n"
                "end_day = {end_day},\n"
                "end_hour = {end_hour},\n"
                "interval_seconds = {interval_seconds}\n"
                "input_from_file =.true.,\n"
                "history_interval = 180,\n"
                "frames_per_outfile = 1,\n"
                "restart =.false.,\n"
                "restart_interval = 1440,\n"
                "io_form_history = 2\n"
                "io_form_restart = 2\n"
                "io_form_input = 2\n"
                "io_form_boundary = 2\n"
                "/\n"
    
                "&domains\n"
                "time_step = 150,\n"
                "use_adaptive_time_step              = .true., \n"
                "step_to_output_time                 = .true., \n"
                "target_cfl                          = 1.2, 1.2, 1.2, \n"
                "max_step_increase_pct               = 5, 51, 51, \n"
                "starting_time_step                  = -1, -1,-1, \n"
                "max_time_step                       = -1, -1,-1, \n"
                "min_time_step                       = -1, -1,-1, \n"
                "adaptation_domain                   = 1, \n"
                "time_step_fract_num = 0,\n"
                "time_step_fract_den = 1,\n"
                "max_dom = 1,\n"
                "e_we = {e_we},\n"
                "e_sn = {e_sn},\n"
                "e_vert = 45,\n"
                "dzstretch_s = 1.1\n"
                "p_top_requested = 5000,\n"
                "num_metgrid_levels = 34,\n"
                "num_metgrid_soil_levels = 4,\n"
                "dx = {dx},\n"
                "dy = {dy},\n"
                "grid_id = 1,\n"
                "parent_id = 0,\n"
                "i_parent_start = 1,\n"
                "j_parent_start = 1,\n"
                "parent_grid_ratio = 1,\n"
                "parent_time_step_ratio = 1,\n"
                "feedback = 1,\n"
                "smooth_option = 0\n"
                "/\n"
                "&physics\n"
                "physics_suite = 'CONUS'\n"
                "mp_physics = {microphy}, -1,\n"
                "cu_physics = {cumulus}, -1,\n"
                "ra_lw_physics = -1, -1,\n"
                "ra_sw_physics = -1, -1,\n"
                "bl_pbl_physics = {pbl}, -1,\n"
                "sf_sfclay_physics = {pbl}, -1,\n"
                "sf_surface_physics = -1, -1,\n"
                "radt = 15, 15,\n"
                "bldt = 0, 0,\n"
                "cudt = 0, 0,\n"
                "icloud = 1,\n"
                "num_land_cat = 21,\n"
                "sf_urban_physics = 0, 0,\n"
                "fractional_seaice = 1,\n"
                "/\n"
    
                "&fdda\n"
                "/\n"
    
                "&dynamics\n"
                "hybrid_opt = 2,\n"
                "w_damping = 0,\n"
                "diff_opt = 2, 2,\n"
                "km_opt = 4, 4,\n"
                "diff_6th_opt = 0, 0,\n"
                "diff_6th_factor = 0.12, 0.12,\n"
                "base_temp = 290.\n"
                "damp_opt = 3,\n"
                "zdamp = 5000., 5000.,\n"
                "dampcoef = 0.2, 0.2,\n"
                "khdif = 0, 0,\n"
                "kvdif = 0, 0,\n"
                "non_hydrostatic =.true.,.true.,\n"
                "moist_adv_opt = 1, 1,\n"
                "scalar_adv_opt = 1, 1,\n"
                "gwd_opt = 1, 0,\n"
                "/\n"
    
                "&bdy_control\n"
                "spec_bdy_width = 5,\n"
                "specified =.true.\n"
                "/\n"
    
                "&grib2\n"
                "/\n"
    
                "&namelist_quilt\n"
                "nio_tasks_per_group = 0,\n"
                "nio_groups = 1,"
                "/\n".format(run_days=str(run_days), run_hours=str(run_hours), run_minutes="00",
                             run_seconds="00", start_year=start_year, start_month=start_month,
                                         start_day=start_day, start_hour=start_hour, end_year=end_year,
                                         end_month=end_month, end_day=end_day, end_hour=end_hour,
                                         interval_seconds=interval_seconds, e_we=e_we, e_sn=e_sn, dx=dxdy+"000",
                             dy=dxdy+"000", microphy=microphy, cumulus=cumulus, pbl=pbl))

        delete_prev_outputs = "rm /home/miade/Build_WRF/WRF-4.3-ARW/test/em_real/wrfout* " \
                              "/home/miade/Build_WRF/WRF-4.3-ARW/test/em_real/outputs.zip"

        os.system(delete_prev_outputs)


        return redirect(url_for('output'))
    else:
        return render_template("wrf.html")


@app.route('/output', methods=["GET", "POST"])
def output():
    if request.method == "GET":

        realrun = "cd /home/miade/Build_WRF/WRF-4.3-ARW/test/em_real && ./real.exe"
        wrfrun = "cd /home/miade/Build_WRF/WRF-4.3-ARW/test/em_real && ./wrf.exe"
        os.system(realrun)
        os.system(wrfrun)

        create_tar_file = "zip /home/miade/Build_WRF/WRF-4.3-ARW/test/em_real/outputs.zip " \
                          "/home/miade/Build_WRF/WRF-4.3-ARW/test/em_real/wrfout*"
        os.system(create_tar_file)
        return render_template('output.html')
    else:
        return send_file("/home/miade/Build_WRF/WRF-4.3-ARW/test/em_real/outputs.zip", as_attachment=True)


@app.route('/download', methods=["GET", "POST"])
def download():

    return send_file("/home/miade/Build_WRF/WRF-4.3-ARW/test/em_real/outputs.zip", as_attachment=True)


app.run(port=5000)


"""
   # forecastHour hesaplamaları
        forecastHour = ""
        saat = int(int(isec) / 3600)
        if saat < 10:
            forecastHour = "00" + str(saat)
        elif saat < 100:
            forecastHour = "0" + str(saat)
        else:
            forecastHour = str(saat)
            
            
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
    
       
fin = open('/home/miade/PycharmProjects/WRF-Online/wrf_static/test_namelist_wps.py', 'wt')
        
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


