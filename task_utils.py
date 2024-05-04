from datetime import datetime, timedelta
import os
import pandas as pd
import discord

def deadline_format(deadline): 
    try: 
        valid_date = datetime.strptime(deadline, "%d-%m-%Y")
        if valid_date >= datetime.now():
            return True
        else: 
            return False
    except ValueError: 
        return False

def time_format(time, deadline): 
    try: 
        timeInputed = f"{deadline} {time}"
        dateAndTime = datetime.strptime(timeInputed, "%d-%m-%Y %H:%M")
        
        if dateAndTime >= datetime.now(): 
            return True
        else: 
            return False
    except ValueError: 
        return False

def saveTask(task_name, deadline, time, author_id): 
    # Membuat DataFrame baru dari new_data
    data = pd.DataFrame({'task_name': [task_name], 'deadline': [deadline], 'time': [time]})
    data_folder = "csv_data"
    
    if not os.path.exists(data_folder): 
        os.makedirs(data_folder)
        
    # Membuat nama folder
    folder_path = os.path.join(data_folder, f'{author_id}.csv')
    
    # Menyimpan DataFrame ke file CSV
    if not os.path.exists(folder_path):
        data.to_csv(folder_path, index=False)
    else: 
        # Baca file CSV ke DataFrame
        existing_data = pd.read_csv(folder_path)
        
        # Gabungkan DataFrame baru dengan data yang ada
        new_data = pd.concat([data, existing_data], ignore_index=True)
        
        # Tulis DataFrame kembali ke file CSV
        new_data.to_csv(folder_path, index=False)
    
    print(data)
    return data

def showTask(author): 
    # Jika file csv ada
    if os.path.exists(f"csv_data/{author}.csv"):
        allTask = pd.read_csv(f"csv_data/{author}.csv")
        return allTask
    else: 
        print("Data kosong")
        return None
    
def count_deadline(date, time): 
    deadline = f"{date} {time}"
    deadline_date = datetime.strptime(deadline, '%d-%m-%Y %H:%M')
    now = datetime.now()
    
    # hitung perbedaan waktu
    diff_day = deadline_date - now
    
    # cari perbedaan hari dan jam
    day = diff_day.days
    hour = diff_day.seconds // 3600
    
    # Kembalikan hari dan jam
    return day, hour

def is_folder_contains_csv(folder_path):
    # Mendapatkan daftar file dalam folder
    files_in_folder = os.listdir(folder_path)
    
    # Memeriksa apakah setidaknya satu file berakhiran dengan ".csv"
    return any(file.endswith('.csv') for file in files_in_folder)

def merge_csv(): 
    csv_array = []
    folder_path = 'csv_data'
    combined_df = pd.DataFrame()
    
    if is_folder_contains_csv(folder_path): 
        for file_name in os.listdir(folder_path): 
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder_path, file_name)
      
                # Baca file CSV
                df = pd.read_csv(file_path)
                
                # Ambil id user dari nama file dan simpan ke dalam kolom "author"
                author = file_name.split('.')[0]
                df['author'] =author
                
                # Tambahkan dataframe ke dalam list
                csv_array.append(df)
                
        # Gabungkan semua dataframe menjadi satu
        combined_df = pd.concat(csv_array, ignore_index=True)
    else: 
        print('Data kosong')
        
    return combined_df

def neared_deadline(): 
    df = merge_csv()
    date_format = '%d-%m-%Y'
    now = datetime.now()
    
    # Penyimpan deadline kurang dari 4 hari
    neared_task = []
    
    for index, row in df.iterrows(): 
        deadline_date = datetime.strptime(row['deadline'], date_format)
        days_to_deadline = (deadline_date - now).days
        if days_to_deadline <= 4 and (now.hour == 9 and now.minute == 0): 
            neared_task.append(row)
            
    return days_to_deadline, neared_task
        
