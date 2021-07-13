import os
import fnmatch
import random
import re
import string
import sys
import shutil 

# data_dir = '/home/dhanya/PhD/Datasets/AIR_Kannada_Dataset_graphemes/Kannada_Dataset/'
# uttid_dir = '/home/dhanya/espnet/egs/kannada/asr1/data/local/data_air/'

if len(sys.argv) != 3:
    print("Usage: python data_prep.py [data_dir] [uttid_dir]")
    sys.exit(1)
data_dir = sys.argv[1]
uttid_dir = sys.argv[2]

# Create the output folder
try:
    os.stat(uttid_dir)
except:
    os.makedirs(uttid_dir)
    
print("AIR Data generation")

#remove punctutions and numbers
table = str.maketrans(dict.fromkeys(string.punctuation+'‘""’0123456789Ielnrtx' + '\u200c' + '\u200d'))

for x in ["train", "test"]: 
    
    # Copy src to dst. (cp src dst) 
    shutil.copy(data_dir + x +'.uttids', uttid_dir) 

    ref_file = open(uttid_dir + x +'.uttids','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')
    
    
    utt2spk_list = []
    spk_list = []
    text_list = []
    wav_list = []
    spk2gender_list = []
    for item in ref_file_content:
        
        file_name = item[:6]
        folder_name = item[7:]
        
        spk = file_name
        spk_list.append(spk)  # speaker info
        
        # # spk2gender 
        gender = spk[0].lower()
        spk2gender_str = spk +' '+ gender
        spk2gender_list.append(spk2gender_str)
        
        # utt2spk  : uttid spk
        utt2spk_str = item + ' ' + spk     # utterance_id + speaker
        utt2spk_list.append(utt2spk_str)
        
        # wav.scp : uttid wav_location
        audio_file_path = data_dir + 'Audio' + '/' + folder_name + '/'+ file_name +'.wav'
        wav_str = item + ' ' + 'sox ' + audio_file_path + ' -t wav -r 16000 -b 16 - |'
        wav_list.append(wav_str)
        
        # text file  : uttid transcript
        text_file_path = data_dir + 'Transcript' + '/' + folder_name + '/'+ file_name +'.txt'
        text_file = open(text_file_path,'r')
        text_content = text_file.read().split('\n')
        for line in text_content:
            line = line.translate(table)
            if len(line) != 0:
                text_str = item + ' ' + line 
                text_list.append(text_str)
        
    #sorting
    utt2spk_list.sort()
    wav_list.sort()
    spk2gender_list = list(set(spk2gender_list))
    spk2gender_list.sort()
    text_list.sort()
    spk_list = list(set(spk_list))
    spk_list.sort()
     
    utt2spk_file = open(uttid_dir + x + '.utt2spk','w')
    for item in utt2spk_list:
        utt2spk_file.write(item+'\n')
    utt2spk_file.close()
        
    wav_file = open(uttid_dir + x +'_wav.scp','w')
    for item in wav_list:
        wav_file.write(item+'\n')
    wav_file.close()
    
    spk2gender_file = open(uttid_dir + x + '.spk2gender','w')
    for item in spk2gender_list:
        spk2gender_file.write(item+'\n')
    spk2gender_file.close()
    
    text_file = open(uttid_dir + x + '.text','w')
    for item in text_list:
        text_file.write(item+'\n')
    text_file.close()
    
    ref_file = open(uttid_dir + x +'.utt2spk','r')
    ref_file_content = ref_file.read().split('\n')
    ref_file_content.remove('')
    
    spk2utt_dict = {}
    for spk in spk_list:
        spk2utt_dict[spk] = []     
         
    for item in ref_file_content:
        spk = item.split(' ')[1]
        spk2utt_dict[spk].append(item.split(' ')[0])

    file = open(uttid_dir + x + '.spk2utt','w')
    for spk in spk_list:
        utt_list = spk2utt_dict[spk]
    
        #spk2utt_str = spk + ' ' + ' '.join([str(elem) for elem in utt_list])
        spk2utt_str = spk
        for utt in utt_list:
            spk2utt_str = spk2utt_str + ' ' + utt
        spk2utt_str = spk2utt_str + '\n'
        file.write(spk2utt_str)

    file.close()