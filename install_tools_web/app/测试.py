import os

base = "D:\视频\\"
file = "Python29期2020-10月结课"
path = os.path.join(base,file)
s = "-"
def print_file(base,file,s):

    s += "-"
    path = os.path.join(base,file)
    if "负载均衡" in file:
        print(s,path)
    if os.path.isdir(path):
        file_ls = os.listdir(path)
        if file_ls:
            for f in file_ls:
                print_file(path,f,s)


print_file(base,file,s)