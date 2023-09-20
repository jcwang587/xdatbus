import xdatbus as xdb

aimd_path = 'B:/projects/04_1d_metad_cn/21_100K'

xdb.f01_aggregate(aimd_path, load_last_xdatcar=True)
xdb.f02_unwrap('XDATBUS')