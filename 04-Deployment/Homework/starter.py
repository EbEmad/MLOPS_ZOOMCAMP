import pickle
import pandas as pd
import numpy as np
import os
import sys


CATEGORICAL = ['PULocationID', 'DOLocationID']


def read_data(filename: str, year: int, month: int) -> pd.DataFrame:
    try:
        df = pd.read_parquet(filename, engine='pyarrow')

        df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
        df['duration'] = df.duration.dt.total_seconds() / 60

        df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
        df[CATEGORICAL] = df[CATEGORICAL].fillna(-1).astype('int').astype('str')
        df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

        print(f"✅ Data loaded. Shape: {df.shape}")
        return df

    except Exception as e:
        print(f"❌ Error reading or processing data: {e}")
        raise


def apply_model(df: pd.DataFrame, model_path: str) -> pd.DataFrame:
    try:
        with open(model_path, 'rb') as f_in:
            dv, model = pickle.load(f_in)

        dicts = df[CATEGORICAL].to_dict(orient='records')
        X_val = dv.transform(dicts)
        y_pred = model.predict(X_val)

        if np.any(~np.isfinite(y_pred)):
            raise ValueError("Predictions contain NaN or infinite values.")

        df_result = pd.DataFrame({
            'ride_id': df['ride_id'],
            'predicted_duration': y_pred
        })

        print("✅ Prediction completed.")
        return df_result

    except FileNotFoundError:
        print(f"❌ Model file '{model_path}' not found.")
        raise
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        raise


def save_results(df_result: pd.DataFrame, output_file: str):
    try:
        df_result.to_parquet(
            output_file,
            engine='pyarrow',
            compression=None,
            index=False
        )
        size_bytes = os.path.getsize(output_file)
        size_mb = size_bytes / (1024 * 1024)
        print(f"✅ File saved: {output_file} ({size_mb:.2f} MB)")

    except Exception as e:
        print(f"❌ Failed to save output file: {e}")
        raise


def run():
    try:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
    except (IndexError, ValueError):
        print("❌ Usage: python starter.py <year> <month>")
        sys.exit(1)

    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output/{year:04d}-{month:02d}.parquet'
    model_path = 'model.bin'

    df = read_data(input_file, year, month)
    df_result = apply_model(df, model_path)
    save_results(df_result, output_file)

    print(f"📊 Mean predicted duration: {df_result['predicted_duration'].mean():.2f} minutes")


if __name__ == "__main__":
    run()