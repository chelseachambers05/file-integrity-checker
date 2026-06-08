# File Integrity Checker

A Python script that monitors a folder for file changes using SHA-256 hashing.

## What it does

- Creates a baseline of SHA-256 hashes for every file in a monitored folder
- On the next run, compares current hashes against that baseline
- Flags anything that was added, deleted, or modified

## Why it matters

If a file gets tampered with -- whether by malware or anything else -- the hash changes. This script catches that. It is the same idea behind tools like Tripwire that security teams use to monitor critical files in real environments.

## Usage

Create a baseline: python integrity_checker.py --baseline

Check for changes: python integrity_checker.py --check

## Built with

- Python 3
- hashlib -- SHA-256 hashing
- os -- file system traversal
- json -- baseline storage

## Concepts covered

- Cryptographic hashing
- File system monitoring
- Defensive security / incident detection