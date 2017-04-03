
import os


workdir = os.getcwd()
print(workdir)

f = open(os.path.join(workdir,'old_file_names.txt'),'r')


OldNames = f.readlines()

f.close()

j = 1

#print OldNames

print('begin  to rename ...\n')

f = open(os.path.join(workdir,'new_bat.bat'),'w')

for i in OldNames:

    if i == 'rename.bat\n' or i == 'old_file_names.txt\n' or i == 'new_bat.bat\n':
        continue

    i.strip()

    OldDir = i

    if j < 10:
        j = '0'+str(j)
    else:
        j = str(j)

    NewDir = j + '_' + i

    print(OldDir + '>' + NewDir)

    w = 'rename' + ' ' +'\"'+OldDir[:-1]+ '\"' + ' ' + '\"'+  NewDir[:-1] + '\"' + '\n'

    f.write(w)

    #os.rename(OldDir ,NewDir)

    j = int(j)

    j += 1

os.remove(os.path.join(workdir,'old_file_names.txt'))

f.close()



