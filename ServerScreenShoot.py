from ssm import ScreenMirrorServer

# ssm_server = ScreenMirrorServer(['<client-ip>', port=7890])
ssm_server = ScreenMirrorServer()  # default: all ip & 7890 port
while True:
	try:
		ssm_server.start()
	except:
		print("Died")

