import xdatbus as xdb

aimd_path = '../metad'

xdb.f01_aggregate(aimd_path, load_last_xdatcar=True)
xdb.f02_unwrap('XDATBUS')