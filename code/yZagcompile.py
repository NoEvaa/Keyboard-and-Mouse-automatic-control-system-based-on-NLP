# -*- coding: utf-8 -*-
"""
Welcome to Noah's Ark
"""

import pyautogui
import time
import copy

from yZaginf import YzDefinition
from yZagerrors import YzErrors

class ProcedurePart:
    def __init__(self, i=3, j=0):
        self.ops_family = i
        self.ops_detail = j
        self.x = 0 #int
        self.y = 0 #int
        self.duration = 0.0 #float>=0
        self.clicks = 0 #int>=0
        self.interval = 0.0 #float>=0
        self.button = 0 #0/1/2
        self.text = ''
        '''
        simple_check_data()
        reset_all()
        write_in([])           {写入参数}
        translate_procedure()  {翻译为中文}
        transform_procedure()  {编码为代码}
        excute()               {执行键鼠控制}
        boundary_check(lx,ly)  {边界检查)
        '''
    def simple_check_data(self): #自检-简
        if (self.ops_family not in [0, 1, 2, 3]):
            return 1
        if (self.ops_detail not in [[0,1,2,3],[0,1,2,3],[0,1,2,3,4],[0,1,2]][self.ops_family]):
            return 1
        if (type(self.x) != int) or (type(self.y) != int):
            return 1
        if self.ops_family == 0 and (self.ops_detail in [0, 2]):
            if self.x < 0 or self.y < 0:
                return 1
        if (type(self.duration) != float) or (self.duration < 0):
            return 1
        if (type(self.clicks) != int) or (self.clicks < 0):
            return 1
        if (type(self.interval) != float) or (self.interval < 0):
            return 1
        if self.button not in [0, 1, 2]:
            return 1
        if (type(self.text) != str) and (type(self.text) != list) or (self.text == []):
            return 1
        return 0
    def reset_all(self): #归零
        self.ops_family = 3
        self.ops_detail = 0
        self.x = 0
        self.y = 0
        self.duration = 0.0
        self.clicks = 0
        self.interval = 0.0
        self.button = 0
        self.text = ''
    def write_in(self, noe): #写入
        if len(noe) != 9:
            return 801 #写入输入错误
        try:
            for x in range(8):
                if noe[x] == '':
                    noe[x] = 0
            self.ops_family = int(noe[0])
            self.ops_detail = int(noe[1])
            self.x = int(noe[2])
            self.y = int(noe[3])
            self.duration = float(noe[4])
            self.clicks = int(noe[5])
            self.interval = float(noe[6])
            self.button = int(noe[7])
            if noe[8] == '':
                self.text = noe[8]
            elif noe[0] == 2 and noe[1] == 4:
                if type(noe[8]) == list:
                    self.text = noe[8]
                else:
                    self.text = noe[8].split()
            else:
                if type(noe[8]) == list:
                    self.text = noe[8][0]
                else:
                    if noe[0] == 2 and noe[1] != 0:
                        self.text = noe[8].split()[0]
                    else:
                        self.text = noe[8]
            if self.simple_check_data():
                self.reset_all()
                return 801 #写入参数错误
            return 0
        except:
            self.reset_all()
            return 404 #写入未知错误
    def translate_procedure(self): #翻译为中文
        CmG = ''
        CmG += YzDefinition.ops_family[self.ops_family][1]+' '
        CmG += YzDefinition.ops_detail[self.ops_family][self.ops_detail][1]
        CmG += self.__generate_parameter_tl()        
        return CmG
    def __generate_parameter_tl(self): #translate
        Cuora = ''
        if self.ops_family == 0:
            Cuora += '[坐标 ('+str(self.x)+' '+str(self.y)+')] '+'[耗时 '+str(self.duration)+'秒]'
            return Cuora
        if self.ops_family == 1:
            if self.ops_detail==0 or self.ops_detail==3:
                Cuora += ' [次数 '+str(self.clicks)+']'
                if self.ops_detail==3:
                    return Cuora
                Cuora += ' [单次间隔 '+str(self.interval)+'秒]'
            Cuora += ' ['+['左键','中键','右键'][self.button]+']'
            return Cuora
        if self.ops_family == 2:
            Cuora += ' '+str(self.text)
            if self.ops_detail == 0:
                Cuora += ' [间隔'+str(self.interval)+'秒]'
            elif self.ops_detail == 3:
                Cuora += ' [次数'+str(self.clicks)+']'
                Cuora += ' [单次间隔'+str(self.interval)+'秒]'
            return Cuora
        if self.ops_family == 3:
            if self.ops_detail == 0:
                Cuora += ' '+str(self.duration)+' 秒'
                return Cuora
            if self.ops_detail == 1:
                Cuora += ' '+str(self.clicks)+' 遍'
                return Cuora
            if self.ops_detail == 2:
                return Cuora
        return Cuora
    def transform_procedure(self): #编码为代码
        noe = ''
        noe += YzDefinition.ops_family[self.ops_family][0]+' '
        noe += YzDefinition.ops_detail[self.ops_family][self.ops_detail][0]
        noe += self.__generate_parameter_tf()        
        return noe
    def __generate_parameter_tf(self): #transform
        vaa = ''
        if self.ops_family == 0:
            vaa += ' '+str(self.x)+' '+str(self.y)+' '+str(self.duration)
            return vaa
        if self.ops_family == 1:
            if self.ops_detail==0 or self.ops_detail==3:
                vaa += ' '+str(self.clicks)
                if self.ops_detail==3:
                    return vaa
                vaa += ' '+str(self.interval)
            vaa += ' '+str(self.button)
            return vaa
        if self.ops_family == 2:
            if self.ops_detail==3:
                vaa += ' '+str(self.clicks)
            if self.ops_detail==0 or self.ops_detail==3:
                vaa += ' '+str(self.interval)
            if type(self.text) == list:
                for harry in self.text:
                    vaa += ' '+str(harry)
                return vaa
            vaa += ' '+str(self.text)
            return vaa
        if self.ops_family == 3:
            if self.ops_detail == 0:
                vaa += ' '+str(self.duration)
                return vaa
            if self.ops_detail == 1:
                vaa += ' '+str(self.clicks)
                return vaa
            if self.ops_detail == 2:
                return vaa
        return vaa
    def excute(self): #执行键鼠控制
        if self.ops_family == 0:
            if self.ops_detail == 0:#moveTo
                if self.boundary_check(self.x,self.y):
                    return 805
                pyautogui.moveTo(x=self.x, y=self.y, 
                                 duration=self.duration, tween=pyautogui.linear)
                return 0
            if self.ops_detail == 1:#moveRel
                cMx, cMy = pyautogui.position()
                if self.boundary_check(cMx+self.x,cMy+self.y):
                    return 805
                pyautogui.moveRel(xOffset=self.x, 
                                  yOffset=self.y, 
                                  duration=self.duration, 
                                  tween=pyautogui.linear)
                return 0 
            if self.ops_detail == 2:#dragTo
                if self.boundary_check(self.x,self.y):
                    return 805
                pyautogui.dragTo(x=self.x, y=self.y, 
                                 duration=self.duration, button='left')
                return 0
            if self.ops_detail == 3:#dragRel
                cMx, cMy = pyautogui.position()
                if self.boundary_check(cMx+self.x,cMy+self.y):
                    return 805
                pyautogui.dragRel(xOffset=self.x, 
                                  yOffset=self.y, 
                                  duration=self.duration, 
                                  button='left')
                return 0 
        if self.ops_family == 1:
            if self.ops_detail == 0:#click
                pyautogui.click(clicks=self.clicks, 
                                interval=self.interval, 
                                button=['left', 'middle', 'right'][self.button])
                return 0
            if self.ops_detail == 1:#mouseDown
                pyautogui.mouseDown(button=['left', 'middle', 'right'][self.button])
                return 0
            if self.ops_detail == 2:#mouseUp
                pyautogui.mouseUp(button=['left', 'middle', 'right'][self.button])
                return 0
            if self.ops_detail == 3:#scroll
                pyautogui.scroll(self.clicks)
                return 0
        if self.ops_family == 2:
            if self.ops_detail == 0:#typewrite
                pyautogui.typewrite(self.text, interval=self.interval)
                return 0
            if self.ops_detail == 1:#keyDown
                pyautogui.keyDown(self.text)
                return 0
            if self.ops_detail == 2:#keyUp
                pyautogui.keyUp(self.text)
                return 0
            if self.ops_detail == 3:#press
                pyautogui.press(self.text, presses=self.clicks, interval=self.interval)
                return 0
            if self.ops_detail == 4:#hotkey
                pyautogui.hotkey(*(self.text))
                return 0
        if self.ops_family == 3:
            if self.ops_detail == 0:#sleep
                time.sleep(self.duration)
                return 0
            if self.ops_detail == 1:
                return -self.clicks
            if self.ops_detail == 2:
                return 1
        return 0
    def boundary_check(self, lx, ly): #边界检查
        sw, sh = pyautogui.size()
        if lx<0 or lx>sw or ly<0 or ly>sh:
            return 1
        if (lx in [0, sw]) and (ly in [0, sh]):
            return 1
        return 0

class YzCompile:
    def __init__(self):
        self.procedure_list = []
        self.size = -1
        self.current = -1
        self.undo_pl_record = []
    '''
    @procedure_list操作
     pl_undo()         {撤销}
     pl_append([])     {创建}
     pl_insert(i,[])   {插入}
     pl_pop(i)         {删除}
     pl_update(i,[])   {修改}
     pl_select(i)      {选取}
     pl_reset()        {重置}
     pl_copy(i,[])     {复制}
     pl_cut(i,t)       {剪切}
    @输出方法
     translate_procedure(i) {翻译为可读文本}
     transform_procedure()  {生成代码文本}
    @输入方法
     alys_code(text)        {解析代码文本}
    '''
    def pl_undo(self): #撤销
        try:
            temp = copy.deepcopy(self.procedure_list)
            self.undo()
            self.undo_pl_record = temp
            return 0
        except:
            return 400
    def undo(self): #撤销++
        self.procedure_list = copy.deepcopy(self.undo_pl_record)
        self.size = len(self.procedure_list)-1
    def reco(self): #记录
        self.undo_pl_record = copy.deepcopy(self.procedure_list)
    def pl_append(self, noe, r=1): #新增
        try:
            npark = ProcedurePart()
            ec = npark.write_in(noe)
            if ec:
                return ec
            ec = self.pl_append_(npark, r)
            if ec:
                return ec
            return 0
        except:
            self.undo()
            return 401 #常规创建未知错误
    def pl_append_(self, noe, r=1): #新增++
        try:
            if r:
                self.reco()
            if type(noe) != ProcedurePart:
                return 401
            self.procedure_list.append(noe)
            self.size += 1
            self.current = self.size
            return 0
        except:
            self.undo()
            return 401 #常规创建未知错误
    def pl_insert(self, i, noe, r=1): #插入
        try:
            if i < 0:
                return 101 #常规越界
            if i > self.size:
                return self.pl_append(noe, r)
            if r:
                self.reco()
            npark = ProcedurePart()
            ec = npark.write_in(noe)
            if ec:
                return ec
            self.procedure_list.insert(i,npark)
            self.size += 1
            return 0
        except:
            self.undo()
            return 402 #常规插入未知错误
    def pl_pop(self, i, r=1): #删除
        try:
            if self.pl_select(i):
                return 101
            if r:
                self.reco()
            self.procedure_list.pop(self.current)
            self.size -= 1
            self.current = self.size
            return 0
        except:
            self.undo()
            return 403 #常规删除未知错误
    def pl_update(self, i, noe, r=1): #修改
        try:
            if self.pl_select(i):
                return 101
            if r:
                self.reco()
            ec = self.procedure_list[self.current].write_in(noe)
            if ec:
                self.undo()
                return ec
            return 0
        except:
            self.undo()
            return 406 #常规修改未知错误   
    def pl_select(self, i): #选取
        if (i > self.size) or (i < 0):
            return 101 #常规越界
        self.current = i
        return 0
    def pl_reset(self): #重置
        self.reco()
        self.procedure_list = []
        self.size = -1
        self.current = -1
        return 0
    def pl_copy(self, i, to=[]): #复制
        if self.pl_select(i):
            return 101
        ec = 0
        self.reco()
        try:
            noe = self.procedure_list[self.current]
            for ct in to:
                ec = ct+1
                self.procedure_list.insert(ct,noe)
                self.size += 1
            self.current = self.size
            return 0
        except:
            self.undo()
            return 0-ec
    def pl_cut(self, i, to): #剪切
        if (i > self.size) or (i < 0) or (to < 0):
            return 101
        if i == to:
            return 0
        self.reco()
        try:
            noe = self.procedure_list[i]
            self.procedure_list.insert(to,noe)
            if i > to:
                i += 1
            self.procedure_list.pop(i)
            self.current = self.size
            return 0
        except:
            self.undo()
            return 410
    def translate_procedure(self, i): #翻译为可读文本
        if i>self.size or i<0:
            return ''    
        return self.procedure_list[i].translate_procedure()
    def transform_procedure(self): #生成代码文本
        text = ''
        for noe in self.procedure_list:
            text += noe.transform_procedure()
            text += '\n'         
        return text
    
    def alys_code_core(self, noah): #代码文本解析核
        '''
        ['T', 'M', 'K', 'O'].index()
        [['A', 'R', 'P', 'Q'], 
         ['C', 'D', 'U', 'R'], 
         ['W', 'D', 'U', 'P', 'H'], 
         ['S', 'L', 'P']]
        '''
        try:
            ark = noah.split()
            if len(ark) < 2:
                return 1, []
            temp1 = ['T', 'M', 'K', 'O'].index(ark[0])
            temp2 = [['A', 'R', 'P', 'Q'], 
                     ['C', 'D', 'U', 'R'], 
                     ['W', 'D', 'U', 'P', 'H'], 
                     ['S', 'L', 'P']][temp1].index(ark[1])
            if temp1 == 0:
                return 0, [temp1, temp2, 
                           int(ark[2]), int(ark[3]), 
                           float(ark[4]), 0, 0, 
                           0, '']
            elif temp1 == 1:
                if temp2 == 0:
                    return 0, [temp1, temp2, 
                               0, 0, 
                               0, int(ark[2]), float(ark[3]), 
                               int(ark[4]), '']
                elif temp2 == 1 or temp2 == 2:
                    return 0, [temp1, temp2, 
                               0, 0, 
                               0, 0, 0, 
                               int(ark[2]), '']
                elif temp2 == 3:
                    return 0, [temp1, temp2, 
                               0, 0, 
                               0, int(ark[2]), 0, 
                               0, '']
            elif temp1 == 2:
                if temp2 == 0:
                    Lilith = noah.split(ark[1],1)[-1]
                    return 0, [temp1, temp2, 
                               0, 0, 
                               0, 0, float(ark[2]), 
                               0, Lilith[1:]]
                elif temp2 in [1, 2]:
                    return 0, [temp1, temp2, 
                               0, 0, 
                               0, 0, 0, 
                               0, ark[2]]
                elif temp2 == 3:
                    return 0, [temp1, temp2, 
                               0, 0, 
                               0, int(ark[2]), float(ark[3]), 
                               0, ark[4]]
                elif temp2 == 4:
                    return 0, [temp1, temp2, 
                               0, 0, 
                               0, 0, 0, 
                               0, [x for x in ark[2:]]]
            elif temp1 == 3:
                if temp2 == 0:
                    return 0, [temp1, temp2, 
                                   0, 0, 
                                   float(ark[2]), 0, 0, 
                                   0, '']
                elif temp2 == 1:
                    return 0, [temp1, temp2, 
                               0, 0, 
                               0, int(ark[2]), 0, 
                               0, '']
                elif temp2 == 2:
                    return 0, [temp1, temp2, 
                               0, 0, 
                               0, 0, 0, 
                               0, '']
        except:
            return 405, [] #解析未知错误
        return 1, []
    def alys_code(self, text, ct=0, r=1): #解析代码文本
        try:
            ec, Eve = self.alys_code_core(text)
            if ec:
                if ec == 1:
                    return 806
                return 405
            Adam = ProcedurePart()
            ec = Adam.write_in(Eve)
            if ct:
                return ec, Adam
            ec = self.pl_append_(Adam, r)
            return ec
        except:
            if r:
                self.undo()
            return 405 #解析未知错误
        return 0
    def alys_code_package(self, text): #解析代码长文本
        errorlist = []
        try:
            text = text.split('\n')
            while '' in text:
                text.remove('')
            i = -1
            for noah in text:
                i += 1
                ec = self.alys_code(noah, 0, 0)
                if ec:
                    errorlist.append(i)
                    continue
        except:
            self.undo()
            errorlist.append(i)
            return 405, errorlist #解析未知错误
        return 0, errorlist
    
    def safety_self_checking(self): #自检
        sw, sh = pyautogui.size()
        if self.size == -1:
            return 'LOAD NULL'
        etext = '' #错误反馈文本
        errors_line = []
        i = -1
        cx, cy = int(sw/2), int(sh/2) #默认鼠标从屏幕中央开始
        mc = [] #鼠标按下记录
        kc = [] #键盘按下记录
        loop = -1 #循环
        while(i < self.size):
            i += 1
            tina = self.procedure_list[i]
            if tina.ops_family == 3:
                if tina.ops_detail == 1:
                    if loop != -1:
                        errors_line.append(i)
                        continue
                    loop = tina.clicks
                    continue
                elif tina.ops_detail == 2:
                    if loop == -1:
                        errors_line.append(i)
                        continue
                    loop = -1
                continue
            elif tina.ops_family == 1:
                if tina.ops_detail == 1:
                    if tina.text in mc:
                        errors_line.append(i)
                        continue
                    mc.append(tina.text)
                    continue
                elif tina.ops_detail == 2:
                    if tina.text not in mc:
                        errors_line.append(i)
                        continue
                    mc.remove(tina.text)
                continue
            elif tina.ops_family == 2:
                if tina.ops_detail == 1:
                    if tina.text in kc:
                        errors_line.append(i)
                        continue
                    kc.append(tina.text)
                    continue
                elif tina.ops_detail == 2:
                    if tina.text not in kc:
                        errors_line.append(i)
                        continue
                    kc.remove(tina.text)
                continue
            elif tina.ops_family == 0:
                if tina.ops_detail in [0, 2]:
                    cx, cy = tina.x, tina.y
                elif tina.ops_detail in [1, 3]:
                    cx += tina.x
                    cy += tina.y
                if tina.boundary_check(cx,cy):
                    etext += '第 '+str(i)+' 行模拟中鼠标位置超出屏幕边界\n模拟中止\n'
                    i = -2
                    break
        if errors_line != []:
            etext += '第'
            for xu in errors_line:
                etext += ' '+str(xu)
            etext += '行存在错误\n'
        if i == -2:
            return etext
        if loop != -1:
            etext += '存在未闭合循环\n'
        if mc != []:
            etext += '存在鼠标按键按下未抬起\n'
        if kc != []:
            etext += '存在键盘按键按下未抬起\n'
        return etext
    def carryout_kernel(self, start = -1, end = -1): #执行核
        if start == -1:
            i = 0
        else:
            i = start
        if end == -1:
            end = self.size
        if i<0 or i>end or end>self.size:
            YzErrors().throw_errors(101)
            return 0
        loop_frequence = 0 #循环次数
        loop_record_i = -1 #循环点
        i -= 1
        try:
            while i<end:
                i += 1
                noe = self.procedure_list[i]
                
                if [noe.ops_family, noe.ops_detail] == [3, 1]:
                    if loop_record_i != -1:
                        pyautogui.alert(text='Error:\n存在循环嵌套无法执行',title='Alert')
                        pyautogui.alert(text='执行中止',title='Notice')
                        return 0
                    loop_frequence = noe.clicks-1 #循环r_clicks遍
                    loop_record_i = i #下一行开始循环
                    continue
                if [noe.ops_family, noe.ops_detail] == [3, 2]:
                    if loop_frequence == 0:
                        loop_record_i = -1
                        continue
                    if loop_record_i<0 or loop_frequence<0:
                        YzErrors().throw_errors(408)
                        return 0
                    i = loop_record_i
                    loop_frequence -= 1
                    continue
                if noe.excute():
                    YzErrors().throw_errors(805)
                    pyautogui.alert(text='执行中止',title='Notice')
                    return 0
            if (loop_record_i != -1) or (loop_frequence != 0):
                pyautogui.alert(text='Warning:\n存在无效循环',title='Alert')
                pyautogui.alert(text='执行中止',title='Notice')
                return 0
        except:
            YzErrors().throw_errors(407)
            return 0
        return 1
            
if __name__ == '__main__':     
    b = YzCompile()
    #'''
    print(b.pl_append([0,1,100,200,4,5,6,0,'']))
    print(b.pl_append([0,0,300,400,4,5,6,0,'a b']))
    print(b.pl_append([0,2,400,300,4,5,6,0,'']))
    print(b.pl_append([0,3,200,400,4,5,6,0,'']))
    print(b.pl_append([2,0,2,3,4,5,1,0,'a b']))
    print(b.pl_append([2,4,2,3,4,5,1,0,'a b']))
    print(b.pl_append([2,1,2,3,4,5,1,0,'a b']))
    print(b.pl_append([2,2,2,3,4,5,1,0,'a b']))
    print(b.pl_append([2,3,2,3,4,5,1,0,'a b']))
    print(b.pl_append([3,0,2,3,4,5,1,0,'']))
    print(b.pl_append([3,1,2,3,4,5,1,0,'']))
    print(b.pl_append([3,2,2,3,4,5,1,0,'']))
    print(b.pl_append([1,0,2,3,4,5,1,0,'']))
    print(b.pl_append([1,1,2,3,4,5,1,1,'']))
    print(b.pl_append([1,2,2,3,4,5,1,2,'']))
    print(b.pl_append([1,3,2,3,4,5,1,0,'']))
    print(b.pl_append([0,0,0,0,4,5,1,0,'a b']))
    '''
    text = 'T R 2 2 2.0\nT A 1 1 1.0\nT P 2 2 2.0\nT Q 1 1 1.0\nK W 1.0 a\nK H a b\nK D a\nK U a\nK P 1 1.0 a\nO S 1.0\nO L 2\nO P\nM C 1 1.0 1\nM D 1\nM U 1\nM R 1'
    b.alys_code(text)
    '''
    print()
    print(b.transform_procedure())
    iii = 0
    while(iii<=b.size):
        print(b.translate_procedure(iii))
        iii += 1
    print(b.safety_self_checking())
    '''
    time.sleep(3)
    for i in b.procedure_list:
        i.excute()
    '''