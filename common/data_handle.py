# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: data_handle.py
@IDE: PyCharm
@time: 2024-03-28 13:41
@description: 数据处理
"""
# 标准库导入
import re, uuid, copy
# 第三方库导入
from string import Template
from common.logger_handle import ui_logger
# 本地模块导入
from common.basefunc import eval_data


class DataHandle:
    """
    数据处理
    """

    def replace_and_store_placeholders(self, pattern, text, resultAsDict=True):
        """
        提取字符串中符合正则表达式的元素，同时用一个唯一的uuid来替换原有字符串
        例如：
        原字符串：user_id: ${user_id}, user_name: ${user_name}
        替换后的原字符串：user_id: e1c6fc74-2f21-49a9-8d0c-de16650c6364, user_name: 50c74155-5cb5-4809-bc5d-277addf8c3e7
        暂存的需要被处理的关键字或函数：{'e1c6fc74-2f21-49a9-8d0c-de16650c6364': {0: '${user_id}', 1: 'user_id'}, '50c74155-5cb5-4809-bc5d-277addf8c3e7': {0: '${user_name}', 1: 'user_name'}}
        """
        placeholders = {}

        def replace(match):
            placeholder = str(uuid.uuid4())  # 使用uuid生成唯一的占位符
            placeholders[placeholder] = {0: f'${match.group(1)}', 1: match.group(1)}  # 将提取到的字符串存储到字典中
            return placeholder

        # 使用正则表达式进行字符串匹配和替换，同时指定替换次数为 1
        replaced_text = re.sub(pattern, replace, text, count=1)
        while replaced_text != text:
            text = replaced_text
            replaced_text = re.sub(pattern, replace, text, count=1)

        if resultAsDict:
            return replaced_text, placeholders
        else:
            # 构造结果字符串
            result = '{\n'
            for key, value in placeholders.items():
                result += f"    '{key}': {{0: \"{value[0]}\", 1: \"{value[1]}\"}},\n"
            result += '}'
            return replaced_text, result

    def invoke_funcs(self, obj, funcs):
        """
        调用方法，并将方法返回的结果替换到obj中去
        """
        for key, funcs in funcs.items():  # 遍历方法字典调用并替换
            func = funcs[1]
            # ui_logger.debug("invoke func : ", func)
            try:
                if "." in func:
                    obj = self.deal_func_res(obj, key, eval(func))
                else:
                    func_parts = func.split('(')
                    func_name = func_parts[0]
                    func_args_str = ''.join(func_parts[1:])[:-1]
                    obj = self.deal_func_res(obj, key, eval(func))
            except:
                ui_logger.warning("Warn: --------函数：%s 无法调用成功, 请检查是否存在该函数-------" % func)
                obj = obj.replace(key, funcs[0])

        return obj

    def deal_func_res(self, obj, key, res):
        obj = obj.replace(key, str(res))
        try:
            if not isinstance(res, str):
                obj = eval(obj)
        except:
            msg = (f"\nobj --> {obj}\n"
                   f"函数返回值 --> {res}\n"
                   f"函数返回值类型 --> {type(res)}\n")
            ui_logger.warning(f"\nWarn: --------处理函数方法后，尝试eval({obj})失败，可能原始的字符串并不是python表达式-------{msg}")
        return obj

    def data_handle(self, obj, source=None):
        obj = copy.deepcopy(eval_data(obj))
        return self.data_handle_(obj, source)

    def data_handle_(self, obj, source=None):
        """
        递归处理字典、列表中的字符串，将${}占位符替换成source中的值
        """
        func = {}
        keys = {}

        source = {} if not source or not isinstance(source, dict) else source
        ui_logger.trace(f"source={source}")

        # 如果进来的是字符串，先将各种类型的表达式处理完
        if isinstance(obj, str):
            # 先把python表达式找出来存着，这里会漏掉一些诸如1+1的表达式
            pattern = r"\${([^}]+\))}"  # 匹配以 "${" 开头、以 ")}" 结尾的字符串，并在括号内提取内容，括号内不能包含"}"字符
            obj, func = self.replace_and_store_placeholders(pattern, obj)

            # 模板替换
            should_eval = 0
            if obj.startswith("${") and obj.endswith("}"):
                if source.get(obj[2:-1]) and not isinstance(source[obj[2:-1]], str):
                    should_eval = 1
            obj = Template(obj).safe_substitute(source)
            if should_eval == 1:
                obj = eval_data(obj)

            if not isinstance(obj, str):
                return self.data_handle(obj)

            # 再找一遍剩余的${}跟第一步的结果合并，提取漏掉的诸如1+1的表达式(在此认为关键字无法替换的都是表达式，最后表达式也无法处理的情况就报错或者原样返回)
            pattern = r'\$\{([^}]+)\}'  # 定义匹配以"${"开头，"}"结尾的字符串的正则表达式
            obj, func_temp = self.replace_and_store_placeholders(pattern, obj)
            func.update(func_temp)
            # 进行函数调用替换
            obj = self.invoke_funcs(obj, func)
            if not isinstance(obj, str):
                return self.data_handle(obj)
            # 直接返回最后的结果
            return obj
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                obj[index] = self.data_handle(item, source)
            return obj
        elif isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self.data_handle(value, source)
            return obj
        else:
            return obj