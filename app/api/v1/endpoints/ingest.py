from fastapi import APIRouter, UploadFile, File, HTTPException
import logging
import pandas as pd
import csv
from io import StringIO
from app.services.data_processing import process_df
from app.core.logging import setup_logging
from fastapi import Depends
from fastapi import Request
from typing import Dict
import os

router = APIRouter()

setup_logging()

@router.post("/ingest")
async def ingest_tweets(
    request: Request,  # Para acceder al estado de la aplicación
    file: UploadFile = File(...)
) -> Dict[str, str]:
    try:
        logging.info("Starting tweet ingestion.")
        
        # Leer el contenido del archivo
        contents = file.file.read()
        buffer = StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(buffer)
        
        # Contar filas y preparar el archivo de salida
        row_count = 0
        output_filename = '/data/input_data.csv'
        if not os.path.exists('/data'):
            output_filename = 'input_data.csv'


        with open(output_filename, mode='w', newline='') as file:
            fieldnames = csv_reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in csv_reader:
                row_count += 1
                writer.writerow(row)
        
        buffer.close()
        
        # Cargar el CSV en un DataFrame y procesarlo
        datos = pd.read_csv(output_filename)
        datos = process_df(datos)
        
        # Almacenar el DataFrame en el estado de la aplicación
        request.app.state.datos = datos
        
        logging.info(f"{row_count} tweets successfully ingested and processed.")
        
        return {"message": f"{row_count} tweets successfully loaded."}
    
    except Exception as e:
        logging.error(f"Error during tweet ingestion: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")