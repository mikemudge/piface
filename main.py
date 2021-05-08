#!python3
import requests
import subprocess
import sys
import os
from time import sleep


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

		print("CPU Load =", cpuPercent)
		image = os.path.join(os.getcwd(), 'image2.png')
		if cpuPercent < 20:
			image = os.path.join(os.getcwd(), 'image1.png')
		if cpuPercent > 50:
			image = os.path.join(os.getcwd(), 'image3.png')
		if cpuPercent > 75:
			image = os.path.join(os.getcwd(), 'image4.png')

		newproc = None
		if pi:
			newproc = subprocess.Popen(('feh --hide-pointer -Z -F -x -q -B white ' + image).split(' '))
		else:
			# Laptop development
			print("Displaying", image)

		# Give it a little time to display before removing the old one.
		sleep(0.5)
		if proc:
			proc.terminate()
		proc = newproc

		sleep(1)

	# Final cleanup.
	if proc:
		proc.terminate()

	print("CPU usage over time", cpuHistory)

	print("Finished piface")


if __name__ == '__main__':
	main()