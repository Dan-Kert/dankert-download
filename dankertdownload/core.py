import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: dankert-download <URL>")
        sys.exit(1)
    url = sys.argv[1]
    print(f"Скачиваю {url}…")