# -*- coding: utf-8 -*-
"""
Welcome to Noah's Ark
"""
import tkinter as tk
from tkinter import scrolledtext, StringVar, IntVar, filedialog
import pyautogui
import time
import pickle
import json

from yZagguibase import YzAdvancedGui
from yZagvoicer import YzVoiceMode
from yZagcompile import ProcedurePart
from yZagnlpcore import NLP_EGG
from yZagtools import YzTools
from yZaginf import YzHelpDoc, YzVoicerDoc, YzVersionDoc
from yZagerrors import YzErrors

class YzChildWins(YzAdvancedGui, YzVoiceMode): #子窗口
    wins_onf = [0] * 7 #窗口开启记录
    wins = [None] * 7 #窗口
    # 0帮助窗口 | 1版本窗口 | 2调试窗口 | 3指令窗口 | 4处理器设置 | 5实时语音窗口 | 6语音设置
    def __init__(self, parent):
        self.egg = NLP_EGG() #中文文本处理蛋
        YzAdvancedGui.__init__(self, parent)
        YzVoiceMode.__init__(self)
    def hide_wins(self): #隐藏窗口
        self.master.withdraw()
        for g in range(len(self.wins)):
            if self.wins_onf[g]:
                self.wins[g].withdraw()
    def display_wins(self): #显示窗口
        self.master.deiconify()
        for g in range(len(self.wins)):
            if self.wins_onf[g]:
                self.wins[g].deiconify()
    def ff_on_mw(self, *args): #聚焦主界面
        self.master.focus_force()
    def carryout(self, *args): #执行
        if pyautogui.confirm(text='开始执行?',title='Notice',buttons=['YES', 'NO']) in ['NO', None]:
            return
        if self.compile.size == -1:
            YzErrors().throw_errors(804)
            return
        self.hide_wins()
        if self.compile.carryout_kernel():
            pyautogui.alert(text='执行完毕',title='Notice')
        self.display_wins()
    def help_doc(self, *args): #帮助文档
        if self.wins_onf[0]:
            self.wins[0].focus_force()
            return
        self.wins_onf[0] = 1
        self.wins[0] = tk.Toplevel()
        self.wins[0].geometry('800x500')
        self.wins[0].resizable(0,0)
        self.wins[0].title('帮助文档')
        
        fm = tk.Frame(self.wins[0])
        self.hdc = IntVar()
        for i in range(5):
            tk.Radiobutton(fm,text=YzHelpDoc.doc[i][0],value=i,variable=self.hdc,command=self.updata_hd).grid(row=0,column=i,padx=30)
        self.hdoc = scrolledtext.ScrolledText(fm,height=20,wrap=tk.WORD,state=tk.DISABLED)
        self.hdoc.grid(row=1,column=0,columnspan=5)
        fm.pack()
        self.updata_hd()
        self.wins[0].bind('<Alt-m>',self.ff_on_mw) #快捷键-主界面
        self.wins[0].bind('<Alt-e>',self.cmd_nlp) #快捷键-模糊输入
        self.wins[0].bind('<Alt-f>',self.cmd_code) #快捷键-代码输入
        self.wins[0].bind('<Alt-v>',self.cmd_voicer) #快捷键-语音输入
        self.wins[0].bind('<Alt-q>',self.hw_callbackClose) #快捷键-关闭窗口
        self.wins[0].protocol('WM_DELETE_WINDOW',self.hw_callbackClose)
        self.wins[0].focus_force()
    def hw_callbackClose(self, *args):
        self.wins_onf[0] = 0
        self.wins[0].destroy()
    def updata_hd(self):
        self.hdoc.configure(state=tk.NORMAL)
        self.hdoc.delete(0.0,tk.END)
        self.hdoc.insert(tk.INSERT,YzHelpDoc.doc[int(self.hdc.get())][1])
        self.hdoc.configure(state=tk.DISABLED)
    def version_doc(self): #版本信息
        if self.wins_onf[1]:
            return
        self.wins_onf[1] = 1
        self.wins[1] = tk.Toplevel()
        self.wins[1].geometry('600x300')
        self.wins[1].resizable(0,0)
        self.wins[1].title('版本信息')
        vtext = tk.Text(self.wins[1])
        vtext.pack()
        vtext.insert(tk.INSERT,YzVersionDoc().doc)
        vtext.configure(state=tk.DISABLED)
        self.wins[1].protocol('WM_DELETE_WINDOW',self.vw_callbackClose)
    def vw_callbackClose(self):
        self.wins_onf[1] = 0
        self.wins[1].destroy()
        
    def debug(self, *args): #调试
        if self.wins_onf[2]:
            return
        self.wins_onf[2] = 1
        self.wins[2] = tk.Toplevel()
        self.wins[2].geometry('320x200')
        self.wins[2].resizable(0,0)
        self.wins[2].title('Debug')
        
        digit_limit = self.wins[2].register(YzTools.in_isdigit) #自然数限定
        tk.Label(self.wins[2],text='起始行:').grid(row=0,column=0,padx=16,pady=4)
        tk.Label(self.wins[2],text='终止行:').grid(row=2,column=0,padx=16,pady=4)
        self.ll_Entry = tk.Entry(self.wins[2],bd=1,relief=tk.RIDGE,bg='AliceBlue',width=12,
                                     textvariable=StringVar(),validate='key',validatecommand=(digit_limit,'%P'))
        self.ll_Entry.grid(row=1,column=0,padx=16,pady=5)
        self.rl_Entry = tk.Entry(self.wins[2],bd=1,relief=tk.RIDGE,bg='AliceBlue',width=12,
                                     textvariable=StringVar(),validate='key',validatecommand=(digit_limit,'%P'))
        self.rl_Entry.grid(row=3,column=0,padx=16,pady=5)
        tk.Button(self.wins[2],text='开始调试',command=self.__start_debugging,justify=tk.LEFT).grid(row=1,column=1,rowspan=2,padx=20,pady=1)
        self.wins[2].protocol('WM_DELETE_WINDOW',self.db_callbackClose)
        self.wins[2].focus_force()
    def db_callbackClose(self):
        self.wins_onf[2] = 0
        self.wins[2].destroy()
    def __start_debugging(self):
        l = self.ll_Entry.get()
        r = self.rl_Entry.get()
        try:
            l = int(l)
            r = int(r)
            if l > r:
                YzErrors().throw_errors(802)
                return
            if (l < 0) or (r > self.compile.size):
                YzErrors().throw_errors(101)
                return
        except:
            YzErrors().throw_errors(802)
            return
        self.hide_wins()
        self.wins[2].withdraw()
        time.sleep(1)
        if self.compile.carryout_kernel(l,r):
            pyautogui.alert(text='调试完毕',title='Notice')
        self.display_wins()
    def cmd_code(self, *args): #代码指令精准输入
        if self.wins_onf[3]:
            self.wins[3].focus_force()
            return
        self.wins_onf[3] = 1
        self.wins[3] = tk.Toplevel()
        self.wins[3].geometry('800x80')
        self.wins[3].resizable(0,0)
        self.wins[3].title('CMD-代码指令')
        
        tk.Label(self.wins[3],text='   :>    ').grid(row=0,column=0,padx=1,pady=20)
        self.cmd_Entry = tk.Entry(self.wins[3],bd=3,relief=tk.SUNKEN,bg='GhostWhite',width=64,textvariable=StringVar())
        self.cmd_Entry.grid(row=0,column=1,columnspan=5,padx=1,pady=20)
        
        self.wins[3].bind('<Alt-m>',self.ff_on_mw) #快捷键-主界面
        self.wins[3].bind('<Alt-h>',self.help_doc) #快捷键-帮助文档
        self.wins[3].bind('<Alt-w>',self.cmd_get_cursor_loc) #快捷键-快速获得鼠标坐标
        self.wins[3].bind('<Alt-f>',self.cmd_clear) #快捷键-清空输入
        self.wins[3].bind('<Alt-q>',self.cmd_callbackClose) #快捷键-关闭窗口
        self.wins[3].bind('<Return>',self.cmd_c_enter) #快捷键-完成输入
		
        self.wins[3].protocol('WM_DELETE_WINDOW',self.cmd_callbackClose)
        self.cmd_Entry.focus_set()
    def cmd_callbackClose(self, *args):
        #if self.wins_onf[4]:
            #self.cds_callbackClose()
        self.wins_onf[3] = 0
        self.wins[3].destroy()
    def cmd_clear(self, *args): #清空输入
        self.cmd_Entry.delete(0,tk.END)
    def cmd_get_cursor_loc(self, *args): #快捷获得光标坐标
        try:
            cMx, cMy = self.get_cursor_xy()
            loc = ' '+str(cMx)+' '+str(cMy)+' '
            self.cmd_Entry.insert(tk.INSERT,loc)
        except:
            YzErrors().throw_errors(999)
    def cmd_c_enter(self, *args): #解析输入
        try:
            in_text = self.cmd_Entry.get()
            in_text = in_text.upper()
            if self.__cmd_c_special_case(in_text):
                self.scr_renew()
                return
            ec = self.compile.alys_code(in_text)
            self.scr_renew()
            if ec:
                YzErrors().throw_errors(ec)
                return
        except:
            YzErrors().throw_errors(806)
    def __cmd_c_special_case(self, intext): #输入特殊情况
        sp_case = intext.split()
        if sp_case == []:
            return 1
        sc = sp_case[0]
        if sc in ['CLEAR', 'RESET']: #清空
            self.compile.pl_reset()
            return 1
        if sc == 'UNDO': #撤销
            if self.compile.pl_undo():
                YzErrors().throw_errors(401)
            return 1
        if sc == 'DEL': #删除
            if len(sp_case) > 1:
                if sp_case[1] in ['ALL', ':']:
                    self.compile.pl_reset()
                    return 1
                ec, Rye = self.ql_input_extract(' '.join(sp_case[1:]))
                if ec:
                    YzErrors().throw_errors(806)
                    return 1
                if Rye == []:
                    return 1
                if Rye[0] > self.compile.size:
                    if len(Rye) == 1:
                        return 1
                    del Rye[0]
                self.base_del_package(Rye)
                return 1
            self.base_del()
            return 1
        if sc == 'COPY':
            return 1
        if sc == 'CUT':
            return 1
        return 0
    def cmd_nlp(self, *args): #中文指令模糊输入
        if self.wins_onf[3]:
            self.wins[3].focus_force()
            return
        self.wins_onf[3] = 1
        self.tr = False #待输入状态
        self.temp_godrose = None #缓存
        self.wins[3] = tk.Toplevel()
        self.wins[3].geometry('800x160')
        self.wins[3].resizable(0,0)
        self.wins[3].title('CMD-模糊中文指令')
        
        tk.Label(self.wins[3],text='   :>    ').grid(row=0,column=0,padx=1,pady=20)
        self.cmd_Entry = tk.Entry(self.wins[3],bd=3,relief=tk.SUNKEN,bg='GhostWhite',width=64,textvariable=StringVar())
        self.cmd_Entry.grid(row=0,column=1,columnspan=5,padx=1,pady=20)
        tk.Label(self.wins[3],text='   <>    ').grid(row=1,column=0,padx=1,pady=20)
        self.cmd_text = tk.Text(self.wins[3],width=60,height=1,bg='PeachPuff')
        self.cmd_text.grid(row=1,column=1,padx=1,pady=10)
        self.cmd_text.configure(state=tk.DISABLED)
        
        self.wins[3].bind('<Alt-m>',self.ff_on_mw) #快捷键-主界面
        self.wins[3].bind('<Alt-w>',self.cmd_get_cursor_loc) #快捷键-快捷获得鼠标坐标
        self.wins[3].bind('<Alt-e>',self.cmd_clear) #快捷键-清空输入
        self.wins[3].bind('<Alt-q>',self.cmd_callbackClose) #快捷键-关闭窗口
        self.wins[3].bind('<Alt-h>',self.help_doc) #快捷键-帮助文档
        self.wins[3].bind('<Alt-s>',self.cmd_setting) #快捷键-设置
        self.wins[3].bind('<Return>',self.cmd_n_enter) #快捷键-完成/确认输入
        self.wins[3].bind('<Alt-Return>',self.cmd_n_unlock) #快捷键-输入栏解锁
        
        self.wins[3].protocol('WM_DELETE_WINDOW',self.cmd_callbackClose)
        self.cmd_Entry.focus_set()
    def cmd_n_unlock(self, *args): #输入栏解锁
        if self.tr:
            self.tr = False
            self.cmd_text.configure(state=tk.NORMAL)
            self.cmd_text.delete(0.0,tk.END)
            self.cmd_text.configure(state=tk.DISABLED)
            self.cmd_text.configure(bg='PeachPuff')
            self.cmd_Entry.configure(state=tk.NORMAL)
    def cmd_n_enter(self, *args): #完成输入/确认输出
        if self.tr:
            self.tr = False
            self.cmd_text.configure(state=tk.NORMAL)
            self.cmd_text.delete(0.0,tk.END)
            self.cmd_text.configure(state=tk.DISABLED)
            self.cmd_text.configure(bg='PeachPuff')
            self.cmd_Entry.configure(state=tk.NORMAL)
            ec = self.compile.pl_append_(self.temp_godrose)
            if ec:
                YzErrors().throw_errors(ec)
            self.scr_renew()
            return
        text = self.cmd_Entry.get()
        if text == '':
            return
        try:
            ec, res, err = self.egg.text_processing([text])
            if ec:
                YzErrors().throw_errors(ec)
                return
            if err[0]:
                YzErrors().throw_errors(806)
                return
            elif err[1]:
                YzErrors().throw_errors(808)
                return
            self.temp_godrose = ProcedurePart()
            ec = self.temp_godrose.write_in(res[0])
            if ec:
                YzErrors().throw_errors(ec)
                return
            self.cmd_text.configure(state=tk.NORMAL)
            self.cmd_text.delete(0.0,tk.END)
            self.cmd_text.insert(tk.INSERT,'  '+self.temp_godrose.translate_procedure())
            self.cmd_text.configure(state=tk.DISABLED)
            self.cmd_text.configure(bg='PaleGreen')
            self.cmd_Entry.configure(state=tk.DISABLED)
            self.tr = True
        except:
            YzErrors().throw_errors(999)
            return
    def vague_leading_in(self):
        in_text = ''
        try:
            file_path = ''
            file_path = filedialog.askopenfilename(title='选择文件',filetypes=[('text file', '*.txt')])
            if (file_path == None) or (file_path == ''):
                return
            with open(file=file_path,mode='r',encoding='utf-8') as file:
                in_text = file.readlines()
            if in_text == []:
                YzErrors().throw_errors(809)
                return
            ec, res, err = self.egg.text_processing(in_text)
            if ec:
                YzErrors().throw_errors(ec)
                return
            for r in res:
                ec = self.compile.pl_append(r)
                if ec:
                    err[1] += 1
                    continue
            self.scr_renew()
            if err != [0, 0]:
                js = '解析文本时:\n'
                js += '  存在 '+str(err[0])+' 行无法识别\n'
                js += '  存在 '+str(err[1])+' 行提取参数失败\n自动忽略'
                pyautogui.alert(text=js,title='Alert')
        except:
            YzErrors().throw_errors(411)
            return
        self.scr_renew()
        pyautogui.alert(text='导入完成',title='Notice')
    def cmd_setting(self, *args): #cmd设置窗口
        if self.wins_onf[4]:
            self.wins[4].focus_force()
            return
        self.wins_onf[4] = 1
        self.wins[4] = tk.Toplevel()
        self.wins[4].geometry('500x400')
        self.wins[4].resizable(0,0)
        self.wins[4].title('CMD设置')
        self.temp_Riena = [-1, -1]
        self.curr_Riena = [self.egg.albumen.TC_type, self.egg.yolk.IE_type]
        
        tk.Label(self.wins[4],text='  [分类器]  ').grid(row=0,column=0,padx=10,pady=20)
        tk.Label(self.wins[4],text='  [提取法]  ').grid(row=0,column=2,padx=10,pady=20)
        tk.Button(self.wins[4],text='扩展',command=self.cds_ext_tc,justify=tk.LEFT).grid(row=0,column=1,padx=10,pady=20,sticky=tk.W)
        tk.Button(self.wins[4],text='扩展',command=self.cds_ext_ie,justify=tk.LEFT).grid(row=0,column=3,padx=10,pady=20,sticky=tk.W)
        self.cds_tc = [tk.Text(self.wins[4],width=20,height=1,bg='Lavender') for x in range(4)]
        self.cds_ie = [tk.Text(self.wins[4],width=20,height=1,bg='Lavender') for x in range(4)]
        for i in range(4):
            self.cds_tc[i].grid(row=i+1,column=0,columnspan=2,padx=20,pady=10)
            if i < len(self.egg.albumen.TC_list):
                self.cds_tc[i].insert(tk.INSERT,' '+self.egg.albumen.TC_name[i])
                if i == self.curr_Riena[0]:
                    self.cds_tc[i].configure(bg='PaleGreen')
            self.cds_ie[i].grid(row=i+1,column=2,columnspan=2,padx=20,pady=10)
            if i < len(self.egg.yolk.IE_list):
                self.cds_ie[i].insert(tk.INSERT,' '+self.egg.yolk.IE_name[i])
                if i == self.curr_Riena[1]:
                    self.cds_ie[i].configure(bg='PaleGreen')
            self.cds_tc[i].configure(state=tk.DISABLED)
            self.cds_ie[i].configure(state=tk.DISABLED)
        tk.Label(self.wins[4],text='<Alt+1>选择↑').grid(row=6,column=0,columnspan=2,padx=10,pady=1)
        tk.Label(self.wins[4],text='<Alt+2>选择↑').grid(row=6,column=2,columnspan=2,padx=10,pady=1)
        tk.Label(self.wins[4],text='<Enter>确认选择').grid(row=7,column=0,columnspan=4,padx=10,pady=1,sticky=tk.W)
        tk.Label(self.wins[4],text='<Ctrl+Alt+R>重启文本处理模块').grid(row=8,column=0,columnspan=4,padx=10,pady=1,sticky=tk.W)
        tk.Label(self.wins[4],text='<Alt+Q>关闭窗口').grid(row=9,column=0,columnspan=4,padx=10,pady=1,sticky=tk.W)
        
        self.wins[4].bind('<Alt-q>',self.cds_callbackClose) #快捷键-关闭窗口
        self.wins[4].bind('<Alt-KeyPress-1>',self.cds_ke_tc)
        self.wins[4].bind('<Alt-KeyPress-2>',self.cds_ke_ie)
        self.wins[4].bind('<Return>',self.cds_enter)
        self.wins[4].bind('<Control-Alt-r>',self.cds_restart)
        
        self.wins[4].protocol('WM_DELETE_WINDOW',self.cds_callbackClose)
        self.wins[4].focus_force()
    def cds_callbackClose(self, *args):
        self.wins_onf[4] = 0
        self.wins[4].destroy()
    def cds_ext_tc(self, *args):
        try:
            file_path = ''
            file_path = filedialog.askopenfilename(title='选择文件',filetypes=[('PKL file', '*.pkl')])
            if (file_path == None) or (file_path == ''):
                return
            with open(file_path, 'rb') as f:
                temp = pickle.load(f)
                ec = self.egg.albumen.TC_load(temp)
                if ec:
                    YzErrors().throw_errors(ec)
                    return
        except:
            YzErrors().throw_errors(412)
            return
        i = len(self.egg.albumen.TC_list)-1
        self.cds_tc[i].configure(state=tk.NORMAL)
        self.cds_tc[i].insert(tk.INSERT,' '+self.egg.albumen.TC_name[i])
        self.cds_tc[i].configure(state=tk.DISABLED)
        self.wins[4].focus_set()
    def cds_ext_ie(self, *args):
        try:
            file_path = ''
            file_path = filedialog.askopenfilename(title='选择文件',filetypes=[('PKL file', '*.pkl')])
            if (file_path == None) or (file_path == ''):
                return
            with open(file_path, 'rb') as f:
                temp = pickle.load(f)
                ec = self.egg.yolk.IE_load(temp)
                if ec:
                    YzErrors().throw_errors(ec)
                    return
        except:
            YzErrors().throw_errors(412)
            return
        i = len(self.egg.yolk.IE_list)-1
        self.cds_ie[i].configure(state=tk.NORMAL)
        self.cds_ie[i].insert(tk.INSERT,' '+self.egg.yolk.IE_name[i])
        self.cds_ie[i].configure(state=tk.DISABLED)
        self.wins[4].focus_set()
    def cds_enter(self, *args):
        if self.temp_Riena[0] != -1:
            if self.temp_Riena[0] != self.curr_Riena[0]:
                ec = self.egg.albumen.TC_select(self.temp_Riena[0])
                if ec:
                    YzErrors().throw_errors(ec)
                    self.cds_tc[self.temp_Riena[0]].configure(bg='Lavender')
                else:
                    self.cds_tc[self.curr_Riena[0]].configure(bg='Lavender')
                    self.cds_tc[self.temp_Riena[0]].configure(bg='PaleGreen')
        if self.temp_Riena[1] != -1:
            if self.temp_Riena[1] != self.curr_Riena[1]:
                ec = self.egg.yolk.IE_select(self.temp_Riena[1])
                if ec:
                    YzErrors().throw_errors(ec)
                    self.cds_ie[self.temp_Riena[1]].configure(bg='Lavender')
                else:
                    self.cds_ie[self.curr_Riena[1]].configure(bg='Lavender')
                    self.cds_ie[self.temp_Riena[1]].configure(bg='PaleGreen')
        self.temp_Riena = [-1, -1]
        self.curr_Riena = [self.egg.albumen.TC_type, self.egg.yolk.IE_type]
    def cds_ke_tc(self, *args):
        if self.temp_Riena[0] != -1:
            if self.temp_Riena[0] != self.curr_Riena[0]:
                self.cds_tc[self.temp_Riena[0]].configure(bg='Lavender')
        self.temp_Riena[0] += 1
        if self.temp_Riena[0] >= len(self.egg.albumen.TC_list):
            self.temp_Riena[0] = 0
        if self.temp_Riena[0] != self.curr_Riena[0]:
            self.cds_tc[self.temp_Riena[0]].configure(bg='Khaki')
    def cds_ke_ie(self, *args):
        if self.temp_Riena[1] != -1:
            if self.temp_Riena[1] != self.curr_Riena[1]:
                self.cds_ie[self.temp_Riena[1]].configure(bg='Lavender')
        self.temp_Riena[1] += 1
        if self.temp_Riena[1] >= len(self.egg.yolk.IE_list):
            self.temp_Riena[1] = 0
        if self.temp_Riena[1] != self.curr_Riena[1]:
            self.cds_ie[self.temp_Riena[1]].configure(bg='Khaki')
    def cds_restart(self, *args):
        self.egg.reboot()
        self.cds_callbackClose()
        self.cmd_setting()
    
    def cmd_voicer(self, *args): #语音输入
        if self.wins_onf[3]:
            self.wins[3].focus_force()
            return
        self.wins_onf[3] = 1
        self.wins[3] = tk.Toplevel()
        self.wins[3].geometry('800x200')
        self.wins[3].resizable(0,0)
        self.wins[3].title('CMD-中文语音')
        self.cmv_text = [tk.Text(self.wins[3],width=60,height=1,bd=3,bg='GhostWhite'), 
                         tk.Text(self.wins[3],width=60,height=1,bd=3,bg='PeachPuff')]
        tk.Label(self.wins[3],text='   :>    ').grid(row=0,column=0,padx=1,pady=20) 
        self.cmv_text[0].grid(row=0,column=1,columnspan=5,padx=1,pady=20)
        self.cmv_text[0].configure(state=tk.DISABLED)
        tk.Label(self.wins[3],text='   <>    ').grid(row=1,column=0,padx=1,pady=20)
        self.cmv_text[1].grid(row=1,column=1,padx=1,pady=10)
        self.cmv_text[1].configure(state=tk.DISABLED)
        
        self.cmv_state = 0 #0准备录音 1录音中 2准备输出 3错误
        #0->1 开始录音 | 1->2 结束录音 | 2->0 确认输出 | 3->0 解除错误
        self.cmv_tips = StringVar()
        tk.Label(self.wins[3],textvariable=self.cmv_tips).grid(row=2,column=1,padx=1,pady=10)
        self.cmv_tips.set('<Enter> 按下后自动开始识别声音')
        
        self.wins[3].bind('<Alt-m>',self.ff_on_mw) #快捷键-主界面
        self.wins[3].bind('<Alt-q>',self.cmv_callbackClose) #快捷键-关闭窗口
        self.wins[3].bind('<Alt-h>',self.help_doc) #快捷键-帮助文档
        self.wins[3].bind('<Alt-s>',self.mv_setting) #快捷键-语音设置
        self.wins[3].bind('<Return>',self.cmv_enter) #快捷键-输入/确认
        self.wins[3].bind('<Alt-Return>',self.cmv_enter_cc) #快捷键-取消输入
        
        self.wins[3].protocol('WM_DELETE_WINDOW',self.cmv_callbackClose)
        self.wins[3].focus_force()
    def cmv_callbackClose(self, *args):
        if self.wins_onf[4]:
            self.mvs_callbackClose()
        self.wins_onf[3] = 0
        self.wins[3].destroy()
    def cmv_set_text(self, co, text = None):
        self.cmv_text[co].configure(state=tk.NORMAL)
        self.cmv_text[co].delete(0.0,tk.END)
        if text != None:
            self.cmv_text[co].insert(tk.INSERT,'  '+text)
        self.cmv_text[co].configure(state=tk.DISABLED)
    def cmv_enter(self, *args):
        if self.cmv_state == 2: #确认输出
            self.cmv_enter_cc()
            ec = self.compile.pl_append_(self.temp_godrose)
            if ec:
                self.cmv_state = 3
                self.cmv_set_text(1, YzErrors().get_errors(ec))
                self.cmv_text[1].configure(bg='PeachPuff')
                self.cmv_tips.set('<Enter> 解除错误')
            self.scr_renew()
            return
        elif self.cmv_state == 1: #录音中
            return
        elif self.cmv_state == 3: #解除错误
            self.cmv_state = 2
            self.cmv_enter_cc()
            return
        self.cmv_state = 1
        ec, text = self.start()
        if ec:
            self.cmv_state = 3
            self.cmv_set_text(1, YzErrors().get_errors(ec))
            self.cmv_text[1].configure(bg='PeachPuff')
            self.cmv_tips.set('<Enter> 解除错误')
            return
        if text == '':
            self.cmv_state = 0
            self.cmv_tips.set('<Enter> 按下后自动开始识别声音')
            return
        try:
            ec, res, err = self.egg.text_processing([text])
            if ec:
                self.cmv_state = 3
                self.cmv_set_text(1, YzErrors().get_errors(ec))
                self.cmv_text[1].configure(bg='PeachPuff')
                self.cmv_tips.set('<Enter> 解除错误')
                return
            if err[0]:
                self.cmv_state = 3
                self.cmv_set_text(1, YzErrors().get_errors(806))
                self.cmv_text[1].configure(bg='PeachPuff')
                self.cmv_tips.set('<Enter> 解除错误')
                return
            elif err[1]:
                self.cmv_state = 3
                self.cmv_set_text(1, YzErrors().get_errors(808))
                self.cmv_text[1].configure(bg='PeachPuff')
                self.cmv_tips.set('<Enter> 解除错误')
                return
            self.temp_godrose = ProcedurePart()
            ec = self.temp_godrose.write_in(res[0])
            if ec:
                self.cmv_state = 3
                self.cmv_set_text(1, YzErrors().get_errors(ec))
                self.cmv_text[1].configure(bg='PeachPuff')
                self.cmv_tips.set('<Enter> 解除错误')
                return
            self.cmv_set_text(0, text)
            self.cmv_set_text(1, self.temp_godrose.translate_procedure())
            self.cmv_text[1].configure(bg='PaleGreen')
            self.cmv_state = 2
            self.cmv_tips.set('<Enter> 确认输出  <Enter+Alt> 放弃输出')
        except:
            self.cmv_state = 3
            self.cmv_set_text(1, YzErrors().get_errors(999))
            self.cmv_text[1].configure(bg='PeachPuff')
            self.cmv_tips.set('<Enter> 解除错误')
            return
    def cmv_enter_cc(self, *args): #取消输入
        if self.cmv_state != 2:
            return
        self.cmv_state = 0
        self.cmv_tips.set('<Enter> 按下后自动开始识别声音')
        self.cmv_set_text(0)
        self.cmv_set_text(1)
        self.cmv_text[1].configure(bg='PeachPuff')
        
    def mode_voicer(self, *args): #实时语音模式
        if self.wins_onf[5]:
            self.wins[5].focus_force()
            return
        self.wins_onf[5] = 1
        self.wins[5] = tk.Toplevel()
        self.wins[5].geometry('620x400')
        self.wins[5].resizable(0,0)
        self.wins[5].title('语音模式[鼠标控制]')
        
        self.mvdoc = scrolledtext.ScrolledText(self.wins[5],width=58,height=15,wrap=tk.WORD)
        self.mvdoc.grid(row=0,column=0,columnspan=2)
        self.mvdoc.delete(0.0,tk.END)
        self.mvdoc.insert(tk.INSERT,YzVoicerDoc.doc)
        self.mvdoc.configure(state=tk.DISABLED)
        tk.Button(self.wins[5],text='<设置>',command=self.mv_setting,justify=tk.LEFT).grid(row=1,column=0,padx=10,pady=20)
        tk.Button(self.wins[5],text='<START>',command=self.mvw_start,justify=tk.LEFT).grid(row=1,column=1,padx=10,pady=20)
        
        self.wins[5].bind('<Alt-s>',self.mv_setting) #快捷键-语音设置
        self.wins[5].bind('<Alt-q>',self.mvw_callbackClose) #快捷键-关闭窗口
        self.wins[5].protocol('WM_DELETE_WINDOW',self.mvw_callbackClose)
        self.wins[5].focus_force()
    def mvw_callbackClose(self, *args):
        self.wins_onf[5] = 0
        self.wins[5].destroy()
    def mvw_start(self, *args):
        try:
            licence = ''
            with open(file='Licence\\licence.txt',mode='r',encoding='utf-8') as fi:
                licence = fi.read()
            licence = licence.strip()
            if licence != 'Vm10amQyVkdTWGROVm1SaFVteGFXRmx0TVRSaFJscDBaRWhLYkZKc2JEVmFSVlUxWVVaV1ZVMUVhejA9':
                return pyautogui.alert(text='|> 未授权用户 <|',title='Notice')
        except:
            return pyautogui.alert(text='|> 未授权用户 <|',title='Notice')
        self.hide_wins()
        try:
            ec = self.start_RT()
            if ec:
                YzErrors().throw_errors(ec)
        except:
            YzErrors().throw_errors(415)
        self.display_wins()
        
    def mv_setting(self, *args): #语音模式设置
        if self.wins_onf[6]:
            self.wins[6].focus_force()
            return
        self.wins_onf[6] = 1
        self.wins[6] = tk.Toplevel()
        self.wins[6].geometry('620x360')
        self.wins[6].resizable(0,0)
        self.wins[6].title('语音模式设置')
        
        tk.Label(self.wins[6],text=' <<Baidu-API>>    ').grid(row=0,column=0,padx=1,pady=10)
        tk.Label(self.wins[6],text='  APP_ID:   ').grid(row=1,column=0,padx=1,pady=10)
        self.mvs_Entry1 = tk.Entry(self.wins[6],bd=3,relief=tk.SUNKEN,bg='GhostWhite',width=38,textvariable=StringVar())
        self.mvs_Entry1.grid(row=1,column=1,columnspan=2,padx=1,pady=20)
        tk.Label(self.wins[6],text='  API_KEY:   ').grid(row=2,column=0,padx=1,pady=10)
        self.mvs_Entry2 = tk.Entry(self.wins[6],bd=3,relief=tk.SUNKEN,bg='GhostWhite',width=38,textvariable=StringVar())
        self.mvs_Entry2.grid(row=2,column=1,columnspan=2,padx=1,pady=20)
        tk.Label(self.wins[6],text='  SECRET_KEY:   ').grid(row=3,column=0,padx=1,pady=10)
        self.mvs_Entry3 = tk.Entry(self.wins[6],bd=3,relief=tk.SUNKEN,bg='GhostWhite',width=38,textvariable=StringVar())
        self.mvs_Entry3.grid(row=3,column=1,columnspan=2,padx=1,pady=20)
        tk.Button(self.wins[6],text='保存',command=self.mvs_save,justify=tk.LEFT).grid(row=4,column=0,columnspan=2,padx=10,pady=10)
        tk.Button(self.wins[6],text='导入',command=self.mvs_load,justify=tk.LEFT).grid(row=4,column=2,columnspan=2,padx=10,pady=10)
        
        self.mvs_et_renew()
        
        self.wins[6].bind('<Alt-q>',self.mvs_callbackClose) #快捷键-关闭窗口
        self.wins[6].bind('<Alt-m>',self.ff_on_mw) #快捷键-主界面
        self.wins[6].protocol('WM_DELETE_WINDOW',self.mvs_callbackClose)
        self.wins[6].focus_force()
    def mvs_callbackClose(self, *args):
        self.wins_onf[6] = 0
        self.wins[6].destroy()
    def mvs_save(self, *args):
        self.baidu_token['APP_ID'] = self.mvs_Entry1.get()
        self.baidu_token['API_KEY'] = self.mvs_Entry2.get()
        self.baidu_token['SECRET_KEY'] = self.mvs_Entry3.get()
        pyautogui.alert(text='Saved Successfully',title='Notice')
    def mvs_load(self, *args):
        text = ''
        try:
            file_path = ''
            file_path = filedialog.askopenfilename(title='选择文件',filetypes=[('text file', '*.txt')])
            if (file_path == None) or (file_path == ''):
                return self.wins[6].focus_force()
            with open(file=file_path,mode='r',encoding='utf-8') as file:
                text = file.read()
            if text == '':
                return YzErrors().throw_errors(809)
            js = json.loads(text)
            if type(js) != dict:
                YzErrors().throw_errors(105)
                return self.wins[6].focus_force()
            self.baidu_token['APP_ID'] = js.get('APP_ID', '')
            self.baidu_token['API_KEY'] = js.get('API_KEY', '')
            self.baidu_token['SECRET_KEY'] = js.get('SECRET_KEY', '')
        except json.JSONDecodeError:
            YzErrors().throw_errors(105)
            return self.wins[6].focus_force()
        except:
            pyautogui.alert(text='Failed',title='Notice')
        self.mvs_et_renew()
        pyautogui.alert(text='Loaded Successfully',title='Notice')
        self.wins[6].focus_force()
    def mvs_et_renew(self):
        self.mvs_Entry1.delete(0,tk.END)
        self.mvs_Entry1.insert(tk.INSERT,self.baidu_token['APP_ID'])
        self.mvs_Entry2.delete(0,tk.END)
        self.mvs_Entry2.insert(tk.INSERT,self.baidu_token['API_KEY'])
        self.mvs_Entry3.delete(0,tk.END)
        self.mvs_Entry3.insert(tk.INSERT,self.baidu_token['SECRET_KEY'])
        
class YzUltimateGui(YzChildWins): #功能搭载
    def __init__(self, parent):
        YzChildWins.__init__(self, parent)
        self.__bind_func()
        self.__create_menu()
    def __bind_func(self):
        self.elem[2].configure(command=self.updata_WH)
        self.elem[3].configure(command=self.bt_append)
        self.elem[4].configure(command=self.bt_insert)
        self.elem[5].configure(command=self.bt_updata)
        self.elem[6].configure(command=self.bt_delete)
        self.elem[7].configure(command=self.simulation_check)
        self.elem[8].configure(command=self.carryout)
    def __create_menu(self): #菜单栏 
        m_font = ('黑体', 10)
        menubar = tk.Menu(self.master) 
        
        filemenu = tk.Menu(menubar,tearoff=False)
        filemenu.add_separator()
        filemenu.add_command(label='导入',command=self.leading_in,font=m_font)
        filemenu.add_command(label='导出',command=self.leading_out,font=m_font)
        filemenu.add_separator()
        filemenu.add_command(label='追加导入',command=self.leading_in_a,font=m_font)
        menubar.add_cascade(label='文件',menu=filemenu)
        
        editmenu = tk.Menu(menubar,tearoff=False)
        editmenu.add_separator()
        editmenu.add_command(label='撤销',command=self.bt_undo,font=m_font)
        editmenu.add_command(label='清空',command=self.bt_clear,font=m_font)
        editmenu.add_separator()
        editmenu.add_command(label='复制',command=self.bt_copy,font=m_font)
        editmenu.add_command(label='剪切',command=self.bt_cut,font=m_font)
        editmenu.add_separator()
        editmenu.add_command(label='新增',command=self.bt_append,font=m_font)
        editmenu.add_command(label='插入',command=self.bt_insert,font=m_font)
        editmenu.add_command(label='修改',command=self.bt_updata,font=m_font)
        editmenu.add_command(label='删除',command=self.bt_delete,font=m_font)
        menubar.add_cascade(label='编辑',menu=editmenu)
        
        compilemenu = tk.Menu(menubar,tearoff=False)
        
        compilemenu.add_separator()
        compilemenu.add_command(label='检验',command=self.simulation_check,font=m_font)
        compilemenu.add_command(label='调试',command=self.debug,font=m_font)
        compilemenu.add_separator()
        compilemenu.add_command(label='执行',command=self.carryout,font=m_font)
        menubar.add_cascade(label='编译',menu=compilemenu)
        
        seniormenu = tk.Menu(menubar,tearoff=False)
        seniormenu.add_separator()
        seniormenu.add_command(label='鼠标定位',command=self.get_cursor_loc,font=m_font)
        seniormenu.add_command(label='模糊导入',command=self.vague_leading_in,font=m_font)
        seniormenu.add_command(label='CMD设置',command=self.cmd_setting,font=m_font)
        seniormenu.add_separator()
        seniormenu.add_command(label='语音模式',command=self.mode_voicer,font=m_font)
        seniormenu.add_command(label='语音设置',command=self.mv_setting,font=m_font)
        menubar.add_cascade(label='高级',menu=seniormenu)
        
        self.qm_var = [IntVar() for g in range(9)]
        self.popm_n = ['清空', '撤销', '快速复制', '快速剪切', '快速删除', 
                       '检验', '调试', '鼠标定位', '追加导入']
        self.popm_f = [self.bt_clear, self.bt_undo, self.quick_copy, self.quick_cut, self.quick_delete, 
                       self.simulation_check, self.debug, self.get_cursor_loc, self.leading_in_a]
        
        quickmenu = tk.Menu(menubar,tearoff=False)
        quickmenu.add_separator()
        quickmenu.add_checkbutton(label=self.popm_n[0],variable=self.qm_var[0],onvalue=1,offvalue=0,command=lambda:self.__qm_cevent(0),font=m_font)
        quickmenu.add_checkbutton(label=self.popm_n[1],variable=self.qm_var[1],onvalue=1,offvalue=0,command=lambda:self.__qm_cevent(1),font=m_font)
        quickmenu.add_checkbutton(label=self.popm_n[2],variable=self.qm_var[2],onvalue=1,offvalue=0,command=lambda:self.__qm_cevent(2),font=m_font)
        quickmenu.add_checkbutton(label=self.popm_n[3],variable=self.qm_var[3],onvalue=1,offvalue=0,command=lambda:self.__qm_cevent(3),font=m_font)
        quickmenu.add_checkbutton(label=self.popm_n[4],variable=self.qm_var[4],onvalue=1,offvalue=0,command=lambda:self.__qm_cevent(4),font=m_font)
        quickmenu.add_separator()
        quickmenu.add_checkbutton(label=self.popm_n[5],variable=self.qm_var[5],onvalue=1,offvalue=0,command=lambda:self.__qm_cevent(5),font=m_font)
        quickmenu.add_checkbutton(label=self.popm_n[6],variable=self.qm_var[6],onvalue=1,offvalue=0,command=lambda:self.__qm_cevent(6),font=m_font)
        quickmenu.add_separator()
        quickmenu.add_checkbutton(label=self.popm_n[7],variable=self.qm_var[7],onvalue=1,offvalue=0,command=lambda:self.__qm_cevent(7),font=m_font)
        quickmenu.add_checkbutton(label=self.popm_n[8],variable=self.qm_var[8],onvalue=1,offvalue=0,command=lambda:self.__qm_cevent(8),font=m_font)
        
        menubar.add_cascade(label='工具',menu=quickmenu)
        self.qm_var[2].set(1)
        self.qm_var[3].set(1)
        self.qm_var[4].set(1)
        
        helpmenu = tk.Menu(menubar,tearoff=False)
        helpmenu.add_separator()
        helpmenu.add_command(label='帮助文档',command=self.help_doc,font=m_font)
        helpmenu.add_command(label='版本信息',command=self.version_doc,font=m_font)
        menubar.add_cascade(label='帮助',menu=helpmenu)
        
        self.master.config(menu=menubar) #显示菜单
        
        #右键菜单
        self.popmenu = tk.Menu(self.master)

        self.popmenu.add_command(label='刷新',command=self.scr_renew,font=m_font)
        self.popmenu.add_command(label=self.popm_n[2],command=self.popm_f[2],font=m_font)
        self.popmenu.add_command(label=self.popm_n[3],command=self.popm_f[3],font=m_font)
        self.popmenu.add_command(label=self.popm_n[4],command=self.popm_f[4],font=m_font)
        self.master.bind('<Button-3>',self.m_pop)
        
        self.master.bind('<Control-c>',self.bt_copy) #快捷键-复制
        self.master.bind('<Control-x>',self.bt_cut) #快捷键-剪贴
        self.master.bind('<Control-z>',self.bt_undo) #快捷键-撤销
        self.master.bind('<Control-Alt-c>',self.carryout) #快捷键-执行
        self.master.bind('<Alt-e>',self.cmd_nlp) #快捷键-模糊输入
        self.master.bind('<Alt-f>',self.cmd_code) #快捷键-代码输入
        self.master.bind('<Alt-w>',self.sc_get_cursor_loc) #快捷键-鼠标快速定位
        self.master.bind('<Alt-d>',self.debug) #快捷键-调试窗口
        self.master.bind('<Alt-h>',self.help_doc) #快捷键-帮助文档
        self.master.bind('<Alt-v>',self.cmd_voicer) #快捷键-语音模式
        
    def m_pop(self, event):
        self.popmenu.post(event.x_root,event.y_root)
    def __qm_cevent(self, cm):
        if self.qm_var[cm].get() == 1:
            self.popmenu.add_command(label=self.popm_n[cm],command=self.popm_f[cm],font=('黑体',10))
        else:
            self.popmenu.delete(self.popm_n[cm])