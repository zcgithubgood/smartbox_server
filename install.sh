sudo apt-get install virtualenv
sudo apt-get install python-dev

cd ..
sudo virtualenv ENV_smartbox
cd smartbox
../ENV_smartbox/bin/pip install -r requirements.txt
