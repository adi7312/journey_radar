import os
import zipfile
import pandas as pd
import requests


BASE_DIR = "./static/"
os.makedirs(BASE_DIR, exist_ok=True)

url_a = "https://gtfs.ztp.krakow.pl/GTFS_KRK_A.zip"
url_m = "https://gtfs.ztp.krakow.pl/GTFS_KRK_M.zip"
url_t = "https://gtfs.ztp.krakow.pl/GTFS_KRK_T.zip"

files = ['GTFS_KRK_A.zip', 'GTFS_KRK_M.zip', 'GTFS_KRK_T.zip']

urls = [url_a, url_m, url_t]

for url, file in zip(urls, files):
    response = requests.get(url)

    with open(f'{BASE_DIR}{file}', "wb") as f:
        f.write(response.content)


zip_files = {
    "T": os.path.join(BASE_DIR, "GTFS_KRK_T.zip"),
    "A": os.path.join(BASE_DIR, "GTFS_KRK_A.zip"),
    "M": os.path.join(BASE_DIR, "GTFS_KRK_M.zip")
}

for prefix, zip_path in zip_files.items():
    extract_dir = os.path.join(BASE_DIR, prefix)
    os.makedirs(extract_dir, exist_ok=True)
    print(f"Rozpakowuję {zip_path} do {extract_dir}...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

target_files = ["trips.txt", "stops.txt", "stop_times.txt", "routes.txt"]

for filename in target_files:
    combined = []
    for prefix in zip_files.keys():
        path = os.path.join(BASE_DIR, prefix, filename)
        if os.path.exists(path):
            df = pd.read_csv(path)
            df["source"] = prefix
            combined.append(df)
    if combined:
        merged = pd.concat(combined, ignore_index=True)
        output_file = os.path.join(BASE_DIR, filename.replace(".txt", ".csv"))
        merged.to_csv(output_file, index=False)
        print(f"Zapisano {output_file}")
