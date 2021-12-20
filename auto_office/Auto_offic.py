# coding=utf8
import re
import sys
import os
from PySide6 import QtCore, QtWidgets  # ()
import PySide6
import pandas as pd
import numpy as np
import json
import datetime
from PySide6.QtWidgets import *
from menu import Ui_Form

# 配置环境变量
dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
print(plugin_path)


#  App class
class MyWidget(QtWidgets.QMainWindow, Ui_Form):
    system_file: list
    save_path: tuple
    CAST_DICT: dict

    def __init__(self):
        # 单例模式
        super().__init__()
        self.setupUi(self)
        self.pending_file_list = []
        #  自定义界面组件属性
        self.toolButton.clicked.connect(self.choice_path_event)
        self.toolButton_2.clicked.connect(self.save_path_event)
        # self.toolButton_3.clicked.connect(self.map_cast_event)  # 费用关系对照表按钮
        # self.toolButton_4.clicked.connect(self.map_cast_event2)  # 部门对照表按钮
        self.toolButton_3.clicked.connect(self.start_event)
        self.pushButton.clicked.connect(self.introduce)

    #  选择待处理文件
    @QtCore.Slot()
    def choice_path_event(self):
        self.pending_file_list = []
        self.textEdit.clear()
        self.system_file = QtWidgets.QFileDialog.getOpenFileNames(self, '浏览', )
        for index, file in enumerate(self.system_file[0]):
            self.textEdit.append(str(index + 1) + ":" + file + ";")
            self.pending_file_list.append(file)
        print(self.pending_file_list)

    #  设置保存路径
    @QtCore.Slot()
    def save_path_event(self):
        self.save_path = QtWidgets.QFileDialog.getSaveFileName(self, '保存路径', dir="export_file.xlsx")
        self.textEdit1.setText(self.save_path[0])
        print(self.save_path)

    #  添加职能中心----费用映射表
    @QtCore.Slot()
    def map_cast_event(self):

        for file in self.pending_file_list:
            file_name = file.split('/')[-1]
            pending_excel = pd.read_excel(file, converters={'二级科目编码': str})
            columns = pending_excel.columns
            cast_code = pending_excel[columns[0]].astype(str, copy=False)
            cast_name = pending_excel[columns[1]]
            CAST_DICT = dict(zip(cast_name, cast_code))
            with open(f'./职能中心关系表/CAST_DICT.json', 'w+', encoding='utf-8') as f:
                json.dump(CAST_DICT, f, ensure_ascii=False)

            with open(f'./CAST_DICT.json', 'r', encoding='utf-8') as f:
                CAST_DICT = json.load(f)

    #  添加职能中心----部门映射表
    @QtCore.Slot()
    def map_dept_event(self):
        for file in self.pending_file_list:
            file_name = file.split('/')[-1]
            pending_excel = pd.read_excel(file)
            pending_excel.dropna(axis='columns', how='all', inplace=True)
            pending_excel.dropna(axis=0, how='any', inplace=True)
            columns = pending_excel.columns
            i = 0
            # (serial0, serial1, serial2, serial3, serial4) = (None for x in range(5))
            # for column in columns:
            #     exec('serial{} = {}'.format(i, list(pending_excel[column])))
            #     i += 1
            serial0 = pending_excel[columns[0]].astype(int, copy=False).astype(str, copy=False)
            serial1 = pending_excel[columns[1]].astype(int, copy=False).astype(str, copy=False)
            serial2 = pending_excel[columns[2]].astype(int, copy=False).astype(str, copy=False)
            serial3 = pending_excel[columns[3]].astype(str, copy=False)
            serial4 = pending_excel[columns[4]].astype(int, copy=False).astype(str, copy=False)
            _dict = {
                'CODE_COMPNY': dict(zip(serial3, serial0)),
                'CODE_BUSNES': dict(zip(serial3, serial1)),
                'CODE_DEPATM': dict(zip(serial3, serial2)),
                'CODE_DEP_ATTR': dict(zip(serial3, serial4)),
            }
            file_list = ['CODE_COMPNY', 'CODE_BUSNES', 'CODE_DEPATM', 'CODE_DEP_ATTR']
            for key, value in _dict.items():
                with open(f'./{key}.json', 'w+', encoding='utf-8') as f:
                    json.dump(value, f, ensure_ascii=False)
            for file in file_list:
                with open(f'./{file}.json', 'r', encoding='utf-8') as f:
                    key = json.load(f)
                print(file)

        # pickle.dump(cast_dict, open('./CAST_DICT.ini', 'wb'))
        # data = open('././CAST_DICT.ini', 'rb')
        # result = pickle.load(data)
        # [print(pending_excel.items()) for column in columns]

    #  费用统计----费用映射表
    def map_cast_event2(self):
        for file in self.pending_file_list:
            file_name = file.split('/')[-1]
            pending_excel = pd.read_excel(file, converters={'科目编码': str})
            columns = pending_excel.columns
            cast_name = pending_excel[columns[0]]
            cast_code = pending_excel[columns[2]].astype(str, copy=False)
            CAST_DICT = dict(zip(cast_name, cast_code))
            with open(f'./费用统计关系表/CAST_DICT.json', 'w+', encoding='utf-8') as f:
                json.dump(CAST_DICT, f, ensure_ascii=False)

    #  费用统计----客商关系映射表
    def map_cost_event2(self):
        for file in self.pending_file_list:
            pending_excle = pd.read_excel(file, converters={'转换的值': str, '适用公司': str})
            columns = pending_excle.columns
            Cost_Merchant = {}
            for index, row in pending_excle.iterrows():
                tran_value = row[[columns[0]]].values[0]
                company_name = row[[columns[1]]].values[0]
                company_head = row[[columns[2]]].values[0]
                b = Cost_Merchant.get(company_name)
                if Cost_Merchant.get(company_name) is None:
                    Cost_Merchant[company_name] = {company_head: tran_value}
                else:
                    Cost_Merchant[company_name][company_head] = tran_value
                # index = index
            with open('./费用统计关系表/Cost_Merchant.json', 'w+', encoding='utf-8') as f:
                json_file = json.dump(Cost_Merchant, f, ensure_ascii=False)
            # lines = pending_excle.values
            # pending_excle.
            # Cost_Merchant

    # 开始处理表按钮
    @QtCore.Slot()
    def start_event(self):
        transform_type = self.comboBox.currentText()
        print(transform_type)
        # 职能费用转换中心
        if transform_type == '职能中心费用转换':
            self.functions_1()

        # 预提费用统计转换
        elif transform_type == '预提费用统计转换':
            self.functions_2()

    #  使用说明
    @QtCore.Slot()
    def introduce(self):
        dialog = QDialog()
        # btn = QPushButton("ok", dialog)
        # btn.move(100, 100)
        dialog.setWindowTitle("使用说明")
        text = "1：打开文件，选择你要转换的表，支持批量转换，多选文件即可\n" \
               "2: 选择保存路径,文件后缀必须以.xlsx结尾\n" \
               "3：点击开始"
        use_guide = QMessageBox
        use_guide.about(dialog, "使用说明", text)
        # dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        # btn.click()
        # dialog.exec_()

    def check(self):
        print(self.checkbox.isChecked())

    @staticmethod
    def up_date(fmt=None):
        uptime = datetime.date.today()
        title_day = datetime.date(uptime.year, uptime.month, 4)
        if uptime < title_day:
            uptime = uptime.replace(day=1) - datetime.timedelta(days=1)
        if not fmt:
            return uptime.strftime("%Y/%m/%d")
        if fmt:
            return "XTTZ" + uptime.strftime(("%Y%m")) + "0001"

    def functions_1(self):
        """职能中心费用转换函数"""
        try:
            i = 1
            self.textBrowser.append("正在处理中......")
            for file in self.pending_file_list:
                src = pd.read_excel(f"{file}")
                src_shape = src.shape
                data_form = np.empty(shape=[src_shape[0] * 3, 11], dtype=str)
                # print(data_form)

                dst = pd.DataFrame(data=data_form, columns=["费用来源",
                                                            "会计日期",
                                                            "会计科目",
                                                            "凭证号",
                                                            "凭证名称",
                                                            "摘要",
                                                            "币别",
                                                            "转换类型",
                                                            "转换率",
                                                            "原币金额",
                                                            "本币金额"])

                config_list = ['CODE_COMPNY', 'CODE_BUSNES', 'CODE_DEPATM', 'CODE_DEP_ATTR', 'CAST_DICT']
                for config in config_list:
                    with open(f'./职能中心关系表/{config}.json', 'r', encoding='utf-8') as f:
                        if config == 'CODE_COMPNY':
                            CODE_COMPNY = json.load(f)
                        if config == 'CODE_BUSNES':
                            CODE_BUSNES = json.load(f)
                        if config == 'CODE_DEPATM':
                            CODE_DEPATM = json.load(f)
                        if config == 'CODE_DEP_ATTR':
                            CODE_DEP_ATTR = json.load(f)
                        if config == 'CAST_DICT':
                            CAST_DICT = json.load(f)
                # serial1 = src["被分摊部门"]
                acc_code_list = []
                abstract_list = []
                original_currency_list = []
                local_currency_list = []
                for item in src.iterrows():
                    cast = item[1]['费用科目']  # type:str
                    if "工资" in cast:
                        cast = "工资"
                    acc_code = CODE_COMPNY[item[1]["被分摊部门"]] + '.' + \
                               CODE_BUSNES[item[1]["被分摊部门"]] + '.' + \
                               CODE_DEPATM[item[1]["被分摊部门"]] + '.' + \
                               CODE_DEP_ATTR[item[1]["被分摊部门"]] + CAST_DICT[cast] + '.0' * 6
                    [acc_code_list.append(acc_code) for i in range(3)]

                    abstract1 = item[1].keys()[4][2:] + item[1].keys()[4][:2] + "计提职能中心" + item[1]["费用科目"]
                    abstract2 = item[1].keys()[5][:2] + "职能中心" + item[1]["费用科目"]
                    abstract3 = item[1].keys()[6][2:] + item[1].keys()[6][:2] + "职能中心" + item[1]["费用科目"]
                    abstract_list.append(abstract1)
                    abstract_list.append(abstract2)
                    abstract_list.append(abstract3)
                    cost1 = item[1][4]
                    cost2 = item[1][5]
                    cost3 = item[1][6]
                    original_currency_list.append(cost1)
                    original_currency_list.append(cost2)
                    original_currency_list.append(cost3)

                dst["费用来源"] = "手工"
                dst["会计日期"] = MyWidget.up_date()
                dst["会计科目"] = acc_code_list
                dst["凭证号"] = MyWidget.up_date(fmt=True)
                dst["摘要"] = abstract_list
                dst["币别"] = "CNY"
                dst["转换类型"] = "User"
                dst["转换率"] = "1"
                dst["原币金额"] = original_currency_list
                dst["本币金额"] = original_currency_list
                sys_file = re.findall(r"(.*/)(.*)(.xlsx)", self.save_path[0])[0]
                path = sys_file[0]
                file_name = sys_file[1]
                file_type = sys_file[2]
                print(path)
                dst.to_excel(f"{path}{file_name}{i}{file_type}", index=False)
                i += 1
            self.textBrowser.append(f"全部导出完毕，文件已保存在:{self.save_path[0]}")

        except Exception as e:
            self.textBrowser.append(f"{e}\n程序异常，请联系开发")

    def functions_2(self):
        try:
            self.textBrowser.append("正在处理中......")
            # 读取关系表
            config_list = ['CODE_COMPNY', 'CODE_BUSNES', 'CODE_DEPATM', 'CODE_DEP_ATTR', 'CAST_DICT', 'Cost_Merchant']
            for config in config_list:
                with open(f'./费用统计关系表/{config}.json', 'r', encoding='utf-8') as f:
                    if config == 'CODE_COMPNY':
                        CODE_COMPNY = json.load(f)
                    elif config == 'CODE_BUSNES':
                        CODE_BUSNES = json.load(f)
                    elif config == 'CODE_DEPATM':
                        CODE_DEPATM = json.load(f)
                    elif config == 'CODE_DEP_ATTR':
                        CODE_DEP_ATTR = json.load(f)
                    elif config == 'CAST_DICT':
                        CAST_DICT = json.load(f)
                    elif config == 'Cost_Merchant':
                        Cost_Merchant = json.load(f)

            # 建立空表框
            for file in self.pending_file_list:
                src = pd.read_excel(f"{file}")
                src.dropna(axis=0, subset=['费用承担部门'], inplace=True)
                # src['所属期'] = src['所属期'].astype(str)
                # print(src.info())
                # src['所属期'] = src['所属期'].apply(lambda x: pd.to_datetime(x).date())
                columns = src.columns
                src_shape = src.shape
                data_form = np.empty(shape=[src_shape[0] * 2, 15], dtype=str)
                dst = pd.DataFrame(data=data_form, columns=["会计科目",
                                                            "TAB",
                                                            "借方",
                                                            "贷方",
                                                            "TAB",
                                                            "说明",
                                                            "TAB",
                                                            "现金流量",
                                                            "TAB",
                                                            "员工工号",
                                                            "TAB",
                                                            "客商编码",
                                                            "TAB",
                                                            "发票号",
                                                            "ENT",
                                                            ])
                i = 0
                j = 0
                for row in src.itertuples():
                    # print(row, dir(row))
                    b = getattr(row, '费用承担部门')
                    dst.loc[i, "会计科目"] = b
                    dst.loc[i, "会计科目"] = CODE_COMPNY[getattr(row, '费用承担部门')] + '.' + \
                                         CODE_BUSNES[getattr(row, '费用承担部门')] + '.' + \
                                         CODE_DEPATM[getattr(row, '费用承担部门')] + '.' + \
                                         CODE_DEP_ATTR[getattr(row, '费用承担部门')] + CAST_DICT[
                                             getattr(row, '费用类别')] + '.0' * 6
                    dst.loc[i + 1:i + 1, ["会计科目"]] = CODE_COMPNY[getattr(row, '费用承担部门')] + '.' + \
                                                     '0' + '.' + \
                                                     '0' + '.' + \
                                                     '22020205' + '.0' * 6

                    dst.iloc[[i], [1]] = 'TAB'
                    dst.iloc[[i + 1], [1]] = 'TAB'

                    dst.loc[i, '借方'] = float('%.2f' % getattr(row, '不含税金额'))
                    dst.loc[i + 1, '借方'] = 'TAB'

                    dst.loc[i, '贷方'] = "TAB"
                    dst.loc[i + 1, '贷方'] = float('%.2f' % getattr(row, '不含税金额'))

                    b = getattr(row, '所属期')

                    dst.iloc[i, 4] = '计提' + getattr(row, '所属期').strftime("%Y-%m") + getattr(row, '费用承担部门') + getattr(
                        row, '供应商') + \
                                     getattr(row, '费用类别')
                    dst.iloc[i + 1, 4] = 'TAB'

                    dst.loc[i, '说明'] = "TAB"
                    dst.loc[i + 1, '说明'] = '计提' + getattr(row, '所属期').strftime("%Y-%m") + getattr(row,
                                                                                                '费用承担部门') + getattr(row,
                                                                                                                    '供应商') + \
                                         getattr(row, '费用类别')
                    dst.iloc[i, 7] = 'TAB'
                    dst.iloc[i + 1, 7] = 'TAB'
                    dst.iloc[i, 9] = 'TAB'
                    dst.iloc[i + 1, 9] = 'TAB'

                    dst.iloc[i + 1, 10] = 'TAB'

                    dst.loc[i, '客商编码'] = 'TAB'
                    dst.loc[i + 1, '客商编码'] = Cost_Merchant[getattr(row, '供应商')][CODE_COMPNY[getattr(row, '费用承担部门')]]

                    dst.loc[i, '发票号'] = "TAB"
                    dst.loc[i + 1, '发票号'] = "TAB"

                    dst.iloc[i, 14] = 'ENT'
                    dst.iloc[i + 1, 14] = 'ENT'
                    i += 2
                # print(dst)
                sys_file = re.findall(r"(.*/)(.*)(.xlsx)", self.save_path[0])[0]
                path = sys_file[0]
                file_name = sys_file[1]
                file_type = sys_file[2]
                print(path)
                dst.to_excel(f"{path}{file_name}{j}{file_type}", index=False)
                j += 1
            self.textBrowser.append(f"全部导出完毕，文件已保存在:{self.save_path[0]}")
        except Exception as e:
            self.textBrowser.append(f"{e}\n程序异常，请联系开发")


app = QtWidgets.QApplication([])
UI = MyWidget()
# widget.resize(800, 600)
UI.show()
sys.exit(app.exec())
