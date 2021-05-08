#!python3
import requests
import sys
from PIL import Image


def main():
	print("Running the piface")
	print('Argument List:', str(sys.argv))

	ip = "192.168.1.76:8085"
	if len(sys.argv) > 1:
		ip = sys.argv[1]

	print('Looking at host', ip)

	response = requests.get("http://" + ip + "/data.json")

	data = response.json()

	for k in data:
		print(k)

	image = Image.open('image.png')
	image.show()

	print("Finished piface")


if __name__ == '__main__':
	main()