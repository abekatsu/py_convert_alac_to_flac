#!/usr/bin/env python3

import os
import json
import ffmpeg

class AudioFileDictIterator(object):
    """
    Iterator for dictionary with Audio file

    参考
    Pythonのイテレータとジェネレータ
    https://qiita.com/tomotaka_ito/items/35f3eb108f587022fa09
    """
    
    def __init__(self, input_path):
        self._filelists = []
        self._i = 0
        for dir_path, subdir_list, file_list in os.walk(input_path):
            for fname in file_list:
                full_path = os.path.join(dir_path, fname)
                try:
                    js = ffmpeg.probe(full_path)
                    if js['streams'][0]['codec_type'] == 'audio':
                        self._filelists.append({ "path" : full_path,
                                                 "probe" : js })
                except ffmpeg._run.Error:
                    pass

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._i == len(self._filelists):
            raise StopIteration()
        value = self._filelists[self._i]
        self._i += 1
        return value


if __name__ == '__main__':
    from os.path import expanduser
    import pickle

    iter = None
    pickle_filename = './audiofiledictiter.pickle'
    try:
        with open(pickle_filename, 'rb') as rf:
            iter = pickle.load(rf)
    except FileNotFoundError:
        home = expanduser("~")
        iter = AudioFileDictIterator(home + "/Music/")    
        with open(pickle_filename, 'wb') as wf:
            pickle.dump(iter, wf)
        
    for dict in iter:
        print(dict['probe']['streams'][0])
        print(dict['path'])



