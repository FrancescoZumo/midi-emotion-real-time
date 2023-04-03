from os.path import isfile, join
import os
import time
import pygame
import sys
import numpy as np
import my_utils


def play_music(midi_filename):
    '''Stream music_file in a blocking manner'''
    clock = pygame.time.Clock()
    pygame.mixer.music.load(midi_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(30)  # check if playback has finished


while True:
    model_used = 'continuous_token'
    project_abs_path = 'C:\\Users\\franc\\PycharmProjects\\midi-emotion'
    generations_rel_path = '\\output\\' + model_used + '\\generations\\inference'
    generations_abs_path = project_abs_path + generations_rel_path

    valence = 0
    arousal = 0

    primers, maps = my_utils.import_primers()

    # questa roba da errore, capisci perché
    # prova asemplicemente prendere un midi di quelli giusti in input, magari è quello che sminchia la variabile usata come primer
    primer_inds = [[maps["tuple2idx"][symbol] for symbol in primer] for primer in primers]
    
    print('loop started')
    os.system('del /q ' + generations_abs_path + '\\*')
    os.chdir('src')
    tmp = os.getcwd()
    print('Current path: ', tmp)
    os.system('python generate.py --gen_len 320 --model_dir ' + model_used + ' --conditioning ' + model_used + 
              ' --batch_size 1 --valence '+ str(valence) + ' --arousal ' + str(arousal))
    os.chdir('..')
    tmp = os.getcwd()
    print('Current path: ', tmp)

    files = [f[:] for f in os.listdir(generations_abs_path) if isfile(join(generations_abs_path, f))]

    os.chdir(generations_rel_path[1:])
    tmp = os.getcwd()
    print('Current path: ', tmp)

    # mixer config
    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024  # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)

    for i, file in enumerate(files):

        if not file.endswith('.mid'):
            continue

        midi_filename = file
        print('playing ', i, ' file')

        # listen for interruptions
        try:
            # use the midi file you just saved
            play_music(midi_filename)
        except KeyboardInterrupt:
            # if user hits Ctrl/C then exit
            # (works only in console mode)
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.stop()
            raise SystemExit

    os.chdir('..\\..\\..\\..')
    print('finished, repeating loop...')

