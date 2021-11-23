# -*- coding: utf-8 -*-
"""
Welcome to Noah's Ark
"""
import jieba
import jieba.analyse
import jieba.posseg
import random

from yZagtools import YzTools

jieba.load_userdict("models\\u_dict.txt")

class NLP_LEXER_ArkKernel():
    def extract(self, text, datalist):
        sentence_seged = jieba.posseg.cut(text.strip())
        items = []
        for x in sentence_seged:
            items.append([x.word,x.flag])
        return self.lexical_analysis_jieba_posseg(items, datalist)
    def lexical_analysis_jieba_posseg(self, items, datalist):
        if items == []:
            return 1, datalist + [1, 1, 1, 1, 1, 1, 'a']
        Lappland = []
        if datalist[0] == 0:
            c = False
            temp_x, temp_y = '1', '1'
            tim = 0
            for i in range(len(items)):
                if items[i][0].isdigit():
                    temp_x = items[i][0]
                    if datalist[1] in [1, 3]:
                        j = i
                        while j>0:
                            j -= 1
                            if items[j][0] == '-':
                                temp_x = '-' + temp_x
                                break
                            if items[j][1] != 'x':
                                break
                    while i < len(items):
                        i += 1
                        if items[i][0].isdigit():
                            temp_y = items[i][0]
                            c = True
                            break
                        if items[i][1] != 'x':
                            break
                    if c:
                        if datalist[1] in [1, 3]:
                            while i>j:
                                i -= 1
                                if items[i][0] == '-':
                                    temp_y = '-' + temp_y
                                    break
                                if items[i][1] != 'x':
                                    break
                        break
            if c:
                for i in range(len(items)):
                    if items[i][0] == '秒':
                        while i>0:
                            i -= 1
                            if YzTools.isfigure(items[i][0]):
                                tim = items[i][0]
                                break
                            if items[i][1] != 'x':
                                break
                        if tim != 0:
                            break
                Lappland = [int(temp_x), int(temp_y), float(tim), 0, 0, 0, '']
                return 0, datalist + Lappland
            
        elif datalist[0] == 1:
            if datalist[1] == 0: #10
                if len(items) == 1:
                    temp = {'单击':[0, 0, 0, 1, 0, 0, ''], 
                            '双击':[0, 0, 0, 2, 0, 0, ''], 
                            '右键':[0, 0, 0, 1, 0, 2, ''], 
                            '中击':[0, 0, 0, 1, 0, 1, ''], 
                            '左键':[0, 0, 0, 1, 0, 0, ''], 
                            '点击':[0, 0, 0, 1, 0, 0, '']}.get(items[0][0])
                    if type(temp) != type(None):
                        Lappland = temp
                        return 0, datalist + Lappland
                else:
                    clicks = '1'
                    button = '0'
                    tim = 0
                    c = False
                    for i in items:
                        if not c and ('双击' in i[0]):
                            clicks = '2'
                            c = True
                        if '左' in i[0]:
                            button = '0'
                        if '中' in i[0]:
                            button = '1'
                        if '右' in i[0]:
                            button = '2'
                    for i in range(len(items)):
                        if c:
                            break
                        if items[i][0] in ['次', '遍']:
                            while i>0:
                                i -= 1
                                if items[i][0].isdigit():
                                    clicks = items[i][0]
                                    c = True
                                    break
                                if items[i][0] == '秒' or items[i][1] == 'v':
                                    break
                    for i in range(len(items)):
                        if items[i][0] == '秒':
                            while i>0:
                                i -= 1
                                if YzTools.isfigure(items[i][0]):
                                    tim = items[i][0]
                                    break
                                if items[i][1] != 'x':
                                    break
                            if tim != 0:
                                break
                    Lappland = [0, 0, 0, int(clicks), float(tim), int(button), '']
                    return 0, datalist + Lappland
                    
            elif datalist[1] in [1, 2]: #11 12
                for i in items:
                    if '左' in i[0]:
                        Lappland = [0, 0, 0, 0, 0, 0, '']
                        return 0, datalist + Lappland
                    if '中' in i[0]:
                        Lappland = [0, 0, 0, 0, 0, 1, '']
                        return 0, datalist + Lappland
                    if '右' in i[0]:
                        Lappland = [0, 0, 0, 0, 0, 2, '']
                        return 0, datalist + Lappland
            elif datalist[1] == 3: #13
                c = True
                clicks = '0'
                for i in range(len(items)):
                    if items[i][0].isdigit():
                        clicks = items[i][0]
                        c = False
                        while i > 0:
                            i -= 1
                            if items[i][1] != 'x':
                                break
                            if items[i][0] == '-':
                                clicks = '-'+clicks
                                break
                        break
                temp = []
                if c:
                    for i in range(len(items)):
                        if items[i][1] == 'm':
                            temp.append(items[i][0])
                            continue
                    if set(temp).issubset(set(['一点', '一点儿'])):
                        clicks = '50'
                if clicks != '0':
                    for i in items:
                        if '上' in i[0]:
                            if '-' in clicks:
                                clicks = clicks[1:]
                            else:
                                clicks = '-'+clicks
                            break
                    Lappland = [0, 0, 0, int(clicks), 0, 0, '']
                    return 0, datalist + Lappland
            
        elif datalist[0] == 2:
            if datalist[1] == 0: #20
                text = ''
                tim = 0
                for i in items:
                    if i[0].encode().isalpha():
                        text = i[0]
                for i in range(len(items)):
                    if items[i][0] == '秒':
                        while i>0:
                            i -= 1
                            if YzTools.isfigure(items[i][0]):
                                tim = items[i][0]
                                break
                            if items[i][1] != 'x':
                                break
                        if tim != 0:
                            break
                if text != '':
                    Lappland = [0, 0, 0, 0, float(tim), 0, text]
                    return 0, datalist + Lappland
            elif datalist[1] in [1, 2]: #21 22
                for i in items:
                    if i[0].encode().isalpha():
                        Lappland = [0, 0, 0, 0, 0, 0, i[0]]
                        return 0, datalist + Lappland
            elif datalist[1] == 3: #23
                text = ''
                tim = 0
                clicks = '1'
                for i in items:
                    if i[0].encode().isalpha():
                        text = i[0]
                for i in range(len(items)):
                    c = False
                    if items[i][0] in ['次', '遍']:
                        while i>0:
                            i -= 1
                            if items[i][0].isdigit():
                                clicks = items[i][0]
                                c = True
                                break
                            if items[i][0] == '秒' or items[i][1] == 'v':
                                break
                        if c:
                            break
                for i in range(len(items)):
                    if items[i][0] == '秒':
                        while i>0:
                            i -= 1
                            if YzTools.isfigure(items[i][0]):
                                tim = items[i][0]
                                break
                            if items[i][1] != 'x':
                                break
                        if tim != 0:
                            break
                if text != '':
                    Lappland = [0, 0, 0, int(clicks), float(tim), 0, text]
                    return 0, datalist + Lappland
            elif datalist[1] == 4: #24
                temp = []
                for i in items:
                    if i[0].encode().isalpha():
                        temp.append(i[0])
                if temp != []:
                    Lappland = [0, 0, 0, 0, 0, 0, temp]
                    return 0, datalist + Lappland
        
        elif datalist[0] == 3:
            if datalist[1] == 0: # 30
                temp = []
                temp_pos = []
                for i in range(len(items)):
                    if YzTools.isfigure(items[i][0]):
                        temp.append(items[i][0])
                        temp_pos.append(items[i][1])
                        continue
                    if items[i][1] == 'm':
                        temp.append(items[i][0])
                        temp_pos.append(items[i][1])
                        continue
                    if items[i][0] == '秒':
                        temp.append(items[i][0])
                        temp_pos.append(items[i][1])
                #print(temp, temp_pos)
                while '秒' in temp:
                    index = temp.index('秒')
                    del temp[index], temp_pos[index]
                    while index > 0:
                        index -= 1
                        if YzTools.isfigure(temp[index]):
                            Lappland = [0, 0, float(temp[index]), 0, 0, 0, '']
                            return 0, datalist + Lappland
                if set(temp).issubset(set(['一会', '一会儿'])):
                    Lappland = [0, 0, float(random.randint(1,5)), 0, 0, 0, '']
                    return 0, datalist + Lappland
            elif datalist[1] == 1: #31
                for i in range(len(items)):
                    #if items[i][1] == 'm':
                    if YzTools.isfigure(items[i][0]):
                        if items[i][0].isdigit():
                            Lappland = [0, 0, 0, int(items[i][0]), 0, 0, '']
                            return 0, datalist + Lappland
            elif datalist[1] == 2: #32
                Lappland = [0, 0, 0, 0, 0, 0, '']
                return 0, datalist + Lappland
        
        if Lappland == []:
            return 1, datalist + [1, 1, 1, 1, 1, 1, 'a']
        return 0, datalist + Lappland
    
if __name__ == '__main__':
    b = NLP_LEXER_ArkKernel()
    
