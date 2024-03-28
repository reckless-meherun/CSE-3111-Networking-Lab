import os
import multiprocessing
import shutil
import sys


def run_script(filename, index):
  """Runs a copy of the Python script with a letter suffix."""
  name,extension = filename.split('.')
  suffix = chr(ord('A') + index)
  copy_name = f"{name}{suffix}.py"
  shutil.copy2(filename, copy_name)  # Use shutil.copy2 instead of os.cp
  
#   os.system(f"python {copy_name}")


def main():
  """Gets user input, creates copies, and runs them in parallel."""
  if len(sys.argv) != 3:
    print("Usage: python script.py <number_of_copies> <python_file>")
    return

  num_copies = int(sys.argv[1])
  python_file = sys.argv[2]

  # Use a pool of worker processes for parallel execution
  pool = multiprocessing.Pool(processes=num_copies)
  pool.starmap(run_script, [(python_file, i) for i in range(num_copies)])
  pool.close()
  pool.join()

  print(f'{num_copies} file created')
#   print(f"All {num_copies} copies of {python_file} are running in parallel.")


if __name__ == "__main__":
  main()
