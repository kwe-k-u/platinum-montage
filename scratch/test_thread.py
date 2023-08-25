from threading import Thread


def say(thread_name):
	for i in range(30):
		print(thread_name,i)

threads = []
for name in ["KWAME","Joseph","Paa","Amegoblish"]:
	thread = Thread(target=say,args=[name])
	threads.append(thread)
	thread.start()

for thread in threads:
	thread.join()