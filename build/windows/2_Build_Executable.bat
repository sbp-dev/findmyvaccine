call conda activate fmv_gui
pyinstaller -w -F ^
-i vaccine_32px.ico ^
--add-data "../../src/.resources;." ^
../../src/findmyvaccine.py 