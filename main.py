import requests
import datetime
import shutil
import tarfile
from tqdm import tqdm
import os
from glob import glob
import sys
import shutil

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        chunk_size = 1024 * 1024 
        with open(local_filename, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=local_filename) as pbar:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

start_date = datetime.datetime.fromisoformat(sys.argv[1])
end_date = datetime.datetime.fromisoformat(sys.argv[2])
date = start_date

while date <= end_date:
    str_date = date.strftime("%Y.%m.%d")
    url = f"https://github.com/adsblol/globe_history_{date.year}/releases/download/v{str_date}-planes-readsb-prod-0/v{str_date}-planes-readsb-prod-0.tar"
    
    download_file(url+".aa", "data.tar.aa")
    download_file(url+".ab", "data.tar.ab")
    
    with open('data.tar', 'wb') as destination:
        for filename in ['data.tar.aa', 'data.tar.ab']:
            with open(filename, 'rb') as source:
                shutil.copyfileobj(source, destination)
    
    with tarfile.open("data.tar", "r:*") as tar:
        members = [m for m in tar.getmembers() if m.name.startswith("./heatmap")]
        tar.extractall(members=members)

    # call the data processing thing
    
    for file in glob(url+"*"):
        os.remove(file)
    for file in glob("data.*"):
        os.remove(file)
    shutil.rmtree("heatmap")

    date += datetime.timedelta(days=1)
