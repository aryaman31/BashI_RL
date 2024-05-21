bash
ls -a
sudo bash
sudo bash
sudo -i
sudo bash
bash
sudo bash
sudo bash
ls
export GUID=e136
pwd
ls
id cloud-user
wget http://www.opentlc.com/download/ansible_bootcamp/openstack_keys/openstack.pub
ls -ltr
ls -a
mv openstack.pub .ssh
cd .ssh
ls -ltr
ls -alte
ls -altr
mv .ssh openstack.pub
mkdir .ssh
chmod 700 .ssh
cd .ssh
ls
cp ../openstack.pub .
ls
cat openstack.pub 
vi authorized_keys
export GUID=e136
export MYKEY=~/.ssh/openstack.pub
export MYUSER=arunkumar.das-wipro.com
ssh -i ${MYKEY} ${MYUSER}@workstation-${GUID}.rhpds.opentlc.com
ssh ${MYUSER}@workstation-${GUID}.rhpds.opentlc.com
ssh -i openstack.pub cloud-user@workstation-${GUID}.rhpds.opentlc.com
export MYUSER=cloud-user
ssh -i ${MYKEY} ${MYUSER}@workstation-${GUID}.rhpds.opentlc.com
ssh -i ${MYKEY} cloud-user@workstation-${GUID}.rhpds.opentlc.com
pwd
cd /home
ls
cd .ssh
cd arunkumar.das-wipro.com/
cd .ssh/
ls
wget http://www.opentlc.com/download/ansible_bootcamp/openstack_keys/openstack.pem -O ~/.ssh/openstack.pem
ls -ltr
cat openstack.pem
vi authorized_keys 
export MYKEY=~/.ssh/openstack.pem
ssh -i ${MYKEY} cloud-user@workstation-${GUID}.rhpds.opentlc.com
ls -ltr
chmod 400 openstack.p*
ssh -i ${MYKEY} cloud-user@workstation-${GUID}.rhpds.opentlc.com
ssh -i openstack.pem cloud-user@workstation-e136.rhpds.opentlc.com
ssh -i openstack.pem arunkumar.das-wipro.com@workstation-e136.rhpds.opentlc.com
bash
cd .ssh
ls
touch ssh.cfg
cd ..
cat << EOF > osp_jumpbox_inventory
[jumpbox]
workstation-${GUID}.rhpds.opentlc.com ansible_ssh_user=cloud-user ansible_ssh_private_key_file=~/.ssh/openstack.pem
EOF

export GUID=e136
cd .ssh
vi ssh.cfg 
cat << EOF >> ssh.cfg
Host workstation-${GUID}.rhpds.opentlc.com
 Hostname workstation-${GUID}.rhpds.opentlc.com
 IdentityFile ~/.ssh/openstack.pem
 ForwardAgent yes
 User cloud-user
 StrictHostKeyChecking no
 PasswordAuthentication no

Host 10.10.10.*
 User cloud-user
 IdentityFile ~/.ssh/openstack.pem
 ProxyCommand ssh -F ./ssh.cfg workstation-${GUID}.rhpds.opentlc.com -W %h:%p
 StrictHostKeyChecking no
EOF

cat ssh.cfg 
mv ssh.cfg ..
ls
cd ..
ls -ltr
ansible -i osp_jumpbox_inventory all -m ping
cd .ssh
ls
rm openstack.pub 
cat authorized_keys 
rm authorized_keys 
cd ..
ansible -i osp_jumpbox_inventory all -m ping
echo $GUID
ls
ansible -i osp_jumpbox_inventory all -m ping
vi osp_jumpbox_inventory
ansible -i osp_jumpbox_inventory all -m ping
ansible -i osp_jumpbox_inventory jumpbox -m os_user_facts -a cloud=ospcloud -v
bash
ls
ansible -i osp_jumpbox_inventory jumpbox -m os_user_facts -a cloud=ospcloud -v
ls
cat << EOF > ansible.cfg
[defaults]
inventory=./osp_jumpbox_inventory

[privilege_escalation]
become=True
become_method=sudo

[ssh_connection]
ssh_args=" -F ./ssh.cfg -o ControlMaster=auto -o ControlPersist=60s"
host_key_checking=False
EOF

more ansible.cfg 
ls
cd roles
ansible-galaxy init osp-network
ls
ansible-galaxy init osp-network -vvv
cd /usr/share/ansible/plugins/modules
cd /usr/share/ansible/
cd /usr/share/
ls
cd -
ls
id
ansible-galaxy init osp-network
sudo -i
ls
cd roles
ls
cd osp-network/
ls
sudo -i
sudo -i
sudo -i
ls
sudo -i
ls
sudo -i
