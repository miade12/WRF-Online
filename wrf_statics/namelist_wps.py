content = """&share
 wrf_core = 'ARW',
 max_dom = {max_dom},
 start_date = '{start_date}','2019-09-04_12:00:00',
 end_date   = '{end_date}','2019-09-04_12:00:00',
 interval_seconds = {interval_seconds},
 
/

&geogrid
 parent_id         =   {parent_id},   
 parent_grid_ratio =   {parent_grid_ratio},  
 i_parent_start    =   {i_parent_start}, 
 j_parent_start    =   {j_parent_start},
 e_we              =  {e_we},
 e_sn              =  {e_sn},
 geog_data_res = 'default',
 dx = {dx},
 dy = {dy},
 map_proj = '{map_proj}',
 ref_lat   =  {ref_lat},
 ref_lon   = {ref_lon},
 truelat1  =  {truelat1},
 truelat2  =  {truelat2},
 stand_lon = {stand_lon},
 geog_data_path = '../WPS_GEOG'
/

&ungrib
 out_format = 'WPS',
 prefix = 'FILE',
/

&metgrid
 fg_name = 'FILE'
/"""
