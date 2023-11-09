import os
import pandas as pd
import re
import warnings

def find_latest_nonempty_log_file(directory):
    # Finds the latest non-empty log file in the given directory.
    log_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.startswith('gpt_train_')]
    sorted_log_files = sorted(log_files, key=os.path.getctime, reverse=True)
    
    for log_file in sorted_log_files:
        if os.stat(log_file).st_size > 0:  # Check if the file is not empty
            return log_file
    return None  # Return None if all files 

def find_latest_log_file(directory):
    # Finds the latest log file in the given directory.
    log_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.startswith('gpt_train_')]
    return max(log_files, key=os.path.getctime)

def extract_relevant_data(file_path):
    # Extracts relevant data from the log file.
    data = []
    pattern = re.compile(r'^\[(\d+) \| (\d+\.\d+)\] loss=(\d+\.\d+) avg=(\d+\.\d+)$')
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.match(line.strip())
            if match:
                iteration, time, loss, avg_loss = match.groups()
                data.append([int(iteration), float(time), float(loss), float(avg_loss)])
    return pd.DataFrame(data, columns=['iteration', 'time', 'loss', 'avg_loss'])

def summarize_data(data, top_n=10):
    # Summarizes the data into key statistics and top/bottom N loss values with iteration numbers.
    
    # If the data is empty, return an empty summary.
    if data.empty:
        return {
            'total_iterations': 0,
            'average_loss': None,
            'median_loss': None,
            'min_loss': None,
            'max_loss': None,
            'std_dev_loss': None,
            'initial_losses': [],
            'top_n_losses': [],
            'bottom_n_losses': [],
            'first_iteration': None,
            'last_iteration': None
        }

    # Ensure the 'loss' and 'avg_loss' columns are of type float.
    data['loss'] = pd.to_numeric(data['loss'], errors='coerce')
    data['avg_loss'] = pd.to_numeric(data['avg_loss'], errors='coerce')
    
    # Drop rows where 'loss' or 'avg_loss' could not be converted to float.
    data = data.dropna(subset=['loss', 'avg_loss'])
    
    # Sort the data by iteration number.
    data = data.sort_values(by='iteration')
    
    # Calculate summary statistics.
    summary = {
        'total_iterations': len(data),
        'average_loss': data['avg_loss'].mean(),
        'median_loss': data['avg_loss'].median(),
        'min_loss': data['avg_loss'].min(),
        'max_loss': data['avg_loss'].max(),
        'std_dev_loss': data['avg_loss'].std(),
        'initial_losses': data[['iteration', 'loss', 'avg_loss']].head(top_n).values.tolist(),
        'top_n_losses': data.nlargest(top_n, 'loss')[['iteration', 'loss', 'avg_loss']].values.tolist(),
        'bottom_n_losses': data.nsmallest(top_n, 'loss')[['iteration', 'loss', 'avg_loss']].values.tolist(),
        'first_iteration': data.iloc[0][['iteration', 'loss', 'avg_loss']].values.tolist(),
        'last_iteration': data.iloc[-1][['iteration', 'loss', 'avg_loss']].values.tolist()
    }
    
    return summary

def main():
    log_dir = "./logs"  # Update as needed
    all_log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.startswith('gpt_train_')]
    all_log_files.sort(key=os.path.getctime, reverse=True)  # Sort files by creation time, newest first
    
    # Start with the latest file and check if it's non-empty
    for log_file in all_log_files:
        if os.stat(log_file).st_size > 0:  # Check if the file is not empty
            data = extract_relevant_data(log_file)
            if not data.empty:  # Make sure data is extracted
                break
            else:
                print(f"File {log_file} is non-empty but no data was extracted. Possibly a format issue.")
                continue
        else:
            print(f"File {log_file} is empty. Skipping to the next file.")
    
    # If all files are empty or no data could be extracted
    if data.empty:
        print("No log data could be extracted from available files.")
        return
    
    # If the file used is not the latest one, warn the user
    if log_file != all_log_files[0]:
        print(f"WARNING: Using data from {log_file} as the latest file is empty or has no extractable data.")
    
    summary = summarize_data(data, top_n=10)  # You can change 'top_n' as needed
    for key, value in summary.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()