import os
import subprocess

KEYS_DIR = "./keys"
#Create keys dir
if not os.path.exists(KEYS_DIR):
    os.makedirs(KEYS_DIR)
    print("Put your keys in " + KEYS_DIR + ".")
    exit(0)

#Setup variables
print("Enter host: ", end="")
HOST = input()
print("Enter username [\"root\"]: ", end="")
value = input()
USERNAME = value if value else "root"

print("\nConcatinating your keys...")
keys = os.listdir(KEYS_DIR)
all_keys = ""
for key in keys:
    path = os.path.join(KEYS_DIR, key)
    #Only files without an extension
    if (os.path.splitext(path)[1] == ".pub"):
        with open(path) as file:
            all_keys += "\n".join([line for line in file.readlines() if line.strip() != ""])
            if not all_keys.endswith("\n"):
                all_keys += "\n"

with open("keys.pub", "w") as file:
    file.write(all_keys)

print("Copying your keys to the server...")
print("Follow the instructions of \"ssh-copy-id\":")
print("="*60)
#Start copying the key
ssh = subprocess.Popen(["ssh-copy-id", "-i./keys.pub", USERNAME + "@" + HOST], \
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)

ssh.wait()
os.remove("keys.pub")

print("="*60)
print("Done with copying keys!")

print("Preparing configuration script...")
config_script = "cat /etc/ssh/sshd_config | "
config_script += "sed -e \"s/PubkeyAuthentication/#PubkeyAuthentication/g\" | "
config_script += "sed -e \"s/PasswordAuthentication/#PasswordAuthentication/g\" | "
config_script += "sudo tee /etc/ssh/sshd_config.tmp && "
config_script += "echo PubkeyAuthentication yes | sudo tee -a /etc/ssh/sshd_config.tmp && "
config_script += "echo PasswordAuthentication no | sudo tee -a /etc/ssh/sshd_config.tmp && "
config_script += "sudo rm /etc/ssh/sshd_config && "
config_script += "sudo mv /etc/ssh/sshd_config.tmp /etc/ssh/sshd_config && "
config_script += "sudo service ssh restart"

print("Evaluating the script on ssh...")
print("Follow the instructions of \"ssh\":")
print("="*60)
ssh = subprocess.Popen(["ssh", USERNAME + "@" + HOST, config_script], \
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)

ssh.wait()

print("="*60)
print("Everything is ready now!")
