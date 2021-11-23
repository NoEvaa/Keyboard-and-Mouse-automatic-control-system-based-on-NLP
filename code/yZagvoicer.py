# -*- coding: utf-8 -*-
"""
Welcome to Noah's Ark
"""
import speech_recognition as sr
from aip import AipSpeech
from requests.exceptions import ConnectionError

from yZnlp_voicer import Voicer_ME_NLPcore
from yZagcompile import ProcedurePart
from yZagtools import YzTools

class YzVoiceMode(Voicer_ME_NLPcore):
    def __init__(self):
        self.baidu_token = {'APP_ID':'', 'API_KEY':'', 'SECRET_KEY':''}
        #baidu: APP_ID   API_KEY   SECRET_KEY
        Voicer_ME_NLPcore.__init__(self)
    def record_au(self):
        try:
            r = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                r.adjust_for_ambient_noise(source)#降噪
                audio = r.listen(source)
            with open("audio\\audio_temp.wav", "wb") as f:
                f.write(audio.get_wav_data(convert_rate=16000))
            return 0
        except OSError:
            return 104
        except:
            return 416
    def __get_file_content(self, file):
        with open(file, 'rb') as f:
            return f.read()
    def baidu_VR(self):
        try:
            aipS = AipSpeech(self.baidu_token['APP_ID'], 
                             self.baidu_token['API_KEY'], 
                             self.baidu_token['SECRET_KEY'])
            result = aipS.asr(self.__get_file_content("audio\\audio_temp.wav"), 'wav', 16000, {'dev_ip': '1536'})
            #print(result)
        except FileNotFoundError:
            return 607, ''
        except ConnectionError:
            return 606, ''
        except:
            return 605, ''
        if result['err_msg'] != 'success.':
            return 810, ''
        result = YzTools.Cn_to_Af(result.get('result', '')[0])
        return 0, result
    def start(self):
        try:
            ec = self.record_au()
            if ec:
                return ec, ''
            return self.baidu_VR()
        except:
            return 415, ''
    def start_RT(self, *args): #real time
        while True:
            ec = self.record_au()
            if ec:
                return ec
            try:
                ec, text = self.baidu_VR()
                for withdraw in ['退出','停止','终止','中止','结束']:
                    if withdraw in text:
                        return 0
                if ec:
                    if ec == 810:
                        continue
                    return ec
                ec, outcome, err = self.text_processing([text])
                if ec:
                    continue
                VldwR1QxTjNQVDA9 = ProcedurePart()
                ec = VldwR1QxTjNQVDA9.write_in(outcome[0])
                if ec:
                    continue
                VldwR1QxTjNQVDA9.excute()
            except:
                return 415