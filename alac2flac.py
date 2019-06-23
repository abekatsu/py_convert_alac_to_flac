#!/usr/bin/env python3

import os
import json
import ffmpeg

class AudioFileInfo(object):
    def __init__(self, js):
        self._js = js

    @property
    def path(self):
        return self._js['format']['filename']

    @property
    def codec_type(self):
        return self._js['streams'][0]['codec_type']
    
    @property
    def codec_tag_string(self):
        return self._js['streams'][0]['codec_tag_string']

class AudioFileIterator(object):
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
                    info = AudioFileInfo(ffmpeg.probe(full_path))
                    if self._is_right_file(info):
                        self._filelists.append(info)
                except ffmpeg._run.Error:
                    pass

    def _is_right_file(self, audio_file_info):
        if audio_file_info.codec_type == 'audio':
            return True
        else:
            return False
        

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._i == len(self._filelists):
            raise StopIteration()
        value = self._filelists[self._i]
        self._i += 1
        return value

class ALACFileIterator(AudioFileIterator):
    """
    Apple Lossless file iterator
    """
    def _is_right_file(self, audio_file_info):
        if audio_file_info.codec_type == 'audio' \
        and audio_file_info.codec_tag_string == 'alac':
            return True
        else:
            return False
        

if __name__ == '__main__':
    from os.path import expanduser
    import pickle

    iter = None
    # pickle_filename = './audiofiledictiter.pickle'
    pickle_filename = './alac_file_iterator.pickle'
    try:
        with open(pickle_filename, 'rb') as rf:
            iter = pickle.load(rf)
    except FileNotFoundError:
        home = expanduser("~")
        # iter = AudioFileIterator(home + "/Music/")
        iter = ALACFileIterator(home + "/Music/")    
        with open(pickle_filename, 'wb') as wf:
            pickle.dump(iter, wf)
        
    for fileinfo in iter:
        # print(dict)
        print(fileinfo.path)



