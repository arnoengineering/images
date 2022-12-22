import sqlite3 as sl

con = sl.connect('my-test.db')

from PyQt5.QtGui import QFont, QTextCharFormat, QPalette, QPainter, QColor, QIcon, QPen  # QPainter, QPen,QBrush,
from PyQt5.QtCore import Qt, QDate, QSettings, QRect  # , QByteArray  # QTimer, QSize,

# from data_view import DataFrameViewer
from PyQt5.QtWidgets import *

import sys

# from super_bc import SuperCombo, SuperButton
from PIL import Image, ExifTags


def sort_day(ls):
    ls.sort(key=lambda x: x.toString(Qt.TextDate))


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.first_show = True
        self.setWindowTitle('Call Schedule Optimizer')
        self.setWindowIcon(QIcon('icons/calendar-blue.png'))

        # self.settings = QSettings('Claassens Software', 'Calling LLB_2022')

    def showEvent(self, event):
        if self.first_show:
            self.first_show = False

            print(f'\n{string_break}\n|| Init Doc Window ||\n{string_break}\n')

            # init items
            self._set_list()

            self._set_empty()

            self._setup_load()

            self._creat_toolbar()
            self._create_tools()
            self._set_center()

            self._update_set()
            super().showEvent(event)

    def _set_list(self):
        """inits butons"""
        # init SaveLoad Option
        self.save_l = saveLoad(self, False)

        # init all combo cmds, name_icon
        self.cmd_ls = {
                       'Type': ['Backup', 'Write'],
                       }

        # init all pushbutton, name_icon todo add to menu, todo grade, grade all, grade sem, grade gear, grade all year
        self.button_list = ['Save_disk-black',
                            'Apply',
                            'Load_document-excel-table',
                            ]

    def _set_empty(self):
        """sets empty lists"""

        self.av = {}
        # self.schedules = []
        self.list_v = {}
        self.action_list = {}
        self.combo = {}
        self.sch_ls = {}
        self.active_shifts = []

        self.default_files = None  # either save or here

    def _setup_load(self):

        self.save_l.on_load_fin(self.default_files['class'], 0)

    def _creat_toolbar(self):
        self.font_sizes = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
        self.tool_bar = QToolBar('Main toolbar')
        self.cal_tool_bar = QToolBar('Calendar')

        self.table_tool = QToolBar('Tables')
        self.col = QColorDialog()

        self.font_op = []
        self.but_edit = {}
        self.font_ty_win = {}

        self.tool_bar.addWidget(self.but_edit['color_fill'])


        self.addToolBar(self.tool_bar)

    def _set_center(self):
        self.cal_wig = Calendar(self)
        self.setCentralWidget(self.cal_wig)
        self.active_wig = 'Cal'



    # noinspection PyArgumentList
    def _create_tools(self):
        self.tool_bar2 = QToolBar()

        self.addToolBar(self.tool_bar2)
        self.addToolBar(self.cal_tool_bar)

        # ___________comboboxes_______

        for wig_name, opt in self.cmd_ls.items():
            k = SuperCombo(wig_name, self, vals=opt)
            self.combo[wig_name] = k
            self.tool_bar2.addWidget(k.wig)

    def run_cmd(self, i, ex=None):
        print(f'Running Command: {i}  ||\n')
        pass

    # def set_active_wig(self, wig):
    #     if self.active_wig in self.ti_info:
    #         self.ti_info[self.active_wig].close_dia()
    #     self.active_wig = wig

    def _update_set(self):

        self.settings.beginGroup('File Locals')
        for i in self.default_files.keys():
            self.default_files[i] = self.settings.value(i, self.default_files[i])
        self.settings.endGroup()

        k = self.settings.allKeys()

        for i, j in [(self.restoreGeometry, "Geometry"), (self.restoreState, "windowState")]:
            if j in k:
                va = self.settings.value(j)
                i(va)

        print(f'Finished Loading Settings\n{string_break}\n')

    def _save_user_settings(self):
        self.settings = QSettings('Claassens Software', 'images')
        self.user_settings()

    def user_settings(self):
        print(f'\n{string_break}\nSaving Settings')
        self.settings.setValue("Geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        self.settings.beginGroup('File Locals')
        for i, j in self.default_files.items():
            self.settings.setValue(i, j)
        self.settings.endGroup()

    def closeEvent(self, event):
        print(f'\n{string_break}\nClosing Doc\n{string_break}\n')
        self.user_settings()
        super().closeEvent(event)


class ExifSide(QWidget):
    def __init__(self,par,side=Qt.RightDockWidgetArea):
        super().__init__()
        self.par = par
        self.name = 'Meta'
        self.doc=QDockWidget(self.name)
        self.doc.setWidget(self)


    def _to_forier(self):

        self.proces = QProgressDialog()
        self.nn.lines.connect(self.proces)



class ImageMap:
    def __init__(self):
        self.selected = False
        # self.clicked.connect(lambda _: self.selected = not self.selected)
        self.img = ''
        self.meta = None
        pass

    def paint(self):
        if self.selected:
            print('checkmark')

    def _load_img(self):
        img = Image.open(self.img)
        img_exif = img.getexif()
        print(type(img_exif))
        # <class 'PIL.Image.Exif'>

        if img_exif is None:
            print('Sorry, image has no exif data.')
        else:
            self.meta = {ExifTags.TAGS[key]:val for key, val in img_exif.items() if key in ExifTags.TAGS}


class ImageViewTree(QTreeView):
    def __init__(self):
        super().__init__()

    def load_img(self):
        pass


class ImageList(QListView):
    def __init__(self):
        super().__init__()
        self.scroll = QScrollArea()


string_break = '_' * 10
if __name__ == '__main__':
    strs = ' ___     ____     ____\n' \
           '|   \\   |    |   |    |\n' \
           '|    )  |    |   |\n' \
           '|___/   |____|   |____|\n\n'
    print(strs)
    print(string_break)
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
