import pandas as pd
import random

# File names and settings
input_file = 'card_transaction.v1.csv'       # Replace with your actual large CSV file
output_file = 'randomized_sample.csv'
target_total = 1000000              # Desired total number of rows
chunksize = 10 ** 6                   # Process 1,000,000 rows at a time

# --- First Pass: Collect Fraud Rows & Count Non-Fraud Rows ---
fraud_rows_list = []
fraud_count = 0

for chunk in pd.read_csv(input_file, chunksize=chunksize):
    # Ensure "Is Fraud?" is treated as a string for reliable comparison
    chunk["Is Fraud?"] = chunk["Is Fraud?"].astype(str)
    
    # Extract fraud rows (case-insensitive comparison)
    chunk_fraud = chunk[chunk["Is Fraud?"].str.strip().str.lower() == "yes"]
    fraud_rows_list.append(chunk_fraud)
    fraud_count += len(chunk_fraud)

# Combine all fraud rows into one DataFrame
if fraud_rows_list:
    fraud_df = pd.concat(fraud_rows_list, ignore_index=True)
else:
    fraud_df = pd.DataFrame()

# Calculate how many non-fraud rows are needed
nonfraud_needed = target_total - fraud_count

# --- Second Pass: Reservoir Sampling for Non-Fraud Rows ---
if nonfraud_needed <= 0:
    # If fraud rows already meet or exceed our target, sample from them only.
    print("Fraud rows exceed or equal the target total. Sampling fraud rows only.")
    final_df = fraud_df.sample(n=target_total, random_state=42).reset_index(drop=True)
else:
    reservoir = []    # This will hold the selected non-fraud rows as dictionaries
    nonfraud_seen = 0 # Counter for the total non-fraud rows processed

    for chunk in pd.read_csv(input_file, chunksize=chunksize):
        # Ensure proper string type for "Is Fraud?"
        chunk["Is Fraud?"] = chunk["Is Fraud?"].astype(str)
        # Filter non-fraud rows (case-insensitive comparison)
        chunk_nonfraud = chunk[chunk["Is Fraud?"].str.strip().str.lower() != "yes"]
        
        # Convert filtered rows to a list of dictionaries (preserving original columns)
        records = chunk_nonfraud.to_dict(orient="records")
        
        # Iterate over each non-fraud record
        for record in records:
            nonfraud_seen += 1
            # If the reservoir isn't full yet, simply append the record
            if len(reservoir) < nonfraud_needed:
                reservoir.append(record)
            else:
                # Randomly decide whether to replace an element in the reservoir
                j = random.randint(0, nonfraud_seen - 1)
                if j < nonfraud_needed:
                    reservoir[j] = record

    # Create a DataFrame from the reservoir sample of non-fraud rows
    nonfraud_df = pd.DataFrame(reservoir)
    
    # Combine fraud and non-fraud DataFrames
    combined_df = pd.concat([fraud_df, nonfraud_df], ignore_index=True)
    # Randomize the order of the combined data
    final_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Ensure the final DataFrame has exactly the target number of rows
if len(final_df) > target_total:
    final_df = final_df.sample(n=target_total, random_state=42).reset_index(drop=True)

# Write the final randomized DataFrame to the output CSV file
final_df.to_csv(output_file, index=False)
print(f"Output CSV '{output_file}' generated with {len(final_df)} rows.")
