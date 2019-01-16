#!/usr/bin/env python    
# -*- coding:utf-8 -*-
import paramiko
import time
         
print('''
###################################

Linux ssh 远程多台机器并执行命令

	Bre--v1.0
				 
By: Lance Blog: www.gklzh.xyz
###################################
''')
#初始化保存主机ip，用户名，密码的列表
hostname = []
username = []
password = []
fault_list = []
def init_user_info():        #初始化主机ip，用户名，密码
	with open("execute_log.txt",'a') as f1:
		f1.write("\n###################################\n")
		f1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		f1.write("\n正在初始化主机信息...\n")
		with open('user_info.txt') as f:
			data = f.readlines()
			for line in data:
				(hname,uname,pw) = line.strip('\n').split(',')
				hostname.append(hname)
				username.append(uname)
				password.append(pw)
		f1.write("初始化完成.\n")	
def ssh_command(hname,uname,pw,command):

	paramiko.util.log_to_file('paramiko.log')    #远程连接日志
	s=paramiko.SSHClient()    
	#s.load_system_host_keys()    
	s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	with open("execute_log.txt",'a') as f:    
	
		f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		
		try:
			s.connect(hostname = hname,username=uname, password=pw)    #使用ip，用户名，密码登录
			print("\n[%s]连接成功!" % hname)
			f.write("\n[%s]连接成功!" % hname)

			stdin,stdout,stderr=s.exec_command(command)    #执行输入的linux命令
		
			print("[%s]的执行结果:"% hname)
			f.write("[%s]执行结果:\n"% (command))
		
			for line in stdout:
				print(line.strip('\n'))
				f.write(line.strip('\n'))
				f.write('\n')
				
		except UnicodeDecodeError:
			print('对不起，此文件名包含不可读取的文件编码！')
			f.write('对不起，此文件名包含不可读取的文件编码！')
			
		except paramiko.ssh_exception.NoValidConnectionsError:
			print("[%s] 远程ssh连接失败！" %hname)
			fault_list.append(hname)
			f.write("\n[%s] 远程ssh连接失败！" %hname)
			
		s.close()
		f.write('\n')
		
def loop_ssh_command(command):  #在多台服务器上批量执行命令
	for i in range(len(hostname)):
		ssh_command(hostname[i],username[i],password[i],command)
		
def execute():
	print("正在初始化主机[IP，用户名，密码]...\n")
	
	init_user_info()
	
	print("初始化成功！\n")
	
	while True:    #循环接收输入
		command = input("请输入需要执行的Linux命令(q/Q:退出)：")
		if command == 'q' or command == 'Q':
			print("bye~")
			break
		loop_ssh_command(command)
		
		with open("execute_log.txt",'a') as f:
			print("\n连接失败主机列表：",fault_list)
			f.write("\n-*-连接失败主机列表-*-：%s\n" % fault_list)
			
if __name__ == "__main__": 
	execute()
			
