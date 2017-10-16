#!/usr/bin/python
import os
import sys
import glob
import numpy as np
import cPickle

def is_important(line):
    match = ['start_selection_loop', 'correct', 'target', 'item', 'start_round', 'start_adaptation', 'end_adaptation','start_collection', 'end_collection','end_round', 'end_selection_loop']
    for m in match:
        if m in line:
            return True
    return False

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print('[WARNING]: Invalid usages!')
        print('Usage: python edf_converter.py [folder/containing/edfs] [folder/for/output]')
        print('      *no brackets')
        sys.exit(0)

    path = str(sys.argv[1])
    target_path = str(sys.argv[2])
    
    if (not os.path.isdir(path)):
        print('[WARNING]: Path is invalid!')        
        sys.exit(0)
    
    file_paths = glob.glob(path + '/*.edf')

    if (file_paths.count == 0):
        print('[WARNING]: Folder does not contain any .edf files!')        
        sys.exit(0)
    command_line = './edf2asc -r -y {} -p {}'.format(' '.join(file_paths), target_path)
    os.system(command_line)
    
    if not os.path.exists(target_path + '/0'):
        os.makedirs(target_path + '/0')
    if not os.path.exists(target_path + '/1'):
        os.makedirs(target_path + '/1')

    file_paths = glob.glob(target_path + '/*.asc')
    for fp in file_paths:
        person_data_0 = []
        person_data_1 = []
        selection_data = []
        round_data = []
        log_data = False
        prev_msg = []
        target = ''
        brightness = ''
        correct = ''
        keep = False
        max_value = 0

        with open(fp) as f:
            for l in f:
                line = l.rstrip('\n').split()
                if len(line) == 0:
                    continue
                if line[0].isdigit() and float(line[3]) > max_value:
                    max_value = float(line[3])

        with open(fp) as f:
            for l in f:
                line = l.rstrip('\n').split()
                if len(line) == 0:
                    continue
                
                is_msg = False
                is_data = False

                if 'MSG' in line and is_important(line):
                    is_msg = True
                elif line[0].isdigit():# and float(line[3]) > 0: BLINKING REMOVE 100 MS AROUND MAYBE
                    is_data = True

                if 'start_selection_loop' in line:
                    selection_data = []
                    round_data = []
                    log_data = False
                    prev_msg = []
                    target = ''
                    brightness = ''
                    correct = ''
                    keep = False

                if 'start_adaptation' in line:
                    log_data = True
                elif 'end_collection' in line:
                    log_data = False
                    selection_data.append(round_data)
                    round_data = []                    
                
                if 'target' in line and 'start_selection_loop' in prev_msg:
                    target = line[4]
                if 'status=init' in line and 'id="{}"'.format(target) in line:
                    brightness = line[9].replace('brightness=', '')

                if 'correct' in line:
                    correct = line[4]

                if correct == '1':
                    keep = True            
                    correct = ''        

                if log_data and is_data:
                    round_data.append('{}'.format(str(round(float(line[3].replace('.0','')) / max_value * 100, 2))))

                if keep:
                    if (brightness == '1'):
                        person_data_1.append(selection_data)  
                    elif (brightness == '-1'):
                        person_data_0.append(selection_data)  
                    keep = False    

                if is_msg:
                    prev_msg = line       

        with open(target_path + '/0/' + fp.replace('output/', '').replace('asc', 'dat'), 'w') as f:
            np.save(f, person_data_0)
        with open(target_path + '/1/' + fp.replace('output/', '').replace('asc', 'dat'), 'w') as f:
            np.save(f, person_data_1)
        os.remove(fp) #REMOVE ASC FILES 
    print('Parsing completed')