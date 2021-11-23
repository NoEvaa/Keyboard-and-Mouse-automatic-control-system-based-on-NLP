# -*- coding: utf-8 -*-
"""
Welcome to Noah's Ark
"""
import pickle
import jieba
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from yZagtools import YzTools

jieba.load_userdict("models\\u_dict.txt")

class NLP_SVM_ArkKernel():
    def __init__(self):
        self.model_BOW = None
        self.model_SVM = None
    def __check_models(self):
        if self.model_BOW == None or self.model_SVM == None:
            return True
        return False
    def __load_models(self):
        path = "models/simply_svm/"
        try:
            with open(path+"classifier.pkl", 'rb') as fw:
                self.model_SVM = pickle.load(fw)
            self.model_BOW = CountVectorizer(token_pattern=r"(?u)\b\w+\b", 
                                             decode_error="replace", 
                                             vocabulary=pickle.load(open(path+"feature.pkl", "rb")))
            return 0
        except:
            return 807
    def categorize(self, text_list=[]): #SVM快速分类
        if self.__check_models():
            if self.__load_models():
                return 807, [], []
        try:
            ec, X, errors = self.__text_pretreatment(text_list)
            if ec:
                return ec, [], []
            return 0, self.model_SVM.predict(X), errors
        except:
            return 411, [], []
    def __text_pretreatment(self, text_list): #文本预处理
        if text_list == []:
            return 411, [], []
        split_corpus = []
        for text in text_list:
            temp = jieba.lcut(text)
            i = 0
            while(i<len(temp)):
                if YzTools.isNotValid(temp[i]):
                    del temp[i]
                    continue
                i += 1
            split_corpus.append( " ".join(temp) )
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
    
if __name__ == '__main__':
    b = NLP_SVM_ArkKernel()
    print(b.categorize(['指针移动到10 10', '指针移动10 10', '指针移动10 10', '你好', '敲击键盘z 5遍', '中键', '鼠标左键6遍']))
    
