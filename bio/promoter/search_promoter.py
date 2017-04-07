# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 00:08:23 2017

@author: Administrator
"""


def extract_promoter(file_path='Hs_EPDnew.dat'):
    promoter_dict = {}
    with open('Hs_EPDnew.dat') as f:
        get = 0
        for line in f:
            if line.startswith("GN"):
                gene_name = line.split('=')[-1].split(';')[0]
                if gene_name:# in gene_list:
                    get = 1
                else:
                    get = 0
            elif get == 1 and line.startswith("SE"):
                promoter_dict[gene_name] = line.split()[-1]
                get = 0
    return(promoter_dict)
promoter_dict = extract_promoter(file_path=r'C:\bat\bio\promoter\Hs_EPDnew.dat')

gene_name = input("Please input your gene symbol:\n").upper()

if gene_name in promoter_dict.keys():
    print("The promoter of {} is:\n".format(gene_name))
    print(promoter_dict[gene_name])
else:
    print("Not found promoter of {}, please check your input\n".format(gene_name))
    all_keys = sorted(list(promoter_dict.keys()))
    for i in all_keys:
        for j in range(len(gene_name), 1,-1):
            try:
                if gene_name[:j] == i[:j]:
                    c = all_keys.index(i)
                    for k in range(5):
                        print(all_keys[c+k])
                        print(promoter_dict[all_keys[c+k]])
                    break
            except:
                pass
    