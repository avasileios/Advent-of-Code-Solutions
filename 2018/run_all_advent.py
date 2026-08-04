import os
import sys
import subprocess
import time
from datetime import datetime

# Base directory = the folder this script lives in.
# Works for ANY year folder (2015/2016/2017/2024), on Linux, Windows or
# macOS, no matter where the repo is cloned on the machine.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YEAR = os.path.basename(BASE_DIR)  # e.g. "2015", "2016", "2017", "2024"

# Results file is written next to the script (inside the year folder)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(BASE_DIR, f"advent_results_{timestamp}.txt")

def run_python_file(filepath, day_name, part_name):
    """Run a Python file and capture its output"""
    try:
        # Run the script with a timeout of 30 seconds.
        # Use the same interpreter that is running this script so it works
        # everywhere: python3 on Linux/macOS, python.exe on Windows, venvs...
        result = subprocess.run(
            [sys.executable, filepath],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=os.path.dirname(filepath)  # Run from the script's directory
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode == 0:
            return {
                'status': 'SUCCESS',
                'output': output if output else '(no output)',
                'error': None
            }
        else:
            return {
                'status': 'ERROR',
                'output': output,
                'error': error
            }
    except subprocess.TimeoutExpired:
        return {
            'status': 'TIMEOUT',
            'output': None,
            'error': 'Script took longer than 300 seconds'
        }
    except Exception as e:
        return {
            'status': 'FAILED',
            'output': None,
            'error': str(e)
        }

def main():
    print("="*80)
    print(f"🎄 Advent of Code {YEAR} - Mass Runner 🎄")
    print("="*80)
    print()

    results = []
    total_success = 0
    total_failed = 0
    total_timeout = 0

    # Open output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write(f"🎄 Advent of Code {YEAR} - Results 🎄\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")

        # Walk through all day directories
        for day_num in range(1, 26):
            day_folder = f"Day-{day_num:02d}-Challenge"
            if day_num == 25:
                day_folder = "Day-25-Challenge-Final"

            day_path = os.path.join(BASE_DIR, day_folder)

            if not os.path.exists(day_path):
                continue

            print(f"\n{'='*80}")
            print(f"📅 Day {day_num}")
            print(f"{'='*80}")

            f.write(f"\n{'='*80}\n")
            f.write(f"📅 Day {day_num}\n")
            f.write(f"{'='*80}\n")

            # Find all Python files in the day folder
            py_files = sorted([file for file in os.listdir(day_path)
                             if file.endswith('.py')])

            for py_file in py_files:
                filepath = os.path.join(day_path, py_file)

                # Determine part name
                if 'p1' in py_file.lower():
                    part_name = "Part 1"
                elif 'p2' in py_file.lower():
                    part_name = "Part 2"
                elif 'final' in py_file.lower():
                    part_name = "Final"
                else:
                    part_name = py_file

                print(f"\n  Running {part_name} ({py_file})...", end=" ")
                f.write(f"\n  {part_name} ({py_file})\n")
                f.write(f"  {'-'*76}\n")

                start_time = time.time()
                result = run_python_file(filepath, f"Day {day_num}", part_name)
                elapsed = time.time() - start_time

                if result['status'] == 'SUCCESS':
                    print(f"✓ ({elapsed:.2f}s)")
                    f.write(f"  Status: ✓ SUCCESS ({elapsed:.2f}s)\n")
                    f.write(f"  Output:\n    {result['output']}\n")
                    total_success += 1
                elif result['status'] == 'TIMEOUT':
                    print(f"⏱ TIMEOUT")
                    f.write(f"  Status: ⏱ TIMEOUT (>30s)\n")
                    f.write(f"  Error: {result['error']}\n")
                    total_timeout += 1
                else:
                    print(f"✗ FAILED")
                    f.write(f"  Status: ✗ FAILED\n")
                    if result['output']:
                        f.write(f"  Output:\n    {result['output']}\n")
                    if result['error']:
                        f.write(f"  Error:\n    {result['error']}\n")
                    total_failed += 1

                results.append({
                    'day': day_num,
                    'part': part_name,
                    'file': py_file,
                    'status': result['status'],
                    'time': elapsed
                })

        # Summary
        total_scripts = total_success + total_failed + total_timeout

        print(f"\n{'='*80}")
        print(f"📊 SUMMARY")
        print(f"{'='*80}")
        print(f"  Total scripts run: {total_scripts}")
        print(f"  ✓ Successful: {total_success}")
        print(f"  ✗ Failed: {total_failed}")
        print(f"  ⏱ Timeout: {total_timeout}")
        print(f"\n  Results saved to: {output_file}")
        print(f"{'='*80}\n")

        f.write(f"\n{'='*80}\n")
        f.write(f"📊 SUMMARY\n")
        f.write(f"{'='*80}\n")
        f.write(f"  Total scripts run: {total_scripts}\n")
        f.write(f"  ✓ Successful: {total_success}\n")
        f.write(f"  ✗ Failed: {total_failed}\n")
        f.write(f"  ⏱ Timeout: {total_timeout}\n")
        f.write(f"{'='*80}\n")

if __name__ == "__main__":
    main()
