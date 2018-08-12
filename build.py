import subprocess 
import os
import sys 

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path)

    icon_path = os.path.join('flanker', 'icon.ico')
    main_path = os.path.join('flanker', 'main.py')
    command = f'{sys.executable} -m PyInstaller --icon {icon_path} --noconsole --name neuropsy {main_path}'
    process = subprocess.Popen(command.split())
    process.wait()

    with open('neuropsy.spec') as fp:
        lines = fp.readlines()
        lines.insert(1, 'from kivy.deps import sdl2, glew \n')

    with open('neuropsy.spec', 'w+') as fp:
        for i in range(len(lines)):
            print(lines[i])
            if 'COLLECT' in lines[i]:
                lines[i] = lines[i].strip(' \t\n\r') + " Tree('flanker'), \n"
            if 'a.datas' in lines[i]:
                space = ''.join([' ' for i in range(len(lines[i]) - len(lines[i].lstrip()))])
                lines[i] += f'{space}*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)], \n'

        fp.writelines(lines)

    command = f'{sys.executable} -m PyInstaller neuropsy.spec'
    process = subprocess.Popen(command.split())
    process.wait()
