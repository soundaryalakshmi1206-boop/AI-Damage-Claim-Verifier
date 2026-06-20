import pandas as pd
import os


class CSVWriter:

    def __init__(self):
        self.rows = []

    def add(self, row):
        self.rows.append(row)

    def save(self, output_path):

        df = pd.DataFrame(self.rows)

        # If output.csv already exists, append instead of overwrite
        if os.path.exists(output_path):

            old_df = pd.read_csv(output_path)

            df = pd.concat(
                [old_df, df],
                ignore_index=True
            )

        df.to_csv(
            output_path,
            index=False
        )

        print("Output Saved :", output_path)