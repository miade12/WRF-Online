content = """& time_control
run_days = {run_days},
run_hours = {run_hours},
run_minutes = {run_minutes},
run_seconds = {run_seconds},
start_year = {start_year},
start_month = {start_month},
start_day = {start_day},
start_hour = {start_hour},
end_year = {end_year},
end_month = {end_month},
end_day = {end_day},
end_hour = {end_hour},
interval_seconds = {interval_seconds}
input_from_file =.true.,
history_interval = 180,
frames_per_outfile = 1,
restart =.false.,
restart_interval = 1440,
io_form_history = 2
io_form_restart = 2
io_form_input = 2
io_form_boundary = 2
/

& domains
time_step = 150,
time_step_fract_num = 0,
time_step_fract_den = 1,
max_dom = 1,
e_we = {e_we},
e_sn = {e_sn},
e_vert = {e_vert},
dzstretch_s = 1.1
p_top_requested = 5000,
num_metgrid_levels = {num_metgrid_levels},
num_metgrid_soil_levels = 4,
dx = {dx},
dy = {dy},
grid_id = 1,
parent_id = 0,
i_parent_start = 1,
j_parent_start = 1,
parent_grid_ratio = 1,
parent_time_step_ratio = 1,
feedback = 1,
smooth_option = 0
/

& physics
physics_suite = 'CONUS'
mp_physics = -1, -1,
cu_physics = -1, -1,
ra_lw_physics = -1, -1,
ra_sw_physics = -1, -1,
bl_pbl_physics = -1, -1,
sf_sfclay_physics = -1, -1,
sf_surface_physics = -1, -1,
radt = 15, 15,
bldt = 0, 0,
cudt = 0, 0,
icloud = 1,
num_land_cat = 21,
sf_urban_physics = 0, 0,
fractional_seaice = 1,
/

& fdda
/

& dynamics
hybrid_opt = 2,
w_damping = 0,
diff_opt = 2, 2,
km_opt = 4, 4,
diff_6th_opt = 0, 0,
diff_6th_factor = 0.12, 0.12,
base_temp = 290.
damp_opt = 3,
zdamp = 5000., 5000.,
dampcoef = 0.2, 0.2,
khdif = 0, 0,
kvdif = 0, 0,
non_hydrostatic =.true.,.true.,
moist_adv_opt = 1, 1,
scalar_adv_opt = 1, 1,
gwd_opt = 1, 0,
/

& bdy_control
spec_bdy_width = 5,
specified =.true.
/

& grib2
/

& namelist_quilt
nio_tasks_per_group = 0,
nio_groups = 1,
/"""
