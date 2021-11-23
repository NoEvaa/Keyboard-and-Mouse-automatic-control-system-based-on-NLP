# -*- coding: utf-8 -*-
"""
Welcome to Noah's Ark
"""
import re
class YzTools:
    def in_isdigit(content): #自然数
        if content.isdigit() or content == '':
            return True
        else:
            return False
    def in_isinteger(content): #整数
        if content == '' or content == '-':
            return True
        if content[0] == '-':
            content = content[1:]
        if content.isdigit():
            return True
        else:
            return False
    def in_isdecimal(content): #小数
        if content == '':
            return True
        content = content.replace('.','',1)
        if content.isdigit():
            return True
        else:
            return False
    def isNotValid(content): #非有效文本判断(非中文)
        for ch in content:
            if u'\u4e00' <= ch <= u'\u9fff':
                return False
            return True
    def isfigure(content): #数字字符判断
        return set(content).issubset(set('0123456789.-'))
    def Cn_to_Af(text): #中文数字转阿拉伯数字
        pattrern = "([负]?)([零一二两三四五六七八九千百十万]+)([点]?[零一二三四五六七八九]*)"
        num_mapping = {'零':'0', '一':'1', '两':'2', '二':'2', '三':'3', '四':'4', '五':'5', '六':'6', '七':'7', '八':'8', '九':'9'}
        allfigs = re.findall(pattrern, text)
        for figl in allfigs:
            if figl[0]+figl[1]+figl[2] == '一点':
                continue
            gs = '' #整数
            if len(figl[1]) == 1:
                if figl[1] == '十':
                    gs = '10'
                else:
                    gs = num_mapping.get(figl[1], None)
                    if gs == None:
                        continue
            else:
                fig = figl[1]
                f = fig.split('万', 1)
                if len(f) == 2:
                    fig = f[1]
                    if f[0] != '':
                        fw = f[0]
                        f = fw.split('千', 1)
                        if len(f) == 2:
                            fw = f[1]
                            if len(f[0]) == 1:
                                gs += num_mapping.get(f[0], '0')
                            else:
                                continue
                        else:
                            if gs != '':
                                gs += '0'
                        f = fw.split('百', 1)
                        if len(f) == 2:
                            fw = f[1]
                            if len(f[0]) == 1:
                                gs += num_mapping.get(f[0], '0')
                            else:
                                continue
                        else:
                            if gs != '':
                                gs += '0'
                        f = fw.split('十', 1)
                        if len(f) == 2:
                            fw = f[1]
                            if len(f[0]) == 1:
                                gs += num_mapping.get(f[0], '0')
                            elif len(f[0]) == 0:
                                gs += '1'
                            else:
                                continue
                        else:
                            if gs != '':
                                gs += '0'
                        if len(fw) == 1:
                            gs += num_mapping.get(fw[0], '0')
                        elif len(fw) == 0:
                            gs += '0'
                        else:
                            if gs == '':
                                for f in fw:
                                    gs += num_mapping.get(f, '0')
                            else:
                                gs += num_mapping.get(fw[-1], '0')
                f = fig.split('千', 1)
                if len(f) == 2:
                    fig = f[1]
                    if len(f[0]) == 1:
                        gs += num_mapping.get(f[0], '0')
                    else:
                        continue
                else:
                    if gs != '':
                        gs += '0'
                f = fig.split('百', 1)
                if len(f) == 2:
                    fig = f[1]
                    if len(f[0]) == 1:
                        gs += num_mapping.get(f[0], '0')
                    else:
                        continue
                else:
                    if gs != '':
                        gs += '0'
                f = fig.split('十', 1)
                if len(f) == 2:
                    fig = f[1]
                    if len(f[0]) == 1:
                        gs += num_mapping.get(f[0], '0')
                    elif len(f[0]) == 0:
                        gs += '1'
                    else:
                        continue
                else:
                    if gs != '':
                        gs += '0'
                if len(fig) == 1:
                    gs += num_mapping.get(fig[0], '0')
                elif len(fig) == 0:
                    gs += '0'
                else:
                    if gs == '':
                        for f in fig:
                            gs += num_mapping.get(f, '0')
                    else:
                        gs += num_mapping.get(fig[-1], '0')
            gj = '' #小数
            if figl[2] != '':
                gj = '.'
                for fig in figl[2][1:]:
                    gj += num_mapping.get(fig, '')
            if figl[0] != '':
                gs = '-' + gs #负数
            text = YzTools.replace_sn(text, figl[0]+figl[1]+figl[2], gs+gj)
        return text
    def replace_sn(text, cn, af):
        t = text.split(cn, 1)
        text = t[0] + ' ' + str(af) + ' ' + t[1]
        return text
        
if __name__ == '__main__':
    print(YzTools.Cn_to_Af('负两千零四万三千六百五十点二'))  
    print(YzTools.Cn_to_Af('负一二三四五六七八九'))     
    print(YzTools.Cn_to_Af('鼠标点击十次。'))
    print(YzTools.Cn_to_Af('万三千六百五十点二')) 
    print(YzTools.Cn_to_Af('鼠标向上一点')) 
    