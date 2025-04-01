import os
import tarfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from flask_socketio import emit

def extract_member(file, batch, path):
    with tarfile.open(file, 'r:gz') as tar:
        for member in batch:
            tar.extract(member, path)

def extract_mbz(file, output_dir):
    with tarfile.open(file, 'r:gz') as tar:
        members = tar.getmembers()

    total_files = len(members)
    n_workers = os.cpu_count()
    chunksize = max(1, round(total_files / n_workers))

    extracted_files = 0

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        
        futures = []
        for i in range(0, total_files, chunksize):
            batch = members[i:i + chunksize]
            future = executor.submit(extract_member, file, batch, output_dir)
            futures.append(future)

        # Überwachen der abgeschlossenen Futures für die Fortschrittsanzeige
        for future in as_completed(futures):
            extracted_files += chunksize
            progress = (extracted_files / total_files) * 100
            print(f"Fortschritt: {extracted_files}/{total_files} Dateien extrahiert ({progress:.2f}%)", end='\r')
            emit('extraction_progress', {'progress': progress, 'finished': extracted_files == total_files})
