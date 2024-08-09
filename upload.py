import datetime
import os
from dotenv import load_dotenv
from ftplib import FTP

load_dotenv(override = True)

user = os.getenv("ftp_user")
password = os.getenv("ftp_password")
host = os.getenv("ftp_host")
remote_root = os.getenv("ftp_remote_root")
local_root = "easai.org/bin/Debug/net7.0/win-x86/publish"

ftp = FTP(host)
ftp.login(user, password)

last_upload_file = "output/last_upload.txt"
last_upload_time = None
if os.path.exists(last_upload_file):
	with open(last_upload_file) as f:
		last_upload_time = float(f.read())

def upload_file(file_name, file_path):
	file_changed_time = os.path.getctime(file_path)
	if last_upload_time and file_changed_time <= last_upload_time:
		return
	print("  Uploading file", file_name)
	with open(file_path, "rb") as f:
		ftp.storbinary(f"STOR {file_name}", f)

def upload_files_recursively(local_folder = local_root, remote_folder = remote_root, child_folder = ""):
	local_folder_path = local_folder
	remote_folder_path = remote_folder
	if len(child_folder) > 0:
		local_folder_path = local_folder + "/" + child_folder
		remote_folder_path = remote_folder + "/" + child_folder
		if not remote_folder_path in ftp.nlst(remote_folder):
			print(f"Creating folder {child_folder} in {remote_folder}")
			ftp.cwd(remote_folder)
			ftp.mkd(child_folder)
	print(f"Uploading folder {local_folder_path} to {remote_folder_path}:")
	for name in os.listdir(local_folder_path):
		ftp.cwd(remote_folder_path)
		path = os.path.join(local_folder_path, name)
		if os.path.isdir(path):
			upload_files_recursively(local_folder_path, remote_folder_path, name)
		else:
			upload_file(name, path)
	expected_remote_files = [remote_folder_path + "/" + name for name in os.listdir(local_folder_path)]
	for remote_file in ftp.nlst(remote_folder_path):
		if ".well-known" not in remote_file and remote_file not in expected_remote_files:
			print(f"Deleting {remote_file} in {remote_folder_path}")
			ftp.delete(remote_file)

upload_files_recursively()

with open(last_upload_file, "w") as f:
	f.write(str(datetime.datetime.now().timestamp()))