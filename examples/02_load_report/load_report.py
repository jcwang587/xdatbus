import xdatbus as xdb

aimd_path = '../metad'

cv = xdb.fm03_report_loader(aimd_path, load_last_report=True)

