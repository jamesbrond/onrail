
def main():
  import sys
  from fare import Fare
  import traceback
  try:
    fare = Fare()
    sys.exit(0)
  except Exception as e:
    print("ERROR: " + str(e), file=sys.stderr)
    # traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
  main()
