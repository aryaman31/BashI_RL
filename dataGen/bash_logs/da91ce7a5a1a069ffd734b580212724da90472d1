sudo apt-get install ruby-full
irb
sudo apt-get install curl
bash < <(curl -sL https://raw.github.com/railsgirls/installation-scripts/master/rails-install-ubuntu.sh)
cd ~
wget http://c758482.r82.cf2.rackcdn.com/sublime-text_build-3083_amd64.deb
cd ~
wget http://c758482.r82.cf2.rackcdn.com/sublime-text_build-3083_amd64.deb
sudo add-apt-repository ppa:webupd8team/sublime-text-2
$ sudo apt install git-all
sudo apt install git-all
ssh-keygen -t rsa
ssh-copy-id tomasaki@78.62.22.39
cat ~/.ssh/id_rsa.pub | ssh tomasaski@78.62.22.39 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat




ssh-keygen
exit


exit



ssh-keygen
ssh-copy-id tomas@remote_host
ssh-copy-id tomas@78.62.22.39
ssh-copy-id tomas@tomas-VirtualBox
sudo nano /etc/ssh/sshd_config
sudo apt-get update
sudo apt-get install openssh-server
sudo ufw allow 22
ls -l ~/.ssh/id_*.pub
ssh-keygen -t rsa -b 4096 -C "tomas.orentas@gmail.com"
ls ~/.ssh/id_*
ssh-copy-id tomas@78.62.22.39
sudo ufw allow ssh
ssh-copy-id tomas@78.62.22.39
sudo sshd -T
ssh
ssh tomas@78.62.22.39
sudo apt-get install openssh-server
clear
sudo service ssh status
ssh localhost
clear
sudo gedit /eetcssh/sshd config
ssh-keygen
ssh-copy-id tomas@78.62.22.39
ssh-copy-id tomas@tomas-VirtualBox
cat ~/.ssh/id_rsa.pub | ssh username@remote_host "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod -R go= ~/.ssh && cat >> ~/.ssh/authorized_keys"
cat ~/.ssh/id_rsa.pub | ssh tomas@tomas-VirtualBox "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod -R go= ~/.ssh && cat >> ~/.ssh/authorized_keys"
cat ~/.ssh/id_rsa.pub | ssh tomas@78.62.22.39 "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod -R go= ~/.ssh && cat >> ~/.ssh/authorized_keys"
cat ~/.ssh/id_rsa.pub | ssh tomas@tomas-VirtualBox "mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod -R go= ~/.ssh && cat

>> ~/.ssh/authorized_keys"
cat ~/.ssh/id_rsa.pub
mkdir -p ~/.ssh
echo public_key_string >> ~/.ssh/authorized_keys
chmod -R go= ~/.ssh
chown -R sammy:sammy ~/.ssh
chown -R tomas:tomas ~/.ssh
ssh tomas@tomas-VirtualBox 
ssh-copy-id tomas@tomas-VirtualBox 
cat ~/.ssh/id_rsa.pub
mkdir -p ~/.ssh
echo public_key_string >> ~/.ssh/authorized_keys
ssh tomas@tomas-VirtualBox 
ssh tomas.orentas@gmail.com
ssh mkdir ~/.ssh && touch ~/.ssh/authorized_keys
chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
ssh tomas@tomas-VirtualBox 
mkdir ~/.ssh && touch ~/.ssh/authorized_keys
chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
scp ~/.ssh/id_rsa.pub tomas@78.62.22.39:~/.ssh/authorized_keys
scp ~/.ssh/id_rsa.pub tomas@203.0.113.10:~/.ssh/authorized_keys
ssh tomas@tomas-VirtualBox 
When you run the commands above, the out should look like the one below…
ssh-copy-id richard@10.0.2.6
The authenticity of host '10.0.2.6 (10.0.2.6)' can't be established.
ECDSA key fingerprint is SHA256:GPeNZbX26TFHJ/zaqVNppD7m9pLvZ3jINahxXy226q4.
Are you sure you want to continue connecting (yes/no)? yes

Type yes to export the key.

After you type your SSH password for the remote host, the key should be successfully installed.

Number of key(s) added: 1

Now try logging into the machine, with: "ssh 'richard@10.0.2.6'"
and check to make sure that only the key(s) you wanted were added.

Now your public key is stored on the remote server…

Now when you logon to the remote server, access should be granted without you typing a password..

ssh richard@10.0.2.6
Welcome to Ubuntu 18.04 LTS (GNU/Linux 4.15.0-20-generic x86_64)

* Documentation: https://help.ubuntu.com
* Management: https://landscape.canonical.com
* Support: https://ubuntu.com/advantage

System information as of Sat Apr 28 02:50:34 UTC 2018

If you’re using a non Linux host or can’t use ssh-copy-id command, you can manually copy your public key and paste into the authorized_keys file on th remote host..

Run the commands below to display your public key…

cat ~/.ssh/id_rsa.pub

The output should look like the linke below..

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDV2FxeXfKhsabnom7Esmh+r2Jf3WF+cqjv1BNXp5zdZhtiEHNT+4qJSxDyJ61DsbJOUX0MANG3geVgUVCkk/gR4hOHGBlJbuUlZRmCZVr5jNSvpBkXrB1M8WB73vwJy3cK0dMtcAQmNdKo23KYAR8/zKlv9lg4mc41qSwnhIXtrL5iyp9s+29bz84oxlsUc3+C0Y4aUWpVYNq4iH62CT0GZDC0vC8up5U/kSEkRbXjZerfnbQBYnsLb7g2SQRRUogauonCMlz1zrWMTP9EK8HdQdp7EaHcagFu3z3PQPMPaIRwJcahmAZIoNN0c2JEdg36j4RPik7CSDQVCA37IdDp richard@ubuntu1804

Copy the entiree key content and paste into ~/.ssh/authorized_keys file you create on the remote host..
Step 3: Disable SSH Password Authentication

Now that you know SSH key authentication works, you can now disable password authentication to enable enhanced SSH security… Connecto the the SSH remote host and open the configuration file by running the commands below

sudo nano /etc/ssh/sshd_config

Then change the line below to no

...
# To disable tunneled clear text passwords, change to no here!
PasswordAuthentication no
...

Save the file and exit…

Restart SSH Server

sudo systemctl restart ssh.service

That’s it!

Now only SSH clients with keys in the authorized_keys file will be allow to access the server.

You may also like the post below:

Setup OpenSSH Key Authentication (Passwordless) on Ubuntu 16.04 LTS Server
Setup OpenSSH Key Authentication (Passwordless) on Ubuntu 16.04 LTS Server
Setup SSH Server for Key Authentication on Ubuntu 17.04 / 17.10
Setup SSH Server for Key Authentication on Ubuntu 17.04 / 17.10
Lesson 41: Logon to Ubuntu via SSH Without Passwords
Lesson 41: Logon to Ubuntu via SSH Without Passwords
!robot

This post was not written by a robot. I spend my spare time searching for ways to help students and new users get to know and understand Linux, Ubuntu, Windows, and Open Source software. ~Enjoy!
One Comment

    mostafa12/06/2018
    Reply

    thank you very much for this infos

Add a Comment

Your email address will not be published. Required fields are marked *

Comment:*

Name:*

Email Address:*

Save my name, email, and website in this browser for the next time I comment.

This site uses Akismet to reduce spam. Learn how your comment data is processed.



Our Popular Posts

    Install the Latest Node.js and NPM Packages on Ubuntu 16.04 / 18.04 LTS
    Configure Static IP Addresses on Ubuntu 18.04 LTS Server
    Connect to Ubuntu 16.04 / 17.10 / 18.04 Desktop via Remote Desktop Connection (RDP) with Xrdp
    Install Proprietary Nvidia GPU Drivers on Ubuntu 16.04 / 17.10 / 18.04
    How to Install Eclipse Oxygen IDE on Ubuntu 16.04 / 17.10 / 18.04
    Enable Screen Sharing on Ubuntu 18.04 LTS Desktop via VNC from Windows Machines
    WordPress 4.9.9 / 5.0.1 Security Released Available -- You Should Upgrade Immediately
    Install Notepad++ on Ubuntu 16.04 / 17.10 / 18.04 via Snap
    Install Adobe Flash Player on Ubuntu 18.04 LTS Desktop





sudo servic
sudo service ssh status
sudo ssh tomas@78.62.22.39
sudo vi /etc/ssh/sshd_config
sudo vi /etc/ssh/sshd config
mkdir odin_on_rails
rails new my_first_rails_app
gem install rails
ghjfg

gem install rails
exit
sudo mkdir odin_on_rails
cd odin_on_rails
rails new my_first_rails_app
sudo rails new_my_dirst_rails_app
sudo mu_first_rails_app
git config --global color.ui true
git config --global user.name "Tomas"
git config --global user.email "tomas.orentas@gMAIL.com"
pwd /home/tomas/odin_on_rails/my_first_rails_app
git init
git commit -m "initial commit"
git remote add origin https://github.com/Moogulthesly/Tomas.git
git remote add origin <https://github.com/Moogulthesly/Tomas.git>
git push -u origin master
git remote add origin https://github.com/Moogulthesly/Tomas.git
git push -u origin master
git checkout master
git remote add origin https://github.com/Moogulthesly/Tomas.git
git init
git remote add origin https://github.com/Moogulthesly/Tomas.git
git push -u origin master
git commit -m "initial commit"
git push origin master
git show-ref
touch README
git commit -m 'reinitialized files'
git push origin master --force
git push origin HEAD:<remoteBranch> 
git commit -m "initial commit"
git push origin master
git init
git add .
git init
git add
git add .
