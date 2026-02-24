import requests
import json
import os
import time

# --- CONFIGURATION API SOBRY AND DATA ---
API_PART_CU4 = "https://api.sobry.co/api/prices/tomorrow?turpe=CU4&profil=particulier"
API_PART_MU4 = "https://api.sobry.co/api/prices/tomorrow?turpe=MU4&profil=particulier"
API_PART_CU = "https://api.sobry.co/api/prices/tomorrow?turpe=CU&profil=particulier"
API_PART_MUDT = "https://api.sobry.co/api/prices/tomorrow?turpe=MUDT&profil=particulier"
API_PART_LU = "https://api.sobry.co/api/prices/tomorrow?turpe=LU&profil=particulier"
API_PRO_CU = "https://api.sobry.co/api/prices/tomorrow?turpe=CU&profil=pro"
API_PRO_LU = "https://api.sobry.co/api/prices/tomorrow?turpe=LU&profil=pro"
DATA_PART_CU4 = "data/particular/cu4"
DATA_PART_MU4 = "data/particular/mu4"
DATA_PART_MUDT = "data/particular/mudt"
DATA_PART_CU = "data/particular/cu"
DATA_PART_LU = "data/particular/lu"
DATA_PRO_CU = "data/pro/cu"
DATA_PRO_LU = "data/pro/lu"
RETENTION_DAYS = 30

# --- DATA DIRECTORY ---
if not os.path.exists(DATA_PART_CU4):
    os.makedirs(DATA_PART_CU4)

if not os.path.exists(DATA_PART_MU4):
    os.makedirs(DATA_PART_MU4)

if not os.path.exists(DATA_PART_MUDT):
    os.makedirs(DATA_PART_MUDT)

if not os.path.exists(DATA_PART_LU):
    os.makedirs(DATA_PART_LU)

if not os.path.exists(DATA_PART_CU):
    os.makedirs(DATA_PART_CU)

if not os.path.exists(DATA_PRO_LU):
    os.makedirs(DATA_PRO_LU)

if not os.path.exists(DATA_PRO_CU):
    os.makedirs(DATA_PRO_CU)

# --- FETCH NEW DATA ---
try:
    response = requests.get(API_PART_CU4)
    payload = response.json()
    
    if payload.get("success"):
        target_date = payload.get("date")
        filename = os.path.join(DATA_PART_CU4, f"tarifs_{target_date}_cu4_particulier.json")
        
        with open(filename, "w") as file:
            json.dump(payload, file)
        print(f"✅ Success: Saved {filename}")
    else:
        print("⚠️ (PARTICULIER CU4) No data available for tomorrow yet.")
except Exception as error:
    print(f"❌ API Error: {error}")

try:
    response = requests.get(API_PART_MU4)
    payload = response.json()
    
    if payload.get("success"):
        target_date = payload.get("date")
        filename = os.path.join(DATA_PART_MU4, f"tarifs_{target_date}_mu4_particulier.json")
        
        with open(filename, "w") as file:
            json.dump(payload, file)
        print(f"✅ Success: Saved {filename}")
    else:
        print("⚠️ (PARTICULIER MU4) No data available for tomorrow yet.")
except Exception as error:
    print(f"❌ API Error: {error}")

try:
    response = requests.get(API_PART_CU)
    payload = response.json()
    
    if payload.get("success"):
        target_date = payload.get("date")
        filename = os.path.join(DATA_PART_CU, f"tarifs_{target_date}_cu_particulier.json")
        
        with open(filename, "w") as file:
            json.dump(payload, file)
        print(f"✅ Success: Saved {filename}")
    else:
        print("⚠️ (PARTICULIER CU) No data available for tomorrow yet.")
except Exception as error:
    print(f"❌ API Error: {error}")

try:
    response = requests.get(API_PART_MUDT)
    payload = response.json()
    
    if payload.get("success"):
        target_date = payload.get("date")
        filename = os.path.join(DATA_PART_MUDT, f"tarifs_{target_date}_mudt_particulier.json")
        
        with open(filename, "w") as file:
            json.dump(payload, file)
        print(f"✅ Success: Saved {filename}")
    else:
        print("⚠️ (PARTICULIER MUDT) No data available for tomorrow yet.")
except Exception as error:
    print(f"❌ API Error: {error}")

try:
    response = requests.get(API_PART_LU)
    payload = response.json()
    
    if payload.get("success"):
        target_date = payload.get("date")
        filename = os.path.join(DATA_PART_LU, f"tarifs_{target_date}_lu_particulier.json")
        
        with open(filename, "w") as file:
            json.dump(payload, file)
        print(f"✅ Success: Saved {filename}")
    else:
        print("⚠️ (PARTICULIER LU) No data available for tomorrow yet.")
except Exception as error:
    print(f"❌ API Error: {error}")

try:
    response = requests.get(API_PRO_LU)
    payload = response.json()
    
    if payload.get("success"):
        target_date = payload.get("date")
        filename = os.path.join(DATA_PRO_LU, f"tarifs_{target_date}_lu_pro.json")
        
        with open(filename, "w") as file:
            json.dump(payload, file)
        print(f"✅ Success: Saved {filename}")
    else:
        print("⚠️ (PRO LU) No data available for tomorrow yet.")
except Exception as error:
    print(f"❌ API Error: {error}")

try:
    response = requests.get(API_PART_CU)
    payload = response.json()
    
    if payload.get("success"):
        target_date = payload.get("date")
        filename = os.path.join(DATA_PRO_CU, f"tarifs_{target_date}_cu_pro.json")
        
        with open(filename, "w") as file:
            json.dump(payload, file)
        print(f"✅ Success: Saved {filename}")
    else:
        print("⚠️ (PRO CU) No data available for tomorrow yet.")
except Exception as error:
    print(f"❌ API Error: {error}")

# --- CLEANUP OLD FILES (> 30 days) ---
current_time = time.time()
for filename in os.listdir(DATA_PART_CU4):
    filepath = os.path.join(DATA_PART_CU4, filename)
    
    if os.path.isfile(filepath):
        file_age_days = (current_time - os.path.getmtime(filepath)) / (24 * 3600)
        if file_age_days > RETENTION_DAYS:
            os.remove(filepath)
            print(f"🗑️ Deleted old file (>{RETENTION_DAYS} days): {filename}")

current_time = time.time()
for filename in os.listdir(DATA_PART_MU4):
    filepath = os.path.join(DATA_PART_MU4, filename)
    
    if os.path.isfile(filepath):
        file_age_days = (current_time - os.path.getmtime(filepath)) / (24 * 3600)
        if file_age_days > RETENTION_DAYS:
            os.remove(filepath)
            print(f"🗑️ Deleted old file (>{RETENTION_DAYS} days): {filename}")

current_time = time.time()
for filename in os.listdir(DATA_PART_MUDT):
    filepath = os.path.join(DATA_PART_MUDT, filename)
    
    if os.path.isfile(filepath):
        file_age_days = (current_time - os.path.getmtime(filepath)) / (24 * 3600)
        if file_age_days > RETENTION_DAYS:
            os.remove(filepath)
            print(f"🗑️ Deleted old file (>{RETENTION_DAYS} days): {filename}")

current_time = time.time()
for filename in os.listdir(DATA_PART_CU):
    filepath = os.path.join(DATA_PART_CU, filename)
    
    if os.path.isfile(filepath):
        file_age_days = (current_time - os.path.getmtime(filepath)) / (24 * 3600)
        if file_age_days > RETENTION_DAYS:
            os.remove(filepath)
            print(f"🗑️ Deleted old file (>{RETENTION_DAYS} days): {filename}")

current_time = time.time()
for filename in os.listdir(DATA_PART_LU):
    filepath = os.path.join(DATA_PART_LU, filename)
    
    if os.path.isfile(filepath):
        file_age_days = (current_time - os.path.getmtime(filepath)) / (24 * 3600)
        if file_age_days > RETENTION_DAYS:
            os.remove(filepath)
            print(f"🗑️ Deleted old file (>{RETENTION_DAYS} days): {filename}")

current_time = time.time()
for filename in os.listdir(DATA_PRO_CU):
    filepath = os.path.join(DATA_PRO_CU, filename)
    
    if os.path.isfile(filepath):
        file_age_days = (current_time - os.path.getmtime(filepath)) / (24 * 3600)
        if file_age_days > RETENTION_DAYS:
            os.remove(filepath)
            print(f"🗑️ Deleted old file (>{RETENTION_DAYS} days): {filename}")

current_time = time.time()
for filename in os.listdir(DATA_PRO_LU):
    filepath = os.path.join(DATA_PRO_LU, filename)
    
    if os.path.isfile(filepath):
        file_age_days = (current_time - os.path.getmtime(filepath)) / (24 * 3600)
        if file_age_days > RETENTION_DAYS:
            os.remove(filepath)
            print(f"🗑️ Deleted old file (>{RETENTION_DAYS} days): {filename}")
