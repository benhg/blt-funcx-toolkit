def setup_ftp_conn(username=None, privkey=None):
    if not username:
        username = getpass.getuser()
    try:
        if not privkey:
            conn = pysftp.Connection('mayo.blt.lclark.edu', username=username)
        else:
            conn = pysftp.Connection('mayo.blt.lclark.edu',
                                     username=username,
                                     private_key=privkey)
    except:
        password = getpass.getpass()
        conn = pysftp.Connection('mayo.blt.lclark.edu',
                                 username=username,
                                 password=password)
    return conn


def check_files(local_path, remote_path, connection):
    if not local_path or not remote_path:
        print("ERROR: Local Path and Remote Path are Required.")
        sys.exit(1)


def upload_file_to_blt(local_path=None, remote_path="~", username=None, force=False):
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


def download_file_from_blt(local_path=".", remote_path=None, username=None,  force=False):
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