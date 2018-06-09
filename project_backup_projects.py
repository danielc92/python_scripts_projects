import shutil
import datetime as dt

stamp = dt.datetime.now().strftime("_%d-%m-%Y_%H-%M-%S-%p")

#windows
# backup_folder_path = "C:/Users/admin-vicvphq/Desktop/PYTHON_BACKUP"+ stamp +"/"
# pycharm_project_path = 'C:/Users/admin-vicvphq/danielc_pycharm_project/'

#mac
backup_folder_path = "/Users/danielcorcoran/Desktop/Pycharm_FullBackup"+ stamp +"/"
pycharm_project_path = '/Users/danielcorcoran/PycharmProjects/daniels_mac_proj/'

shutil.copytree(pycharm_project_path, backup_folder_path)