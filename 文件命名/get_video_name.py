import os
target_dir = os.getcwd()
f = open('old_files.txt','r')
data = f.readlines()
file_names = data
f.close()
print file_names
types = file_names[1].strip()
types = types.split('.')[-1]
target_dir = os.getcwd()
f = open('old_files.txt','w')
for i in file_names:
	i.strip()
	write_line = 'file '.encode('gbk') + "'".encode('gbk') + target_dir +'\\'+ i[:-1].decode('gbk').encode('gbk') + "'"+'\n'
        if i.split('.')[-1].lower()[0:3] == 'mp4' or i.split('.')[-1].lower()[0:3] == 'avi' or i.split('.')[-1].lower()[0:3] == 'ts' or i.split('.')[-1].lower()[0:3] == 'wmv':
	    f.write(write_line)
f.close()