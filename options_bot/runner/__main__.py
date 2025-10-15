"""
Main entry point for running scans.
"""
import sys
from .scan import run_scan

if __name__ == "__main__":
    # Allow command line argument for scan name
    scan_name = None
    if len(sys.argv) > 1:
        scan_name = " ".join(sys.argv[1:])
    
    run_scan(scan_name=scan_name)

