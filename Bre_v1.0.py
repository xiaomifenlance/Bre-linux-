#!/usr/bin/env python    
import paramiko    
         

#初始化保存主机ip，用户名，密码的列表
print('''
##########################################

Linux ssh 远程多台机器并执行命令

	Bre--v1.0
				 by: Lance
##########################################
''')
hostname = []
username = []
password = []
 
def init_user_info():        #初始化主机ip，用户名，密码
	with open('user_info.txt') as f:
		data = f.readlines()
		for line in data:
			(hname,uname,pw) = line.strip('\n').split(',')
			hostname.append(hname)
			username.append(uname)
			password.append(pw)
			
def ssh_command(hname,uname,pw,command):
	paramiko.util.log_to_file('paramiko.log')    #远程连接日志
	s=paramiko.SSHClient()    
	#s.load_system_host_keys()    
	s.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
	
	s.connect(hostname = hname,username=uname, password=pw)    #使用ip，用户名，密码登录
	
	stdin,stdout,stderr=s.exec_command(command)    #执行输入的linux命令
	print("%s的执行结果:\n"% hname)
	for line in stdout:
		print(line)
	s.close()
	
			
if __name__ == "__main__": 
	init_user_info()
	#print(hostname)  
	#print(username)
	#print(password)
	while True:
		command = input("请输入需要执行的Linux命令(q/Q:退出)：")
		#print(len(hostname))
		if command == 'q' or command == 'Q':
			print("Bye~")
			break
		for i in range(len(hostname)):
			ssh_command(hostname[i],username[i],password[i],command)
