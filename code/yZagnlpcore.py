# -*- coding: utf-8 -*-
"""
Welcome to Noah's Ark
"""

from yZnlp_tc import NLP_SVM_ArkKernel
from yZnlp_ie import NLP_LEXER_ArkKernel

class NLP_EGG():
    def __init__(self):
        self.yolk = NLP_YOLK() #信息抽取器  Information Extraction
        self.albumen = NLP_ALBUMEN() #文本分类器  Text Categorization
        '''
        self.albumen.TC(text_list) #categorize()
            分类器TC：输入文本列表，对列表中每个文本进行分类[0~15]
            Args:
                text_list (list[String])
            Return:
                ec        (int)         错误码
                y         (list[int])   预测列表
                errors    (list[int])   分类失败的行号
        self.yolk.IE(text, datalist) #extract()
            抽取器IE：输入文本和起始类别，返回参数列表
            Args:
                text      (String)
                datalist  (list[...])   (len(datalist) == 2)
                    #[ops1, ops2]
            Return:
                ec        (int)         错误码
                datalist  (list[...])   (len(datalist) == 9)
                    #[ops1, ops2, int(x), int(y), float(duration), int(clicks), float(interval), int(button), '']
        '''
    def reboot(self): #重启
        self.yolk = NLP_YOLK()
        self.albumen = NLP_ALBUMEN()
    def text_processing(self, text_list): #文本处理主函数
        '''
        Return:
            ec                  (int)     错误码
            treatment_result    (list)    处理结果
            errors              (list)    解析失败数
        '''
        try:
            ec, y, errors_c = self.albumen.TC(text_list)
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
        if y>15 or y<0:
            return 411, []
        datalist = [[0, 0], [0, 1], [0, 2], [0, 3], 
                    [1, 0], [1, 1], [1, 2], [1, 3], 
                    [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], 
                    [3, 0], [3, 1], [3, 2]][y]
        #[ops1, ops2, int(x), int(y), float(duration), int(clicks), float(interval), int(button), '']
        try:
            ec, datalist = self.yolk.IE(text, datalist)
            if ec:
                return 808, []
        except:
            return 602, []
        return 0, datalist
    
class NLP_ALBUMEN(): #分类器集
    def __init__(self, c=0):
        '''
         0        SVM                        NLP_SVM_ArkKernel()
         n        External_Loading           Unknown()     
         (n < 4) == True
        '''
        self.TC_type = 0 #类型
        self.TC_list = [NLP_SVM_ArkKernel()] #列表
        self.TC = self.TC_list[self.TC_type].categorize
        self.TC_name = ['core_SVM', 'Extension1', 'Extension2', 'Extension3']
    def TC_select(self, snow): #TC选取
        if type(snow) != int:
            return 999
        if snow >= len(self.TC_list) or snow < 0:
            return 807
        try:
            self.TC = self.TC_list[snow].categorize
        except:
            self.TC = self.TC_list[self.TC_type].categorize
            return 604
        self.TC_type = snow
        return 0
    def TC_load(self, tc, name=None): #载入扩展TC
        if len(self.TC_list) >= 4:
            return 603
        self.TC_list.append(tc)
        if name != None:
            self.TC_name[len(self.TC_list)-1] = name
        return 0
    
class NLP_YOLK(): #参数提取方法集
    def __init__(self ,s=0):
        '''
         0        lexer_jieba
         n        External_Loading
         (n < 4) == True
        '''
        self.IE_type = s #类型
        self.IE_list = [NLP_LEXER_ArkKernel()] #列表
        self.IE = self.IE_list[self.IE_type].extract
        self.IE_name = ['lexer_jieba', 'Extension1', 'Extension2', 'Extension3']
    def IE_select(self, snow): #IE选取
        if type(snow) != int:
            return 999
        if snow >= len(self.IE_list) or snow < 0:
            return 807
        try:
            self.IE = self.IE_list[snow].extract
        except:
            self.IE = self.IE_list[self.IE_type].extract
            return 604
        self.IE_type = snow
        return 0
    def IE_load(self, ie, name=None): #载入扩展IE
        if len(self.IE_list) >= 4:
            return 603
        self.IE_list.append(ie)
        if name != None:
            self.IE_name[len(self.IE_list)-1] = name
        return 0
    
if __name__ == '__main__':
    from yZagcompile import ProcedurePart
    '''
    text_l = ['指针移动到10 10', '1秒移动过到', '呆呆', '光标移动-10 -10', '鼠标单击', 
              '你好', '敲击键盘y键10次，间隔2秒', '等待一会儿']
    '''
    text_l = ['哈哈哈哈哈，鼠标移动到屏幕中央。', '鼠标拖向坐标 30 358']
    b = NLP_EGG()
    ec, res, err = b.text_processing(text_l)
    print('Input:')
    for i in text_l:
        print(i)
    print('Raise:',ec)
    print('解析失败数:',err)
    for i in res:
        npark = ProcedurePart()
        ec = npark.write_in(i)
        print(i,'      ',npark.translate_procedure())
    #b.text_processing()
    #c = NLP_YOLK()
    #print(c.solution_jieba('光标到左上角',[0,0]))
    #print(c.solution_jieba('光标移动至屏幕左下角',[0,0]))
    #print(c.solution_jieba('光标马上移动到 -348 -128 ，耗时1秒',[0,3]))

