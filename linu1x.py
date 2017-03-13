#encoding:UTF-8
import pexpect
from pexpect import popen_spawn
import getpass,os

def ssh_command(user,host,password,cmd):
	ssh_newkey = 'Are you sure you want to continue connecting'
	child = pexpect.popen_spawn.PopenSpawn('ssh -l %s %s %s'%(user,host,cmd))
	i = child.expect([pexpect.TIMEOUT,ssh_newkey,'password:'])
	if i == 0:
		print ('error!')
	if i == 1:
		child.sendline('yes')
		child.expect('password:')
		i = child.expect([pexpect.TIMEOUT,ssh_newkey,'password:'])
		if i==0:
			print ('error')
			return None
	child.sendline(password)
	return child
def main():
	host = input('hostname:')
	user = input('username:')
	password = getpass.getpass()
	command = input("command:")
	child = ssh_command(user,host,password,command)
	child.expect(pexpect.EOF)
	print (child.before)	

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(e)	
		