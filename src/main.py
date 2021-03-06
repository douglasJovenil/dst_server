from os import system, getcwd, chdir, popen, environ
from os.path import expanduser
from shutil import rmtree
from sys import argv
import argparse


def main():
  root_path = environ['DST_CLI_PATH'] if 'DST_CLI_PATH' in environ.keys() else f'{getcwd()}/{__file__}'.split('/src')[0]

  parser = argparse.ArgumentParser('CLI to manage the DST server')
  parser.add_argument('--install', help='Configure the container', action='store_true')
  parser.add_argument('--start', help='Start the server', action='store_true')
  parser.add_argument('--stop', help='Stop the server', action='store_true')
  parser.add_argument('--delete', help='Delete the server', action='store_true')
  parser.add_argument('--overworld', help='Open the overworld container', action='store_true')
  parser.add_argument('--underworld', help='Open the underworld container', action='store_true')
  parser.add_argument('--containers', help='List all containers', action='store_true')
  parser.add_argument('--images', help='List all images', action='store_true')

  args = parser.parse_args()

  if (len(argv) <= 1):
    parser.print_help()
    exit(0)

  if (args.install):
    bashrc_path = f'{expanduser("~")}/.bashrc'
    alias_to_add = f'\nalias dst="python3.8 {root_path}/src/main.py"\n'
    env_var_to_add = f'\nexport DST_CLI_PATH={root_path}\n'

  # sudo apt-get install libcurl4-openssl-dev 
    system('sudo apt-get update -y')
    system('sudo apt-get upgrade -y')
    system('sudo apt-get autoremove -y')

    system('sudo apt-get install docker.io apt-transport-https ca-certificates curl gnupg2 software-properties-common  -y')
    system('curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -')

    system('sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose')
    system('sudo chmod +x /usr/local/bin/docker-compose')
    system('sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose')

    chdir(f'{root_path}/container')
    system('sudo docker-compose build')

    with open(bashrc_path, 'r') as f: 
      bashrc = f.read()
    
    if (not alias_to_add in bashrc):
      print('Adding alias')
      with open(bashrc_path, 'w') as f:
        f.write(bashrc + env_var_to_add + alias_to_add)
      system(f'exec bash')

    print('Success configuring server')

  if (args.start):
    chdir(f'{root_path}/container')
    system('sudo docker-compose up -d')

  if (args.stop):
    chdir(f'{root_path}/container')
    system('sudo docker-compose down')
    # containers = getContainers()
    # for container in containers:
    #   system(f'sudo docker stop {container}')
  
  if (args.delete):
    images = set(getImages())

    system('sudo docker system prune')
    
    for image in images:
      print(image)
      system(f'sudo docker rmi {image} -f')  

    system(f'sudo rm {root_path}/container/underworld -rf')
    system(f'sudo rm {root_path}/container/overworld -rf')
  
  if (args.overworld):
    overworld = getContainers()[0]
    system(f'sudo docker exec -it {overworld} /bin/bash')

  if (args.underworld):
    underworld = getContainers()[1]
    system(f'sudo docker exec -it {underworld} /bin/bash')

  if (args.containers):
    system('sudo docker ps')

  if (args.images):
    system('sudo docker images')

def getContainers():
  return popen('sudo docker ps -q').read().split('\n')[:-1]

def getImages():
  return popen('sudo docker images -q').read().split('\n')[:-1]


if __name__ == '__main__':
  main()
