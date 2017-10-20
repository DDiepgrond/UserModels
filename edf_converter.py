#!/usr/bin/python
import os
import sys
import glob
import numpy as np
import cPickle

DOWNSAMPLE_RATE = 775 / 10

def is_important(line):
    match = ['start_selection_loop', 'correct', 'target', 'item', 'start_round', 'start_adaptation', 'end_adaptation','start_collection', 'end_collection','end_round', 'end_selection_loop']
    for m in match:
        if m in line:
            return True
    return False

def downsampling(data):
    # Downsampling of person data
    new_person_data = []
    # Loop through the selection loops of the person
    for s in xrange(len(data)):
        new_person_data.append([])
        # Loop through the rounds in the selection loop
        for r in xrange(0, len(data[s])):
            new_person_data[s].append([])
            #print new_person_data
            for d in xrange(0, len(data[s][r]), DOWNSAMPLE_RATE):
                f_dat = [float(j) for j in data[s][r]]
                new_person_data[s][r].append(str(np.nanmedian(f_dat[d:len(f_dat)]) if len(f_dat) < d + DOWNSAMPLE_RATE else np.nanmedian(f_dat[d:d + DOWNSAMPLE_RATE])))
    return new_person_data

if __name__ == "__main__":
    #if (len(sys.argv) != 3):
    if (len(sys.argv) != 2):
        print('[WARNING]: Invalid usages!')
        #print('Usage: python edf_converter.py [folder/containing/edfs] [folder/for/output]')
        print('Usage: python edf_converter.py [folder/for/output]')
        print('      *no brackets')
        sys.exit(0)

    #path = str(sys.argv[1])
    #target_path = str(sys.argv[2])
    target_path = str(sys.argv[1])
    
    #if (not os.path.isdir(path)):
        #print('[WARNING]: Path is invalid!')        
        #sys.exit(0)
    
    '''file_paths = glob.glob(path + '/*.edf')

    if (file_paths.count == 0):
        print('[WARNING]: Folder does not contain any .edf files!')        
        sys.exit(0)
    command_line = './edf2asc -r -y {} -p {}'.format(' '.join(file_paths), target_path)
    os.system(command_line)
    sys.exit()'''
    if not os.path.exists(target_path + '/0'):
        os.makedirs(target_path + '/0')
    if not os.path.exists(target_path + '/1'):
        os.makedirs(target_path + '/1')

    file_paths = glob.glob(target_path + '/*.asc')
    
    print 'Finding min and max values!'
    max_value = 0
    min_value = 9999
    for fp in file_paths:
        with open(fp) as f:
            for l in f:
                line = l.rstrip('\n').split()
                if len(line) == 0:
                    continue
                if line[0].isdigit():
                    if float(line[3]) > max_value:
                        max_value = float(line[3])
                    if float(line[3]) > 0 and float(line[3]) < min_value:
                        min_value = float(line[3])
    print min_value
    print max_value
    print 'Converting...'
    for fp in file_paths:
        person_data_0 = []
        person_data_1 = []
        selection_data = []
        round_data = []
        log_data = False
        #prev_msg = []
        #target = ''
        brightness = ''
        correct = ''
        #keep = False
        msg_log = []

        with open(fp) as f:
            for l in f:
                line = l.rstrip('\n').split()
                if len(line) == 0:
                    continue
                
                is_msg = False
                is_data = False

                if 'start_selection_loop' in line:
                    selection_data = []

                if 'start_adaptation' in line:
                    log_data = True

                if 'MSG' in line and is_important(line):
                    is_msg = True
                elif line[0].isdigit():
                    is_data = True
                
                if log_data and is_data:
                    x = float(line[3].replace('.0',''))
                    value = round((x - min_value) / (max_value - min_value), 4)
                    round_data.append('{}'.format(str(value))) 

                if 'end_collection' in line:
                    log_data = False
                    selection_data.append(round_data)
                    round_data = []                

                if 'status=winner' in line:
                    brightness = '-1' if float(line[12].replace('x=', '')) < 0 else '1'
                
                if 'correct' in line:
                    correct = line[4]
                
                if correct is '1':
                    if (brightness is '-1'):
                        person_data_0.append(selection_data)
                    elif (brightness is '1'):
                        person_data_1.append(selection_data) 
                    correct = ''
                    brightness = ''
                '''
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
                if 'status=winner' in line:# and 'id="{}"'.format(target) in line:
                    brightness = '-1' if float(line[12].replace('x=', '')) < 0 else '1'#line[9].replace('brightness=', '')

                if 'correct' in line:
                    correct = line[4]

                if correct == '1':
                    keep = True         

                #print 'cor: {}\nkeep: {}\n bright: {}\ntarget: {}\n'.format(correct, keep, brightness, target)

                if log_data and is_data:
                    round_data.append('{}'.format(str(round(float(line[3].replace('.0','')) / max_value * 100, 2))))                
                

                if keep:
                    if (brightness == '1'):
                        person_data_1.append(selection_data)  
                    elif (brightness == '-1'):
                        person_data_0.append(selection_data)         
                    correct = ''   
                    keep = False    
                if is_msg:
                    prev_msg = line'''

        print 'Raw 0 | n_s {}, n_r {}, n_d {}, tot_sd {}'.format(len(person_data_0), len(person_data_0[0]), len(person_data_0[0][0]), len(person_data_0[0] * len(person_data_0[0][0])))
        print 'Raw 0 | n_s {}, n_r {}, n_d {}, tot_sd {}'.format(len(person_data_1), len(person_data_1[0]), len(person_data_1[0][0]), len(person_data_1[0] * len(person_data_1[0][0])))
        
        new_person_data_0 = downsampling(person_data_0)
        new_person_data_1 = downsampling(person_data_1)

        print 'Downsampled 0 | n_s {}, n_r {}, n_d {}, tot_sd {}'.format(len(new_person_data_0), len(new_person_data_0[0]), len(new_person_data_0[0][0]), len(new_person_data_0[0] * len(new_person_data_0[0][0])))
        print 'Downsampled 0 | n_s {}, n_r {}, n_d {}, tot_sd {}'.format(len(new_person_data_1), len(new_person_data_1[0]), len(new_person_data_1[0][0]), len(new_person_data_1[0] * len(new_person_data_1[0][0])))
        
        with open(target_path + '/0/' + fp.replace('output/', '').replace('asc', 'dat'), 'w') as f:
            np.save(f, new_person_data_0)
        with open(target_path + '/1/' + fp.replace('output/', '').replace('asc', 'dat'), 'w') as f:
            np.save(f, new_person_data_1)
        #os.remove(fp) #REMOVE ASC FILES 
    print('Parsing completed')