import time
from install_tools_web.settings import BASE_DIR
import paramiko
import os

def upfile_to_linux(hostdic, filename,linuxpath):
    host = hostdic.get("host")
    port = hostdic.get("port")
    user = hostdic.get("username")
    password = hostdic.get("password")
    msg = ""

    # 本第文件上传到linux
    try:
        t = paramiko.Transport((host, int(port)))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
    except Exception as e:
        msg =  "连接主机失败"
        return msg
    try:
        dirpath = os.path.join(BASE_DIR,"upfile")
        filepath = os.path.join(dirpath,filename)
        linuxpath = os.path.join(linuxpath,filename).replace("\\","/")
        sftp.put(filepath, linuxpath)
        msg = "上传成功"
        t.close()
    except Exception as e:
        msg = e
        print("问题少年的问题是：", e)


    return msg

def paramiko_uploadfile_to_linux(hostdic, shellname_ls=[]):
    host = hostdic.get("host")
    port = hostdic.get("port")
    user = hostdic.get("username")
    password = hostdic.get("password")
    run_shellpath_ls = []
    std_out_ls = []

    # 本第文件上传到linux
    try:
        t = paramiko.Transport((host, int(port)))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
    except Exception as e:
        return std_out_ls

    try:
        for shellname in shellname_ls:
            lpath = "/home/" + shellname
            dirpath = os.path.join(BASE_DIR, "media")
            dirpath = os.path.join(dirpath,"shellfile")
            filepath = os.path.join(dirpath, shellname)
            sftp.put(filepath, lpath)
            run_shellpath_ls.append(lpath)
        t.close()
    except Exception as e:

        print("问题少年的问题是：", e)

        # 执行shell脚本
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host,port,user,password)
    except Exception as e:
        std_out_ls.append(e)
        print(e)

    try:
        for path in run_shellpath_ls:
            command = "/bin/bash %s"%(path)
            std_in,std_out,std_err = ssh_client.exec_command(command)
            std_out = [i for i in std_out][-1]
            std_out_str = std_out.replace('\r','').replace("\n",'').replace("\t",'')
            print("std_out_str",std_out_str)
            std_out_ls.append(std_out_str)
            time.sleep(0.5)
            # 执行完后删除shell文件
            _,_,_ = ssh_client.exec_command("rm -rf %s"%(path))
            time.sleep(0.5)


        ssh_client.close()
    except Exception as e:
        print(e)

    return std_out_ls


# if __name__ == '__main__':
    # hostdic_ls = [{"host": "192.168.45.100", "port": 22, "username": "root", "password": "root"}]
    # linuxpath = "\home"
    # filename = "test.txt"
    # for hostdic in hostdic_ls:
    #     std_out = upfile_to_linux(hostdic,filename,linuxpath)

    # shellpath_ls = ["test.sh","test1.sh"]
    # for hostdic in hostdic_ls:
    #     std_out_ls = paramiko_uploadfile_to_linux(hostdic, shellpath_ls)
    #     for std_out in std_out_ls:
    #         for line in std_out:
    #             print(line)