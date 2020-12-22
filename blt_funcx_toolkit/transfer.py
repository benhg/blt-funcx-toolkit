import getpass
import sys
import os
import subprocess
import random

import pysftp

from blt_funcx_toolkit.config import *
from blt_funcx_toolkit.execution import run_console_cmd


def setup_ftp_conn(username=None, privkey=None):
    """
    Open FTP connection to BLT

    Uses the following protocol for authentication:

    1. If no `username` provided, assume BLT username
        is local username
    2. If path to private key passed, use private key
    3. Else, attempt to use default `~/.ssh/id_rsa`
    4. If that fails, ask user for password.


    """
    if not username:
        username = getpass.getuser()
    try:
        if not privkey:
            conn = pysftp.Connection(BLT_LOGIN_ADDRESS, username=username)
        else:
            conn = pysftp.Connection(BLT_LOGIN_ADDRESS,
                                     username=username,
                                     private_key=privkey)
    except:
        password = getpass.getpass()
        conn = pysftp.Connection(BLT_LOGIN_ADDRESS,
                                 username=username,
                                 password=password)
    return conn


def check_files(local_path, remote_path, connection):
    if not local_path or not remote_path:
        print("ERROR: Local Path and Remote Path are Required.")
        sys.exit(1)


def ftp_upload_file_to_blt(local_path=None,
                           remote_path="~",
                           username=None,
                           force=False):
    """
    Upload a file or directory to BLT using FTP

    :param local_path: Path where file should be saved
    :param remote_path: Path where file is currently
    :param username: Remote host username
    :param force: Do not ask user to overwrite existing files
    """
    print(f"Uploading {local_path} to BLT at location {remote_path}")
    conn = setup_ftp_conn(username)
    check_files(local_path, remote_path, conn)
    local_path = os.path.abspath(local_path)

    if not (os.path.isfile(local_path) or os.path.isdir(local_path)):
        print(f"ERROR: Local Path {local_path} Does not Exist")
        sys.exit(1)
    if conn.exists(remote_path) and not force:
        res = input(f"WARN: Remote File {remote_path} Exists. Continue? y/N: ")
        if res.lower() != "y":
            print("Aborting.")
            sys.exit(1)

    remote_dir = os.path.dirname(remote_path)
    conn.cd(remote_dir)
    # If it's a dir, assume you want the dirname to be the same
    if os.path.isdir(local_path):
        conn.makedirs(f"{remote_path}/{os.path.basename(local_path)}")
        conn.put_r(local_path,
                   f"{remote_path}/{os.path.basename(local_path)}/")
    else:
        conn.put(local_path, remote_path)


def ftp_download_file_from_blt(local_path=".",
                               remote_path=None,
                               username=None,
                               force=False):
    """
    Download a file or directory from BLT using FTP

    :param local_path: Path where file should be saved
    :param remote_path: Path where file is currently
    :param username: Remote host username
    :param force: Do not ask user to overwrite existing files
    """
    print(f"Downloading {remote_path} to BLT at location {local_path}")
    conn = setup_ftp_conn(username)
    check_files(local_path, remote_path, conn)
    local_path = os.path.abspath(local_path)

    if not conn.exists(remote_path):
        print(f"ERROR: Remote Path {remote_path} Does not Exist")
        sys.exit(1)
    if (os.path.isfile(local_path) or os.path.isdir(local_path)) and not force:
        res = input(f"WARN: Local File {local_path} Exists. Continue? y/N: ")
        if res.lower() != "y":
            print("Aborting.")
            sys.exit(1)
        os.remove(local_path)

    remote_dir = os.path.dirname(remote_path)
    conn.cd(remote_dir)
    # If it's a dir, assume you want the dirname to be the same
    if conn.isdir(remote_path):
        remote_basename = remote_path.split("/")[-1]
        os.makedirs(f"{os.path.dirname(local_path)}/{remote_basename}")
        conn.get_d(remote_path,
                   f"{os.path.dirname(local_path)}/{remote_basename}")
    else:
        conn.get(remote_path, local_path)


def croc_upload_file_to_blt(local_path=None, remote_path="~", force=False):
    """
    Upload a file or directory to BLT using Croc

    :param local_path: Path where file is currently
    :param remote_path: Path where file should be saved
                Must be an absolute path
                If a file is provided with a remote directly, we will
                place that file in the directory with the same name
    :param username: Remote host username
    :param force: Do not ask user to overwrite existing files
    """
    passphrase = f"blt-upload-{random.randint(0, 100000)}"
    output = subprocess.Popen(
        ["croc", "send", "--code", passphrase, local_path])
    print(passphrase)
    run_console_cmd(f"croc --yes {passphrase} --out {remote_path}")
    print(f"{local_path} has been uploaded to {remote_path} on BLT")


def croc_download_file_from_blt(local_path=None, remote_path="~", force=False):
    """
    Download a file or directory from BLT using Croc

    :param local_path: Path where file should be saved
    :param remote_path: Path where file is currently
    :param username: Remote host username
    :param force: Do not ask user to overwrite existing files
    """
    #remote_path = input("What is the path to the file you wish to upload?")
    output = run_console_cmd(f"croc send {remote_path}")
    passphrase = output.split("croc ", 1)
    if not local_path == None:
        os.system(f"cd {local_path}")
    #else:
    #local_path = input("What is the path you wish to upload the file to?")
    os.system(f"croc --yes {passphrase}")
    print(f"{remote_path} on BLT has been downloaded to {local_path}")


def upload_file_to_blt(local_path=None,
                       remote_path="~",
                       username=None,
                       force=False):
    """
    Upload a file or directory to BLT.

    Use FTP if it is available, otherwise use Croc

    :param local_path: Path where file should be saved
    :param remote_path: Path where file is currently
    :param username: Remote host username
    :param force: Do not ask user to overwrite existing files
    """
    if ftp_is_available(username=username):
        ftp_upload_file_to_blt(local_path=local_path,
                               remote_path=remote_path,
                               username=username,
                               force=force)
    else:
        croc_upload_file_to_blt(local_path=local_path,
                                remote_path=remote_path,
                                force=force)


def download_file_from_blt(local_path=None,
                           remote_path="~",
                           username=None,
                           force=False):
    """
    Download a file or directory from BLT.

    Use FTP if it is available, otherwise use Croc

    :param local_path: Path where file should be saved
    :param remote_path: Path where file is currently
    :param username: Remote host username
    :param force: Do not ask user to overwrite existing files
    """
    if ftp_is_available(username=username):
        ftp_upload_file_to_blt(local_path=local_path,
                               remote_path=remote_path,
                               username=username,
                               force=force)
    else:
        croc_upload_file_to_blt(local_path=local_path,
                                remote_path=remote_path,
                                force=force)


def ftp_is_available(username=None):
    """
    Check if FTP transfers from this computer
        to BLT are possible

    :return Boolean: True if FTP available.
    """
    try:
        setup_ftp_conn(username=username, privkey=None)
        return True
    except:
        return False
