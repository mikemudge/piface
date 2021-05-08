#!python3
import requests

import sys

def main():
	print("Running the piface")
	print('Argument List:', str(sys.argv))

	ip = "192.168.1.76:8085"
	if 1 in sys.argv:
		ip = sys.argv[1]

	response = requests.get("http://" + ip + "/data.json")

	print(response.json())
	print("Finished piface")


if __name__ == '__main__':
	main()