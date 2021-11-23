# -*- coding: utf-8 -*-
"""
Welcome to Noah's Ark
"""
import pickle
import jieba
import jieba.posseg
import nltk
import pyautogui
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from yZagtools import YzTools

jieba.load_userdict("models\\u_dict.txt")

class Voicer_ME_NLPcore: #mouse event
    def __init__(self):
        self.tc = ME_tc() #分类器
        self.ie = ME_ie() #提参器
    def text_processing(self, text_list): #文本处理主函数
        '''
        Return:
            ec                  (int)     错误码
            treatment_result    (list)    处理结果
            errors              (list)    解析失败数
        '''
        try:
            ec, y, errors_c = self.tc.tc(text_list)
        except:
            return 601, [], []
        if ec:
            return ec, [], []
        i = len(text_list) - 1
        while i>-1:
            if i in errors_c:
                del text_list[i]
            i -= 1
        errors_e = []
        treatment_result = []
        for i in range(len(text_list)):
            ec, temp = self.__extract_datalist(text_list[i], y[i])
            if ec:
                errors_e.append(i)
                continue
            treatment_result.append(temp)
        if treatment_result == []:
            return 808, [], []
        return 0, treatment_result, [len(errors_c), len(errors_e)]
    def __extract_datalist(self, text, y):
        if y>7 or y<0:
            return 411, []
        #[ops1, ops2, int(x), int(y), float(duration), int(clicks), float(interval), int(button), '']
        try:
            ec, datalist = self.ie.ie(text, y)
            if ec:
                return 808, []
        except:
            return 602, []
        return 0, datalist

class ME_tc:
    def __init__(self):
        self.model_BOW = None
        self.model_SVM = None
    def __check_models(self):
        if self.model_BOW == None or self.model_SVM == None:
            return True
        return False
    def __load_models(self):
        path = "models/voicer/"
        try:
            with open(path+"classifier.pkl", 'rb') as fw:
                self.model_SVM = pickle.load(fw)
            self.model_BOW = CountVectorizer(token_pattern=r"(?u)\b\w+\b", 
                                             decode_error='replace', 
                                             vocabulary=pickle.load(open(path+"feature.pkl", "rb")))
            return 0
        except:
            return 807
    def tc(self, text_list=[]): #SVM快速分类
        if self.__check_models():
            if self.__load_models():
                return 807, [], []
        try:
            ec, X, errors = self.__text_pretreatment(text_list)
            if ec:
                return ec, [], []
            return 0, self.model_SVM.predict(X), errors
        except:
            return 414, [], []
    def __text_pretreatment(self, text_list): #文本预处理
        if text_list == []:
            return 102, [], []
        split_corpus = []
        for text in text_list:
            temp = jieba.lcut(text)
            i = 0
            while(i<len(temp)):
                if YzTools.isNotValid(temp[i]):
                    del temp[i]
                    continue
                i += 1
            split_corpus.append( ' '.join(temp) )
        X = self.model_BOW.transform(split_corpus)
        X = X.toarray()
        errors = []
        i = len(X) - 1
        while i>-1:
            if set(X[i]) == {0}:
                errors.append(i)
                X = np.delete(X, i, axis=0)
            i -= 1
        return 0, X, errors

class ME_ie:
    def __init__(self):
        self.ck = ME_ie_chunking() #分块器
    def get_pos_list(self, text): #生成词性序列
        return [(w.word, w.flag) for w in jieba.posseg.lcut(text)]
    def ie_list(self, textl, yl):
        if textl == []:
            return 102, []
        if len(textl) != len(yl):
            return 103, []
        error_l = []
        temp_result = []
        for i in range(len(yl)):
            ec, temp = self.ie(textl[i], yl[i])
            if ec:
                error_l.append(i)
                continue
            temp_result.append(temp)
        return error_l, temp_result  
    def ie(self, text, y):
        pos_list = self.get_pos_list(text)
        ec, cktree = self.ck.chunking(pos_list, y)
        if ec:
            return 806, []
        ec, datalist = self.__extracting(cktree, y)
        if ec:
            return 808, []
        return 0, datalist
    def __extracting(self, cktree, y):
        #print(cktree)
        #[ops1, ops2, int(x), int(y), float(duration), int(clicks), float(interval), int(button), '']
        ops = [int(y/4), y%4]
        if (ops[0] == 0) and (ops[1] in [0, 2]):
            xy = []
            for tag in cktree.subtrees():
                if tag.label() == 'CD':
                    for wd in tag:
                        if wd[0].isdigit():
                            xy.append(int(wd[0]))
                    if len(xy) == 2:
                        break
                    xy = []
                if tag.label() == 'CDF':
                    for wd in tag:
                        if wd[1] == 'f':
                            scW, scH = pyautogui.size()
                            if '中' in wd[0]:
                                xy = [scW/2, scH/2]
                                break
                            if '角' in wd[0]:
                                if '左' in wd[0]:
                                    xy.append(1)
                                elif '右' in wd[0]:
                                    xy.append(scW-1)
                                else:
                                    xy = []
                                    break
                                if '上' in wd[0]:
                                    xy.append(1)
                                elif '下' in wd[0]:
                                    xy.append(scH-1)
                                else:
                                    xy = []
                                break
                            pc = 1
                            if '左' in wd[0]:
                                xy.append(1)
                            elif '右' in wd[0]:
                                xy.append(scW-1)
                            else:
                                pc = 0
                                xy.append(pyautogui.position()[0])
                            if '上' in wd[0]:
                                xy.append(1)
                                break
                            elif '下' in wd[0]:
                                xy.append(scH-1)
                                break
                            if pc and (len(xy) == 1):
                                xy.append(pyautogui.position()[1])
                                break
                    if len(xy) == 2:
                        break
                    xy = []
            if len(xy) != 2:
                return 1, []
            dur = self.__extracting_T(cktree)
            return 0, ops + xy + [dur, 0, 0, 0, '']
        elif (ops[0] == 0) and (ops[1] in [1, 3]):
            xy = []
            for tag in cktree.subtrees():
                if tag.label() == 'CDF':
                    rel = []
                    for Purestream in cktree.subtrees():
                        if Purestream.label() == 'CD':
                            neg = 0
                            for ps in Purestream:
                                if ps[0] == '-':
                                    neg = 1
                                    continue
                                if ps[0].isdigit():
                                    if neg:
                                        rel.append(-int(ps[0]))
                                        neg = 0
                                    else:
                                        rel.append(int(ps[0]))
                                    continue
                                if ps[1] == 'm':
                                    if '点' in ps[0]:
                                        rel = [50]
                                        break
                                    elif '些' in ps[0]:
                                        rel = [200]
                                        break
                                    elif '少许' in wd[0]:
                                        rel = [100]
                                        break
                            if len(rel) in [1, 2]:
                                break
                            rel = []
                    if len(rel) not in [1, 2]:
                        rel = [10]
                    for wd in tag:
                        if wd[1] in ['f', 'm']:
                            pc = 1
                            if '左' in wd[0]:
                                xy.append(-rel[0])
                            elif '右' in wd[0]:
                                xy.append(rel[0])
                            else:
                                pc = 0
                                xy.append(0)
                            if '上' in wd[0]:
                                if len(rel) == 2:
                                    xy.append(-rel[1])
                                else:
                                    xy.append(-rel[0])
                            elif '下' in wd[0]:
                                if len(rel) == 2:
                                    xy.append(rel[1])
                                else:
                                    xy.append(rel[0])
                            if pc and (len(xy) == 1):
                                xy.append(0)
                            break
                    if len(xy) == 2:
                        break
                    xy = []
            if len(xy) != 2:
                for tag in cktree.subtrees():
                    if tag.label() == 'CD':
                        neg = 0
                        for wd in tag:
                            if wd[0] == '-':
                                neg = 1
                                continue
                            if wd[0].isdigit():
                                if neg:
                                    xy.append(-int(wd[0]))
                                    neg = 0
                                else:
                                    xy.append(int(wd[0]))
                        if len(xy) == 2:
                            break
                        xy = []
            if len(xy) != 2:
                return 1, []
            dur = self.__extracting_T(cktree)
            return 0, ops + xy + [dur, 0, 0, 0, '']
        if (ops[0] == 1) and (ops[1] in [1, 2]):
            for tag in cktree.subtrees():
                if tag.label() == 'VCX':
                    btn = 0
                    if tag[0][1] == 'f':
                        if '左' in tag[0][0]:
                            btn = 0
                        elif '中' in tag[0][0]:
                            btn = 1
                        elif '右' in tag[0][0]:
                            btn = 2
                    else:
                        btn = {'vcl':0, 'vcm':1, 'vcr':2}.get(tag[0][1])
                    if btn == None:
                        btn = 0
                    return 0, ops + [0, 0, 0, 0, 0, btn, '']
            return 1, []
        if (ops[0] == 1) and (ops[1] == 3):
            ck = None
            for tag in cktree.subtrees():
                if tag.label() == 'CK':
                    ck = None
                    neg = 0
                    for wd in tag:
                        if wd[0] == '-':
                            neg = 1
                        if wd[0].isdigit():
                            if neg:
                                ck = -int(wd[0])
                            else:
                                ck = int(wd[0])
                            break
                        if wd[1] == 'm':
                            if '点' in wd[0]:
                                ck = 10
                                break
                            elif '些' in wd[0]:
                                ck = 25
                                break
                            elif '少许' in wd[0]:
                                ck = 20
                    if ck != None:
                        break
            if ck == 0:
                ck = 1
            if ck == None:
                ck = 5
            for tag in cktree.subtrees():
                if tag.label() == 'F':
                    for wd in tag:
                        if wd[1] == 'f':
                            if '上' in wd[0]:
                                ck = -ck
                                break
                            elif '下' in wd[0]:
                                break
            return 0, ops + [0, 0, 0, ck, 0, 0, '']
        if (ops[0] == 1) and (ops[1] == 0):
            btn = None
            ck = None
            for tag in cktree.subtrees():
                if tag.label() == 'VCX':
                    for wd in tag:
                        if wd[1] == 'vcl':
                            btn = 0
                            break
                        if wd[1] == 'vcm':
                            btn = 1
                            break
                        if wd[1] == 'vcr':
                            btn = 2
                            break
                        if wd[1] == 'f':
                            if '左' in wd[0]:
                                btn = 0
                                break
                            if '中' in wd[0]:
                                btn = 1
                                break
                            if '右' in wd[0]:
                                btn = 2
                                break
                    if btn != None:
                        break
            if btn == None:
                btn = 0
            for tag in cktree.subtrees():
                if tag.label() == 'VCT':
                    ck = 2
                    break
                if tag.label() == 'CK':
                    for wd in tag:
                        if wd[0].isdigit():
                            ck = int(wd[0])
                            break
                    if ck != None:
                        break
            if ck == None:
                ck = 1
            inv = self.__extracting_T(cktree, 0)
            return 0, ops + [0, 0, 0, ck, inv, btn, '']
    def __extracting_T(self, cktree, tp = 1): #tp:1 dur | 0 inv
        pt = -1
        for tag in cktree.subtrees():
            if tag.label() == 'T':
                for wd in tag:
                    if wd[1] == 't':
                        if wd[0] in ['慢慢', '缓缓', '缓慢']:
                            if tp:
                                pt = 5
                            else:
                                pt = 2
                        else:
                            if tp:
                                pt = 0
                            else:
                                pt = 0.1
                        break
                    if pt < 0:
                        if wd[0].isdigit():
                            pt = float(wd[0])
                        continue
                    else:
                        if wd[1] in ['m', 'q']:
                            if wd[0].isdigit():
                                continue
                            unit = {'分钟':60,'秒':1,'分秒':0.1,'厘秒':0.01,'毫秒':0.001}.get(wd[0])
                            if unit == None:
                                continue
                            else:
                                pt *= unit
                                break
                if pt >= 0:
                    break
        if pt < 0:
            if tp:
                pt = 0
            else:
                pt = 0.1
        return pt
        
class ME_ie_chunking:
    def __init__(self):
        self.grammer = ['''
                        CD:
                            {<v|p>?<ns>?<x>+?<m><x>+?<m>}
                        T:
                            {<m><n><f>}
                            {<v|vd|p|n>?<m><x>*?<m|q>}
                            {<t>}
                        CDF:
                            {<v|p>?<n>?<f>}
                        ''',
                        '''
                        CD:
                            {<x>+?<m><x>+?<m>}
                            {<x>+?<m>}
                        T:
                            {<m><n><f>}
                            {<v|vd|p|n>?<m><x>*?<m|q>}
                            {<t>}
                        CDF:
                            {<p><f|m>}
                        CD:
                            {<m>}
                        ''',
                        '''
                        CD:
                            {<v|p>?<ns>?<x>+?<m><x>+?<m>}
                        T:
                            {<m><n><f>}
                            {<v|vd|p|n>?<m><x>*?<m|q>}
                            {<t>}
                        CDF:
                            {<v|p>?<n>?<f>}
                        ''',
                        '''
                        CD:
                            {<x>+?<m><x>+?<m>}
                        T:
                            {<m>+?<n>}
                            {<m><n><f>}
                            {<v|vd|p|n>?<m><x>*?<m|q>}
                            {<t>}
                        CDF:
                            {<p><f|m>}
                            {<f>}
                        CD:
                            {<x>+?<m>}
                        CD:
                            {<m>}
                        ''',
                        '''
                        VCX:
                            {<v>*?<f>}
                            {<vcl|vcm|vcr>}
                        VC:{<v>}
                        VCT:{<vct>}
                        CK:{<m><x>*?<q>}
                        T:
                            {<n><x>*?<m><x>*?<m|q>}
                            {<t>}
                        ''',
                        '''
                        VCX:
                            {<f>}
                            {<vcl|vcm|vcr>}
                        ''',
                        '''
                        VCX:
                            {<f>}
                            {<vcl|vcm|vcr>}
                        ''',
                        '''
                        F:{<p><f>}
                        CK:
                            {<x>*?<m><x>*?<n|v|q>}
                            {<m>}
                        ''']
        '''
        CD 坐标 1234
        CDF 坐标方位 1234
        T 耗时 1234
        VC 点击 5
        VCT 双击 5
        VCX 键位 567
        CK 次数 58
        T 间隔 5
        F 方向 8
        '''
        self.cp = nltk.RegexpParser(self.grammer[0])
        self.cur = 0
    def sel(self, i):
        try:
            i = int(i)
            if i < 0 or i > 7:
                return 1
            if i == self.cur:
                return 0
            self.cp = nltk.RegexpParser(self.grammer[i])
            self.cur = i
            return 0
        except:
            return 1
    def chunking(self, pos_sent, cfy = 0):
        if self.sel(cfy):
            return 1, None
        return 0, self.cp.parse(pos_sent)
if __name__ == '__main__':
    
    print('[ops1, ops2, int(x), int(y), float(duration), int(clicks), float(interval), int(button), \'\']')
    '''
    ie = ME_ie()
    ie.ielist(['鼠标用10毫秒移动到左上角'],[0])
    ie.ielist(['鼠标慢慢移动到右下角'],[0])
    ie.ielist(['鼠标移动到右边，花2分秒'],[0])
    ie.ielist(['鼠标向右移动-200'],[1])
    ie.ielist(['鼠标向上移动-200'],[1])
    ie.ielist(['鼠标向左上移动500'],[1])
    ie.ielist(['鼠标2秒向左下移动500 -200'],[1])
    
    ie.ie('按下右键',5)
    ie.ie('鼠标点击右键 8 次，每次间隙2秒',4)
    print(ie.ie('鼠标向上移动一点',1))
    print(ie.ie('指针2秒内朝下相对拖动 251',3))
    print(ie.ie('箭头相对拖动 -90 146，消耗1秒',3))
    print(ie.ie('箭头花1秒相对拖动 166 141',3))
    '''
    ie = ME_ie()
    tc = ME_tc()
    print('滚轮转动-299圈')
    print(ie.ie('滚轮转动-299圈',7))
    print(tc.tc(['滚轮转动-299圈']))
    vmc = Voicer_ME_NLPcore()
    print(vmc.text_processing(['滚轮转动-299圈']))
    #print(vmc.text_processing(['箭头相对拖动 -90 146，消耗1秒','鼠标用10毫秒移动到左上角','','你好','鼠标移动']))