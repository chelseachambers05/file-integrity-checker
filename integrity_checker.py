import hashlib
import os
import json

# change these if you want to monitor a different folder or use a different baseline file name
BASELINE_FILE = "baseline.json"
MONITOR_DIR = "monitored_folder"

def hash_file(filepath):
    # creates a new SHA-256 hashing object
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        # read the file in chunks to avoid memory issues with large files
        while chunk := f.read(4096):
            sha256.update(chunk) # feeds each chunk into the hashing algorithm
    return sha256.hexdigest() # returns the final hash value as a hexadecimal string

def build_baseline():
    baseline = {}

    # goes through every subfolder and file in the monitored directory
    for root, dirs, files in os.walk(MONITOR_DIR):
        for filename in files:
            # builds the full file path
            filepath = os.path.join(root, filename)
            baseline[filepath] = hash_file(filepath)

    # saves the dictionary to baseline.json so we can compare against it later
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

    print(f"Baseline created with {len(baseline)} file(s).")

def check_integrity():
    # stops the program if no baseline exists yet
    if not os.path.exists(BASELINE_FILE):
        print("No baseline found. Run with --baseline first.")
        return
    
    # loads the previously saved baseline hashes from the JSON file
    with open(BASELINE_FILE, "r") as f:
        baseline = json.load(f)

    current = {} # store the current state of files

    # scans the monitored folder again and hashes everything fresh
    for root, dirs, files in os.walk(MONITOR_DIR):
        for filename in files:
            filepath = os.path.join(root, filename)
            current[filepath] = hash_file(filepath)

    added = [f for f in current if f not in baseline] # files that are in the current state but not in the baseline (new files)
    deleted = [f for f in baseline if f not in current] # files that are in the baseline but not in the current state (deleted files)
    modified = [f for f in current if f in baseline and current[f] != baseline[f]] # files that are in both states but have different hashes (modified files)

    if not added and not deleted and not modified:
        print("All files intact. No changes detected.")
    else:
        if added:
            print("\n[ADDED]")
            for f in added:
                print(f"  + {f}")
        if deleted:
            print("\n[DELETED]")
            for f in deleted:
                print(f"  - {f}")
        if modified:
            print("\n[MODIFIED]")
            for f in modified:
                print(f"  ! {f}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python integrity_checker.py --baseline OR --check")
    elif sys.argv[1] == "--baseline":
        build_baseline()
    elif sys.argv[1] == "--check":
        check_integrity()
    else:
        print("Unknown argument. Use --baseline or --check")