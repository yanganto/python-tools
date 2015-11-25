"""
    Send command over ssh

USAGE:
    sshcmd.py [ip:port] [username] [password] [command]

EXAMPLE:
    sshcmd.py 192.168.2.100:22 yanganto mypassword ls -l
"""
import paramiko
import sys


def ssh_command(addr, user, password, command):
    ip,  port_str = addr.split(':')
    port = int(port_str) if port_str else 22
    client = paramiko.SSHClient()
    # client.load_host_keys('/home/yanganto/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=user, password=password)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024))
    return ssh_session.recv(1024)

if __name__ == '__main__':
    if len(sys.argv[1:]) < 5:
        print(__doc__)
        sys.exit(0)
    else:
        command = ' '.join(sys.argv[4:])
        ssh_command(sys.argv[1], sys.argv[2], sys.argv[3], command)
