#!python3
import requests

def main():
	print("Running the piface")
	# TODO use an arg.
	ip = "192.168.1.76:8085"

	response = requests.get("http://" + ip + "/data.json")

	print(response.json())
	print("Finished piface")


if __name__ == '__main__':
	main()