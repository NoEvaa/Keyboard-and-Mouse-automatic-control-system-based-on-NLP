# -*- coding: utf-8 -*-
"""
Welcome to Noah's Ark
"""
import tkinter as tk
from tkinter import scrolledtext, StringVar, ttk, filedialog
import pyautogui
import time

from yZagtools import YzTools
from yZaginf import YzInputSpecification
from yZagcompile import YzCompile
from yZagerrors import YzErrors

class YzBaseGui: #主界面
    elem = []
    '''
      # StringVar() | Bt Button | Et Entry | Cb Combobox | St ScrolledText #
        [0screenW, 1screenH, 2Bt[更新],
         3Bt[新增], 4Bt[插入], 5Bt[修改], 6Bt[删除],
         7Bt[检验], 8Bt[执行], 9Et[行],
         10mode, 11Cb[类], 12oper, 13Cb[种],
         14Et[x], 15Et[y], 
         16Et[duration], 17Et[clicks], 18Et[interval],
         19Cb[button], 20Et[text], 21St[scr]]
    '''
    def __init__(self, parent):
        self.master = parent
        self.__create_parts()
    def __create_parts(self):
        #用户操作面板
        self.frame = tk.Frame(self.master)
        
        self.elem.append(StringVar()) #0 screenW
        self.elem.append(StringVar()) #1 screenH
        self.elem.append(tk.Button(self.frame,text='更新',justify=tk.LEFT)) #2
        tk.Label(self.frame,text='当前屏幕分辨率：').grid(row=0,column=0,padx=0,pady=5)
        self.elem[2].grid(row=0,column=1,padx=5)
        tk.Label(self.frame,textvariable=self.elem[0]).grid(row=1,column=0,padx=3,pady=3)
        tk.Label(self.frame,textvariable=self.elem[1]).grid(row=2,column=0,padx=3,pady=3)
        
        self.elem.append(tk.Button(self.frame,text='新增',justify=tk.LEFT)) #3
        self.elem.append(tk.Button(self.frame,text='插入',justify=tk.LEFT)) #4
        self.elem.append(tk.Button(self.frame,text='修改',justify=tk.LEFT)) #5
        self.elem.append(tk.Button(self.frame,text='删除',justify=tk.LEFT)) #6
        tk.Label(self.frame,text='行操作：').grid(row=6,column=0,padx=5,pady=15)
        self.elem[3].grid(row=6,column=1,padx=3)
        self.elem[4].grid(row=6,column=2,padx=3)
        self.elem[5].grid(row=6,column=3,padx=3)
        self.elem[6].grid(row=6,column=4,padx=3)
        
        self.elem.append(tk.Button(self.frame,text='检验',justify=tk.LEFT)) #7
        self.elem.append(tk.Button(self.frame,text='执行',justify=tk.LEFT)) #8
        tk.Label(self.frame,text='编译操作：').grid(row=4,column=0,padx=5,pady=15)
        self.elem[7].grid(row=4,column=1,padx=3)
        self.elem[8].grid(row=4,column=2,padx=3)
        tk.Label(self.frame,text='---------------------------').grid(row=5,column=0,columnspan=3,padx=5,pady=5)
        
        digit_limit = self.master.register(YzTools.in_isdigit) #自然数限定
        integer_limit = self.master.register(YzTools.in_isinteger) #整数限定
        decimal_limit = self.master.register(YzTools.in_isdecimal) #正小数限定
        
        tk.Label(self.frame,text='目标行').grid(row=7,column=0,padx=5,pady=5)
        self.elem.append(tk.Entry(self.frame,bd=2,relief=tk.RIDGE,bg='lightyellow',width=10,
                                 textvariable=StringVar(),validate='key',validatecommand=(digit_limit,'%P'))) #9
        self.elem[9].grid(row=7,column=1,columnspan=4,padx=5,pady=5)
        
        self.elem.append(StringVar()) #10 mode
        self.elem.append(ttk.Combobox(self.frame,width=12,textvariable=self.elem[10],state='readonly')) #11 modeChosen
        self.elem.append(StringVar()) #12 oper
        self.elem.append(ttk.Combobox(self.frame,width=12,textvariable=self.elem[12],state='readonly')) #13 operChosen
        tk.Label(self.frame,text='操作类').grid(row=8,column=0,padx=5,pady=5)
        self.elem[11]['values'] = ('光标', '鼠标', '键盘', '特殊')
        self.elem[11].grid(row=8,column=1,columnspan=4,padx=5,pady=5)
        self.elem[11].current(3)
        tk.Label(self.frame,text='操作种').grid(row=9,column=0,padx=5,pady=5)
        self.elem[13]['values'] = ('暂停', '循环', '循环反复')
        self.elem[13].grid(row=9,column=1,columnspan=4,padx=5,pady=5)
        self.elem[13].current(0)
        self.elem[11].bind('<<ComboboxSelected>>',self.mode_choice)
        self.elem[13].bind('<<ComboboxSelected>>',self.oper_choice)

        self.elem.append(tk.Entry(self.frame,bd=1,relief=tk.RIDGE,bg='lightcyan',width=10,
                                 textvariable=StringVar(),validate='key',validatecommand=(integer_limit,'%P'))) #14 x
        self.elem.append(tk.Entry(self.frame,bd=1,relief=tk.RIDGE,bg='lightcyan',width=10,
                                 textvariable=StringVar(),validate='key',validatecommand=(integer_limit,'%P'))) #15 y
        self.elem.append(tk.Entry(self.frame,bd=1,relief=tk.RIDGE,bg='lightcyan',width=12,
                                 textvariable=StringVar(),validate='key',validatecommand=(decimal_limit,'%P'))) #16 duration
        self.elem.append(tk.Entry(self.frame,bd=1,relief=tk.RIDGE,bg='lightcyan',width=12,
                                 textvariable=StringVar(),validate='key',validatecommand=(digit_limit,'%P'))) #17 clicks
        self.elem.append(tk.Entry(self.frame,bd=1,relief=tk.RIDGE,bg='lightcyan',width=12,
                                 textvariable=StringVar(),validate='key',validatecommand=(decimal_limit,'%P'))) #18 interval
        self.elem.append(ttk.Combobox(self.frame,width=8,textvariable=StringVar(),state='readonly')) #19 buttonChosen
        self.elem.append(tk.Entry(self.frame,bd=3,relief=tk.SUNKEN,bg='GhostWhite',width=20,textvariable=StringVar())) #20 text
        
        tk.Label(self.frame,text='坐标').grid(row=10,column=0,padx=5,pady=5)
        tk.Label(self.frame,text='x').grid(row=10,column=1,padx=1,pady=5)
        self.elem[14].grid(row=10,column=2,columnspan=3,padx=1,pady=5)
        tk.Label(self.frame,text='y').grid(row=11,column=1,padx=1,pady=5)
        self.elem[15].grid(row=11,column=2,columnspan=3,padx=1,pady=5)
        tk.Label(self.frame,text='耗时/秒').grid(row=12,column=0,padx=5,pady=5)
        self.elem[16].grid(row=12,column=1,columnspan=3,padx=1,pady=5)
        tk.Label(self.frame,text='次数/次').grid(row=13,column=0,padx=5,pady=5)
        self.elem[17].grid(row=13,column=1,columnspan=3,padx=1,pady=5)
        tk.Label(self.frame,text='间隔/秒').grid(row=14,column=0,padx=5,pady=5)
        self.elem[18].grid(row=14,column=1,columnspan=3,padx=1,pady=5)
        tk.Label(self.frame,text='键位').grid(row=15,column=0,padx=5,pady=5)
        self.elem[19]['values'] = ('左键', '中键', '右键')
        self.elem[19].grid(row=15,column=1,columnspan=3,padx=5,pady=5)
        self.elem[19].current(0)
        tk.Label(self.frame,text='文本').grid(row=16,column=0,padx=5,pady=5)
        self.elem[20].grid(row=16,column=1,columnspan=5,padx=1,pady=5)
        
        self.frame.pack(padx=20,pady=10,side=tk.RIGHT,fill='y',expand=1)
        self.__input_disable(3,0)
        #显示面板
        self.elem.append(scrolledtext.ScrolledText(self.master,wrap=tk.WORD,state=tk.DISABLED)) #21 scr
        self.elem[21].pack(padx=20,pady=12,side=tk.LEFT,expand=1,fill=tk.BOTH)
        
    def __input_disable(self, t1, t2): #输入禁用
        try:
            Specter = YzInputSpecification.para[t1][t2]
        except:
            return
        for x in range(7):
            self.elem[x+14].configure(state=YzInputSpecification.state[Specter[x]])
    def mode_choice(self, *args):
        case = self.elem[11]['values'].index(self.elem[10].get())
        if case == 0:
            self.elem[13]['values'] = ('移至', '移动', '拖至', '拖动')
            self.elem[13].current(0)
        elif case == 1:
            self.elem[13]['values'] = ('点击', '按下', '抬起', '滚动')
            self.elem[13].current(0)
        elif case == 2:
            self.elem[13]['values'] = ('键入', '按下', '抬起', '敲击', '热键')
            self.elem[13].current(0)
        elif case == 3:
            self.elem[13]['values'] = ('暂停', '循环', '循环反复')
            self.elem[13].current(0) 
        self.__input_disable(case,0)
    def oper_choice(self, *args):
        case1 = self.elem[11]['values'].index(self.elem[10].get())
        case2 = self.elem[13]['values'].index(self.elem[12].get())
        self.__input_disable(case1,case2)

class YzInitialGui(YzBaseGui): #基本功能
    '''
    新增|插入|修改|删除
    更新|刷新|撤销|清空
    检验
    '''
    def __init__(self, parent):
        YzBaseGui.__init__(self, parent)
        
        #self.sW, self.sH = pyautogui.size()
        self.compile = YzCompile() #编译库
        self.updata_WH()
    def b1(self, *args):
        pyautogui.alert(text='请加载扩展模块！',title='Notice')
    def updata_WH(self): #更新屏幕分辨率
        self.sW, self.sH = pyautogui.size() #屏幕分辨率 width,height
        self.elem[0].set('    Width[{:d}]'.format(self.sW))
        self.elem[1].set('    Height[{:d}]'.format(self.sH))
    def generate_parameter_list(self): #生成输入参数列表
        npark = self.__get_info()
        if self.__check_info(npark):
            return 802, []
        return 0, npark
    def __get_info(self): #读取输入参数
        return [self.elem[9].get(), 
                self.elem[11]['values'].index(self.elem[10].get()), 
                self.elem[13]['values'].index(self.elem[12].get()), 
                self.elem[14].get(), self.elem[15].get(), 
                self.elem[16].get(), self.elem[17].get(), self.elem[18].get(), 
                ['左键', '中键', '右键'].index(self.elem[19].get()), 
                self.elem[20].get()]
    def __check_info(self, Lemon): #检查读取内容
        try:
            Scorpio = YzInputSpecification.para[Lemon[1]][Lemon[2]]
        except:
            return 1
        for i in range(7):
            if Scorpio[i] and (Lemon[i+3] == ''):
                return 1
        return 0
    def __scr_delete_std(self, i=0, j=tk.END): #显示-删除规范
        self.elem[21].configure(state=tk.NORMAL)
        if j != tk.END:
            j = float(int(j))
        i = float(int(i))
        self.elem[21].delete(i,j)
        self.elem[21].configure(state=tk.DISABLED)
    def scr_renew(self): #显示-刷新
        try:
            self.__scr_delete_std()
            self.elem[21].configure(state=tk.NORMAL)
            luo = 0
            while(luo<=self.compile.size):
                tianyi = self.compile.translate_procedure(luo)
                self.elem[21].insert(tk.INSERT,'#'+str(luo)+'>> '+tianyi+'\n')
                luo += 1
            self.elem[21].configure(state=tk.DISABLED)
        except:
            YzErrors().throw_errors(413)
    def base_insert(self, para, i='end'): #插入规范
        if i == 'end':
            i = self.compile.size + 1
        ec = self.compile.pl_insert(i, para)
        if ec:
            YzErrors().throw_errors(ec)
            return
    def base_del(self, i='end'): #删除规范
        if i == 'end':
            i = self.compile.size
        ec = self.compile.pl_pop(i)
        if ec:
            YzErrors().throw_errors(ec)
            return
    def bt_append(self, *args): #编辑-新增
        ec, noe = self.generate_parameter_list()
        if ec:
            YzErrors().throw_errors(ec)
            return
        self.base_insert(noe[1:])
        ik = self.compile.translate_procedure(self.compile.current)
        self.elem[21].configure(state=tk.NORMAL)
        self.elem[21].insert(tk.INSERT,'#'+str(self.compile.current)+'>> '+ik+'\n')
        self.elem[21].configure(state=tk.DISABLED)
    def bt_insert(self): #编辑-插入
        ec, noe = self.generate_parameter_list()
        if ec:
            YzErrors().throw_errors(ec)
            return
        if noe[0] == '':
            YzErrors().throw_errors(803)
            return
        noe[0] = int(noe[0])
        self.base_insert(noe[1:], noe[0])
        self.scr_renew()
    def bt_delete(self, *args): #编辑-删除
        pinecone = self.elem[9].get()
        if pinecone == '':
            YzErrors().throw_errors(803)
            return
        pinecone = int(pinecone)
        if pinecone<0:
            YzErrors().throw_errors(101)
            return
        if pinecone>self.compile.size:
            pinecone = self.compile.size
        self.base_del(pinecone)
        self.scr_renew()
    def bt_updata(self): #编辑-修改
        ec, noe = self.generate_parameter_list()
        if ec:
            YzErrors().throw_errors(ec)
            return
        if noe[0] == '':
            YzErrors().throw_errors(803)
            return
        noe[0] = int(noe[0])
        ec = self.compile.pl_update(noe[0], noe[1:])
        if ec:
            YzErrors().throw_errors(ec)
            return
        self.scr_renew()
    def bt_clear(self, *args): #编辑-清空
        ans = pyautogui.confirm(text='确认清空?',title='Notice',buttons=['YES', 'NO'])
        if ans == 'NO':
            return
        if ans == None:
            return
        self.compile.pl_reset()
        self.scr_renew()
    def bt_undo(self, *args): #撤销
        if self.compile.pl_undo():
            YzErrors().throw_errors(401)
        self.scr_renew()
    def simulation_check(self): #检验
        checkresult = self.compile.safety_self_checking()
        if checkresult == '':
            pyautogui.alert(text='完美通过检验~',title='Congratulations')
        else:
            checkresult = 'WARNING:\n'+checkresult
            pyautogui.alert(text=checkresult,title='Alert')
    def get_cursor_xy(self, t=0): #获取光标位置
        time.sleep(t)
        currentMx, currentMy = pyautogui.position()
        return currentMx, currentMy
    def input_cover(self, noe): #输入界面-数据覆盖
        self.elem[11].current(noe.ops_family)
        self.mode_choice()
        self.elem[13].current(noe.ops_detail)
        self.oper_choice()
        self.elem[14].delete(0,tk.END)
        self.elem[14].insert(0,str(noe.x))
        self.elem[15].delete(0,tk.END)
        self.elem[15].insert(0,str(noe.y))
        self.elem[16].delete(0,tk.END)
        self.elem[16].insert(0,str(noe.duration))
        self.elem[17].delete(0,tk.END)
        self.elem[17].insert(0,str(noe.clicks))
        self.elem[18].delete(0,tk.END)
        self.elem[18].insert(0,str(noe.interval))
        self.elem[19].current(noe.button)
        self.elem[20].delete(0,tk.END)
        self.elem[20].insert(0,noe.text)

class YzAdvancedGui(YzInitialGui): #功能扩展
    '''
    快速删除
    复制|快速复制
    剪切|快速剪切
    鼠标定位|鼠标快捷定位
    导出|导入|追加导入
    '''
    def __init__(self, parent):
        YzInitialGui.__init__(self, parent)
    def ql_input_extract(self, NorthMing): #浓缩行参数 
        NorthMing = NorthMing.split()
        if NorthMing == []:
            return 802, []
        Sherry = []
        try:
            Eyjafjalla = len(NorthMing)-1
            Alice = -1
            while Alice < Eyjafjalla:
                Alice += 1
                Yoshinon = NorthMing[Alice]
                if Yoshinon.isdigit():
                    Sherry.append(int(Yoshinon))
                    continue
                else:
                    if ':' not in Yoshinon:
                        return 802, []
                    Pandora = Yoshinon.split(':',1)
                    for Farfalla in Pandora:
                        if not Farfalla.isdigit():
                            return 802, []
                    l, r = int(Pandora[0]), int(Pandora[1])
                    if l>r:
                        return 802, []
                    if r > self.compile.size+1:
                        r = self.compile.size+1
                    for ShiAn in [x for x in range(l,r+1)]:
                        Sherry.append(ShiAn)
            Sherry = list(set(Sherry))
            Sherry.sort(reverse=True)
            Eyjafjalla = len(Sherry)
            Alice = 0
            while Alice < Eyjafjalla:
                if (Sherry[Alice] > self.compile.size+1) or (Sherry[Alice] < 0):
                    del Sherry[Alice]
                    Eyjafjalla -= 1
                    continue
                Alice += 1  
            return 0, Sherry
        except:
            return 999, []
    def __ql_get(self): #选取行
        pinecone = self.elem[9].get()
        if pinecone == '':
            YzErrors().throw_errors(803)
            return -1
        try:
            pinecone = int(pinecone)
            if pinecone < 0:
                YzErrors().throw_errors(101)
                return -1
            if pinecone > self.compile.size:
                pinecone = self.compile.size
        except:
            YzErrors().throw_errors(999)
            return -1
        return pinecone
    def base_del_package(self, Rye): #多项删除
        c = 1
        for r in Rye:
            ec = self.compile.pl_pop(r, c)
            if c:
                c = 0
            if ec:
                self.compile.undo()
                self.scr_renew()
                text = '删除第 '+str(r)+' 行时遇到了错误\n删除中止\n'
                pyautogui.alert(text=text,title='ERROR')
                return
    def quick_delete(self): #快速删除
        NorthMing = pyautogui.prompt(text='请输入需删除第i行[自然数]:\n{如需删除多行,请以空格分隔}',title='Notice',default='')
        if NorthMing == None:
            return
        ec, Rye = self.ql_input_extract(NorthMing)
        if ec:
            YzErrors().throw_errors(ec)
            return
        if Rye == []:
            YzErrors().throw_errors(802)
            return
        try:
            if Rye[0] > self.compile.size:
                if len(Rye) == 1:
                    YzErrors().throw_errors(802)
                    return
                del Rye[0]
        except:
            YzErrors().throw_errors(999)
            return  
        if Rye == []:
            YzErrors().throw_errors(802)
            return
        text = '行即将删除\n是否确认?'
        for r in Rye:
            text = str(r)+' '+text
        text = '第 '+text 
        if pyautogui.confirm(text=text,title='Notice',buttons=['YES', 'NO']) in ['NO', None]:
            return
        self.base_del_package(Rye)
        self.scr_renew()
    def bt_copy(self, *args): #编辑-复制
        xikal = self.__ql_get()
        if xikal < 0:
            return
        try:
            noe = self.compile.procedure_list[xikal]
            self.input_cover(noe)
        except:
            self.scr_renew()
            YzErrors().throw_errors(409)
    def quick_copy(self): #快速复制
        xikal = self.__ql_get()
        if xikal < 0:
            return
        NorthMing = pyautogui.prompt(text='请输入粘贴到第i行(复制前的行号)[自然数]:\n{如需粘贴多行,请以空格分隔}',title='Notice',default='')
        if NorthMing == None:
            return
        ec, Rye = self.ql_input_extract(NorthMing)
        if ec:
            YzErrors().throw_errors(ec)
            return
        if Rye == []:
            YzErrors().throw_errors(802)
            return
        text = '行\n是否确认?'
        for r in Rye:
            text = str(r)+' '+text
        text = '第'+str(xikal)+'行将被复制到第 '+text 
        if pyautogui.confirm(text=text,title='Notice',buttons=['YES', 'NO']) in ['NO', None]:
            return
        
        try:
            ec = self.compile.pl_copy(xikal, Rye)
            self.scr_renew()
            if ec:
                if ec<0:
                    r = -ec-1
                    text = '粘贴到第 '+str(r)+' 行时遇到了错误\n粘贴中止\n'
                    pyautogui.alert(text=text,title='ERROR')
                    return
                YzErrors().throw_errors(ec)
        except:
            self.scr_renew()
            YzErrors().throw_errors(409)
    def bt_cut(self, *args): #编辑-剪切
        xikal = self.__ql_get()
        if xikal < 0:
            return
        try:
            noe = self.compile.procedure_list[xikal]
            self.input_cover(noe)
            ec = self.compile.pl_pop(xikal)
            self.scr_renew()
            if ec:
                YzErrors().throw_errors(ec)
        except:
            self.scr_renew()
            YzErrors().throw_errors(410)
    def quick_cut(self, *args): #快速剪切
        xikal = self.__ql_get()
        if xikal < 0:
            return
        Anmicius = pyautogui.prompt(text='请输入需剪切到第i行(剪切前的行号)[自然数]:',title='Notice',default='')
        if Anmicius == None:
            return
        try:
            if not Anmicius.isdigit():
                YzErrors().throw_errors(802)
                return
            Anmicius = int(Anmicius)
        except:
            YzErrors().throw_errors(999)
            return
        if Anmicius < 0:
            YzErrors().throw_errors(101)
            return
        if Anmicius > self.compile.size+1:
            Anmicius = self.compile.size+1
            
        text = '第'+str(xikal)+'行将被剪切到第 '+str(Anmicius)+' 行\n是否确认?'
        if pyautogui.confirm(text=text,title='Notice',buttons=['YES', 'NO']) in ['NO', None]:
            return
        try:
            ec = self.compile.pl_cut(xikal, Anmicius)
            self.scr_renew()
            if ec:
                YzErrors().throw_errors(ec)
        except:
            self.scr_renew()
            YzErrors().throw_errors(410)
    def __input_xy_cover(self, cx, cy):
        if self.elem[11]['values'].index(self.elem[10].get()) != 0:
            self.elem[11].current(0)
            self.mode_choice()
            self.elem[13].current(0)
            self.oper_choice()
        self.elem[14].delete(0,tk.END)
        self.elem[14].insert(0,str(cx))
        self.elem[15].delete(0,tk.END)
        self.elem[15].insert(0,str(cy))
    def get_cursor_loc(self): #定位光标
        xikal = pyautogui.prompt(text='请输入需等待时间[自然数]:',title='Notice',default='5')
        if xikal == None:
            return
        try:
            if not xikal.isdigit():
                YzErrors().throw_errors(802)
                return
            xikal = int(xikal)
        except:
            YzErrors().throw_errors(999)
            return
        try:
            self.master.withdraw()
            cMx, cMy = self.get_cursor_xy(xikal)
            self.master.deiconify()
            pyautogui.alert(text='鼠标刚才所在坐标\n x[{:d}] y[{:d}]'.format(cMx,cMy),title='鼠标定位成功')
            self.__input_xy_cover(cMx, cMy)
        except:
            self.master.deiconify()
            YzErrors().throw_errors(999)
    def sc_get_cursor_loc(self, *args): #快捷定位光标
        try:
            cMx, cMy = self.get_cursor_xy()
            self.__input_xy_cover(cMx, cMy)
        except:
            YzErrors().throw_errors(999)
    def leading_out(self): #导出
        try:
            file_path = ''
            file_path = filedialog.asksaveasfilename(title='保存文件',defaultextension='.txt',filetypes=[('text file', '*.txt')])
            if (file_path == None) or (file_path == ''):
                return
            out_text = self.compile.transform_procedure()
            with open(file=file_path,mode='w+',encoding='utf-8') as file:
                file.write(out_text)
        except:
            YzErrors().throw_errors(501)
            return
        pyautogui.alert(text='导出完成',title='Notice')
    def leading_in(self): #导入
        self.leading_in_a(1)
    def leading_in_a(self, a=0): #追加导入
        in_text = ''
        try:
            file_path = ''
            file_path = filedialog.askopenfilename(title='选择文件',filetypes=[('text file', '*.txt')])
            if (file_path == None) or (file_path == ''):
                return
            with open(file=file_path,mode='r',encoding='utf-8') as file:
                in_text = file.read()
            self.compile.reco()
            if a:
                self.compile.pl_reset()
            ec, el = self.compile.alys_code_package(in_text)
            if ec:
                YzErrors().throw_errors(ec)
                return
            if el != []:
                ccz = '导入代码时:\n  第'
                for thh in el:
                    ccz += ' '+str(thh)
                ccz += '\. 行\n解析失败\n自动跳过'
                pyautogui.alert(text=ccz,title='Alert')
        except:
            self.compile.undo()
            YzErrors().throw_errors(802)
            self.scr_renew()
            return
        self.scr_renew()
        pyautogui.alert(text='导入完成',title='Notice')

