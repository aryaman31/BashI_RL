vim /etc/ansible/hosts 
ls
mkdir roles
ansible-galaxy init win_ad_install
ls
rm -rf win_ad_install/
ls
cd roles/
rm -rf win_ad_install/
ansible-galaxy init win_ad_install
ls
cd win_ad_install/
ls
cd tasks/
ls
vim main.yml 
vim install_ad_service.yml
vim ad_controller.yml
vim reboot.yml
ansible - m win_ping windows
ansible -m win_ping windows
vim print_domainlist.yml
cd ..
cd vars/
ls
vim main.yml 
cd ../tasks/
ls
vim ad_controller.yml 
cd ..
ls
cd ..
ls
cd win_ad_install/
cd tests/
ls
vim inventory 
vim test.yml 
cd ../..
ls
vim ad.yml
ansible-playbook ad.yml 
cd win_ad_install/
ls
cd tasks/
ls
vim main.yml 
cd ..
ansible-playbook ad.yml 
cd win_ad_install/
vim tasks/main.yml 
vim tasks/print_domainlist.yml 
cd ..
ansible-playbook ad.yml 
vim win_ad_install/tasks/print_domainlist.yml 
ansible-playbook ad.yml 
vim win_ad_install/tasks/print_domainlist.yml 
ansible-playbook ad.yml 
vim win_ad_install/tasks/print_domainlist.yml 
ansible-playbook ad.yml -e "GUID=2b3b"
vim win_ad_install/tasks/print_domainlist.yml 
ansible-playbook ad.yml -e "GUID=2b3b"
ansible-playbook ad.yml -e
vim win_ad_install/tasks/print_domainlist.yml 
ansible-playbook ad.yml -e "GUID=2b3b"
vim win_ad_install/tasks/ad_controller.yml 
vim win_ad_install/vars/main.yml 
ansible-playbook ad.yml 
vim win_ad_install/tasks/main.yml 
vim win_ad_install/tasks/reboot.yml 
vim win_ad_install/tasks/ad_controller.yml 
vim win_ad_install/tasks/print_domainlist.yml 
ansible-playbook ad.yml 
ansible-playbook ad.yml -vvvv
cd ~
ls
python-devel
sudo yum install python-devel krb5-devel krb5-libs krb5-workstation python-pip gcc
sudo pip install pywinrm
pip install pywinrm[kerberos]
sudo pip install pywinrm[kerberos]
sudo export GUID=`hostname | awk -F"." '{print $2}'`
cat << EOF > /etc/krb5.conf.d/ansible.conf
[realms]

 AD1.${GUID_CAP}.EXAMPLE.OPENTLC.COM = {

 kdc = ad1.${GUID}.example.opentlc.com
 }

[domain_realm]
 .ad1.${GUID}.example.opentlc.com = AD1.${GUID_CAP}.EXAMPLE.OPENTLC.COM
EOF

sudo cat << EOF > /etc/krb5.conf.d/ansible.conf
[realms]

 AD1.${GUID_CAP}.EXAMPLE.OPENTLC.COM = {

 kdc = ad1.${GUID}.example.opentlc.com
 }

[domain_realm]
 .ad1.${GUID}.example.opentlc.com = AD1.${GUID_CAP}.EXAMPLE.OPENTLC.COM
EOF

sudo cat << EOF > /etc/krb5.conf.d/ansible.conf
[realms]

 AD1.${GUID_CAP}.EXAMPLE.OPENTLC.COM = {

 kdc = ad1.${GUID}.example.opentlc.com
 }

[domain_realm]
 .ad1.${GUID}.example.opentlc.com = AD1.${GUID_CAP}.EXAMPLE.OPENTLC.COM
EOF

sudo su
cat /etc/krb5.conf.d/ansible.conf
                
kinit administrator@AD1.2b3b.EXAMPLE.OPENTLC.COM
kinit administrator@AD1.${GUID_CAP}.EXAMPLE.OPENTLC.COM
Password for administrator@AD1.${GUID_CAP}.EXAMPLE.OPENTLC.COM:
sudo su
