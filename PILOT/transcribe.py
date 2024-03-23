import os
from google.cloud import speech, storage
import pandas as pd
import argparse


# Función para transcribir un archivo de audio local y obtener los desplazamientos de tiempo de las palabras
def transcribe_local_audio_with_word_time_offsets(audio_path: str) -> speech.RecognizeResponse:
    # Crear un cliente para el servicio de Google Cloud Speech-to-Text
    client = speech.SpeechClient()

    # Configurar el objeto de audio de reconocimiento
    audio = speech.RecognitionAudio(uri=audio_path)
    
    # Configurar los parámetros de reconocimiento, incluyendo el idioma y la habilitación de los desplazamientos de tiempo de las palabras
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US",
        enable_word_time_offsets=True,
        audio_channel_count=1,  # Especificar el número de canales de audio (en este caso, 2 para estéreo)
)
    

    # Iniciar la operación de reconocimiento de larga duración
    operation = client.long_running_recognize(config=config, audio=audio)

    # Esperar a que la operación se complete y obtener el resultado
    print("Esperando a que la operación se complete...")
    result = operation.result(timeout=90)

    return result

# Función principal
def main(bucket_name, prefix, output_folder):
    
    # Read data from bucket (this assumes that aduios are already converted to wav files)
    storage_client = storage.Client()   
    blobs = storage_client.list_blobs(bucket_name, prefix = prefix)

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # b = [blob.name for blob in blobs if blob.name.endswith('.wav')]
    # Iterar sobre cada archivo .wav en la carpeta
    for blob in blobs:
        
        file_name = blob.name
        
        if file_name.endswith('.csv'):
            print(output_folder)
            print(blob.name[len(prefix):])
            p = os.path.join(output_folder, blob.name[len(prefix)+1:])
            print(p)
            blob.download_to_filename(os.path.join(output_folder, blob.name[len(prefix)+1:]))
        
        elif file_name.endswith(".wav"):
            # Obtener la ruta completa del archivo de audio
            # audio_path = os.path.join(folder_path, file_name)
            
            audio_path = os.path.join('gs://semantic-data',file_name)
            
            # Realizar la transcripción de audio y obtener los resultados
            result = transcribe_local_audio_with_word_time_offsets(audio_path)

            # Convertir el resultado a un DataFrame de pandas
            rows = []
            for res in result.results:
                alternative = res.alternatives[0]
                for word_info in alternative.words:
                    word = word_info.word
                    start_time = word_info.start_time.total_seconds()
                    end_time = word_info.end_time.total_seconds()
                    confidence = alternative.confidence
                    rows.append([word, start_time, end_time, confidence])

            df = pd.DataFrame(rows, columns=["Word", "Start_time", "End_time", "Confidence"])

            # Escribir el DataFrame en un archivo de Excel
            output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.xlsx")
            df.to_excel(output_path, index=False)

            print(f"Transcripción para {file_name} guardada en {output_path}")
        
            

# Ejecutar la función principal si este script es el archivo principal que se está ejecutando
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Execute Semantic Foraging Code.')
    parser.add_argument('--bucket_name', type=str,  help='Name of google cloud bucket where data is stored')
    parser.add_argument('--prefix', type=str,  help='directory name in which the audio is stored in the bucket')
    parser.add_argument('--output_folder', type=str,  help='Path for output transcriptions to be stored')
    args = parser.parse_args()
    main(args.bucket_name, args.prefix, args.output_folder)
    