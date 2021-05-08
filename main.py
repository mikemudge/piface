#!python3
import requests
import subprocess
import sys
from time import sleep
from PIL import Image


def main():
	print("Running the piface")
	print('Argument List:', str(sys.argv))

	ip = "192.168.1.76:8085"
	if len(sys.argv) > 1:
		ip = sys.argv[1]

	print("Running on", sys.platform)
	pi = True
	if sys.platform == 'darwin':
		pi = False

	print('Looking at host', ip)

	cpuHistory = []
	proc = None
	for i in range(10):
		response = requests.get("http://" + ip + "/data.json")

		data = response.json()

		print('Keys', data.keys())
		pc = data.get('Children')[0]

		print("Showing data for PC named", pc.get('Text'))
		
		for component in pc.get('Children'):
			name = component.get('Text')
			for section in component.get('Children'):
				if section.get('Text') == 'Load':
					for v in section.get("Children"):
						if v.get('Text') == 'CPU Total':
							# This is a primary metric
							print("CPU Load =", v.get('Value'))
							cpuPercent = float(v.get('Value')[:-1].strip())
							print("float()", cpuPercent)
							cpuHistory.append(cpuPercent)

						print(component.get('Text'), "> Load >", v.get('Text'), v.get('Value'))

		# Pick a face and display it.
		if pi:
			if proc:
				proc.terminate()
			proc = subprocess.Popen('feh --hide-pointer -Z -F -x -q -B white ~/projects/piface/image.png'.split(' '))
		else:
			# Laptop development
			print("Displaying image.png")

		sleep(1)


	print("CPU usage over time", cpuHistory)

	print("Finished piface")


if __name__ == '__main__':
	main()