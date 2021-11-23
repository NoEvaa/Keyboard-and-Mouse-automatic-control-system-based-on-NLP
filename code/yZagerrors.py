# -*- coding: utf-8 -*-
"""
Welcome to Noah's Ark
"""

import pyautogui

class YzErrors:
    def __init__(self):
        self.errors = {'101':'目标行超出范围!', 
                       '102':'-空输入-', 
                       '103':'-异常输入-', 
                       '104':'-麦克风异常-', 
                       '105':'文本内容格式错误', 
                       
                       '400':'ERROR:撤销时发生未知错误', 
                       '401':'ERROR:创建时发生未知错误', 
                       '402':'ERROR:插入时发生未知错误', 
                       '403':'ERROR:删除时发生未知错误', 
                       '404':'ERROR:写入时发生未知错误', 
                       '405':'ERROR:解析时发生未知错误', 
                       '406':'ERROR:修改时发生未知错误', 
                       '407':'ERROR:执行时发生未知错误', 
                       '408':'ERROR:执行中存在循环出现未知错误', 
                       '409':'ERROR:复制时发生未知错误', 
                       '410':'ERROR:剪切时发生未知错误', 
                       '411':'ERROR:模糊解析时发生未知错误', 
                       '412':'ERROR:添加扩展模块时发生未知错误', 
                       '413':'ERROR:刷新时发生未知错误', 
                       '414':'ERROR:文本分类时发生未知错误', 
                       '415':'ERROR:语音模式下发生未知错误', 
                       '416':'ERROR:录音时发生未知错误', 
                       
                       '501':'导出时发生错误', 
                       '502':'导入时发生错误', 
                       
                       '601':'模糊解析时分类器异常', 
                       '602':'模糊解析时提取器异常', 
                       '603':'扩展模块数量达到上限，无法载入', 
                       '604':'扩展模块无法正常使用', 
                       '605':'Baidu API调用异常', 
                       '606':'网络连接异常', 
                       '607':'语音文件读取异常', 
                       
                       '801':'写入参数中存在错误!', 
                       '802':'请规范输入指定参数!', 
                       '803':'请指定目标行!', 
                       '804':'未识别到代码!', 
                       '805':'执行时鼠标超出屏幕边界!', 
                       '806':'输入内容解析失败!', 
                       '807':'缺少关键组件!', 
                       '808':'无法正常识别参数!', 
                       '809':'未识别到文本!', 
                       '810':'语音识别失败!', 
                       
                       '999':'未知异常'}
    def throw_errors(self, err):
        try:
            if type(err) != str:
                err = str(err)
            if err == '0':
                return
            error_get = self.errors.get(err, 'ERROR:未知错误')
            pyautogui.alert(text=error_get,title='ERROR')
        except:
            pyautogui.alert(text='程序状态异常!',title='ERROR')
    def get_errors(self, err):
        try:
            if type(err) != str:
                err = str(err)
            if err == '0':
                return
            return self.errors.get(err, 'ERROR:未知错误')
        except:
            return '程序状态异常!'
if __name__ == '__main__':
    YzErrors().throw_errors(401)      
       
        