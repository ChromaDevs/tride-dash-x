from PySide6 import QtCore as QtC
from PySide6 import QtWidgets as QtWi
from PySide6 import QtGui
from PIL import Image
import os, sys, json, subprocess, time
import UnityPy
from platformdirs import user_data_dir

data_file: dict = {}
initialised = True
data_folder = user_data_dir("td_custom_icons", "flamezfr")
conf_file = f"{data_folder}\\conf.json"

def clearLayout(layout: QtWi.QLayout):
    if layout is None:
        return
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            # Delete the widget
            widget.deleteLater()
        else:
            # If the item is a nested layout, clear it recursively
            clearLayout(item.layout())

class IconCard(QtWi.QWidget):
    def __init__(self, img_path):
        super().__init__()
        self.img_path = img_path
        self.setMaximumSize(120, 120)
        
        layout = QtWi.QVBoxLayout(self)
        
        preview = QtWi.QLabel(alignment=QtC.Qt.AlignmentFlag.AlignTop)
        pixmap = QtGui.QPixmap(self.img_path).scaled(70, 70, QtC.Qt.KeepAspectRatio)
        preview.setPixmap(pixmap)
        layout.addWidget(preview)
        
        select_btn = QtWi.QPushButton("select")
        select_btn.setGeometry(0,0,20,20)
        select_btn.clicked.connect(self.select)
        layout.addWidget(select_btn) 
    @QtC.Slot()
    def select(self) -> None:
        b = open(f"{data_file["tdfolder"]}\\Tride Dash_Data\\sharedassets1.bak", "rb")
        bakup = b.read()
        b.close()
        with open(f"{data_file["tdfolder"]}\\Tride Dash_Data\\sharedassets1.assets", "wb") as m:
            m.write(bakup)
            m.close()

        res = UnityPy.load(f"{data_file["tdfolder"]}\\Tride Dash_Data\\sharedassets1.assets")
        for obj in res.objects:
            if obj.type.name == "Texture2D":
                if obj.peek_name() == "player":
                    try:
                        player = obj.parse_as_object()
                        img = Image.open(self.img_path)

                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')

                        player.image = img
                        player.save()

                        with open(f"{data_file["tdfolder"]}\\Tride Dash_Data\\sharedassets1.assets", "wb") as f:
                            f.write(res.file.save())
                        break
                    except Exception as e:
                        print(f"Error patching player icon: {e}")
                        continue
                elif obj.peek_name() == "player inner":
                    pass

class MyWidget(QtWi.QWidget):
    def __init__(self):
        global data_file
        super().__init__()
        self.layout: QtWi.QLayout = QtWi.QBoxLayout(QtWi.QBoxLayout.Direction.TopToBottom, self)
        if not initialised:
            self.setupState = 0
            self.h1 = QtGui.QFont()
            self.h1.setPointSize(30)
            self.title = QtWi.QLabel("welcome to td!Custom Icons setup", alignment=QtC.Qt.AlignmentFlag.AlignHCenter)
            self.nextPageBtn = QtWi.QPushButton("next")
            self.nextPageBtn.clicked.connect(self.updSetupLayout)
            self.title.setFont(self.h1)
            self.layout.addWidget(
                self.title
            )
            self.layout.addWidget(self.nextPageBtn)
        else:
            data_file = json.loads(
                open(conf_file, "rt").read()
            )
            self.topbar = QtWi.QHBoxLayout()
            self.title = QtWi.QLabel("your icons")
            self.title.setStyleSheet("font-size: 36px;")
            self.topbar.addWidget(self.title)
            @QtC.Slot()
            def open_icon_dir():
                subprocess.Popen(f"explorer \"{data_file["tdfolder"]}\\icons\\\"")
            @QtC.Slot()
            def refresh():
                self.render_icons()
                self.layout.addStretch()
            self.openicondir = QtWi.QPushButton("open icon folder")
            self.openicondir.clicked.connect(open_icon_dir)
            self.topbar.addWidget(self.openicondir)
            self.topbar.setAlignment(QtC.Qt.AlignmentFlag.AlignTop)
            self.refreshBtn = QtWi.QPushButton("refresh")
            self.refreshBtn.clicked.connect(refresh)
            self.topbar.addWidget(self.refreshBtn)
            self.layout.addLayout(self.topbar)
            self.iconsCont = QtWi.QGridLayout()
            self.iconsCont
            self.layout.addLayout(self.iconsCont)
            self.render_icons()
            self.layout.addStretch()
    
    def render_icons(self):
        clearLayout(self.iconsCont)
        MAX_COLS = 5
        r = 0
        c = 0
        if len(os.listdir(f"{data_file["tdfolder"]}\\icons\\")) == 0:
            self.iconsCont.addWidget(QtWi.QLabel("You have no custom icons. Click \"open icon folder\" to add some.",alignment=QtC.Qt.AlignmentFlag.AlignTop))
        else:
            for filename in os.listdir(f"{data_file["tdfolder"]}\\icons\\"):
                self.iconsCont.addWidget(
                    IconCard(f"{f"{data_file["tdfolder"]}\\icons\\"}{filename}"),
                    r,
                    c
                )
                c+= 1
                if c >= MAX_COLS:
                    r += 1
                    c = 0
    @QtC.Slot()
    def updSetupLayout(self):
        self.setupState += 1
        match self.setupState:
            case 1:
                clearLayout(self.layout)
                self.title = QtWi.QLabel("locate your tride dash installation",
                                         alignment=QtC.Qt.AlignmentFlag.AlignHCenter)
                self.title.setFont(self.h1)
                self.errorMsg = QtWi.QLabel("",
                                         alignment=QtC.Qt.AlignmentFlag.AlignHCenter)
                self.pickfilebtn = QtWi.QPushButton("choose a file")
                self.pickfilebtn.clicked.connect(self.openTDLocator)
                self.layout.addWidget(self.title)
                self.layout.addWidget(self.errorMsg)
                self.layout.addWidget(self.pickfilebtn)
    @QtC.Slot()
    def openTDLocator(self):
        self.tdFPath, _ = QtWi.QFileDialog.getOpenFileName(
            self,
            "Select Tride Dash Installation",
            "",
            "Tride Dash Executable (*.exe)")
        if self.tdFPath:
            print(self.tdFPath)
            self.errorMsg.setFont(self.h1)
            if not str(self.tdFPath).endswith("Tride Dash.exe"):
                self.errorMsg.setStyleSheet("color: red;")
                self.errorMsg.setText("ERROR! Not a tride dash installation")
            else:
                self.errorMsg.setStyleSheet("color: black;")
                self.errorMsg.setText("Success")
                data_file["tdfolder"] = "\\".join(str(self.tdFPath).split("/")[:-1])
                clearLayout(self.layout)
                self.title = QtWi.QLabel("setup done, reload application",
                                         alignment=QtC.Qt.AlignmentFlag.AlignHCenter)
                self.title.setFont(self.h1)
                self.layout.addWidget(self.title)
                subprocess.Popen(f"copy {data_file["tdfolder"]}\\Tride Dash_Data\\sharedassets1.assets {data_file["tdfolder"]}\\Tride Dash_Data\\sharedassets1.bak")
                os.mkdir(f"{data_file["tdfolder"]}\\icons")
                os.makedirs(data_folder)
                with open(conf_file, "wt") as conf:
                    conf.write(
                        json.dumps(data_file)
                    )
                    print(f"conf saved to {conf_file}")
                    conf.close()

dark_styles = """
QWidget {
    background-color: #333343;
    color: white;
}

QPushButton {
    background: #222233;
    border: 1px solid #aaaaaa;
    border-radius: 2px;
    color: white;
}
QPushButton:hover {
    background: #33333d;
    color: white;
    border: 1px solid #999999
}
"""

if __name__ == "__main__":
    app = QtWi.QApplication([])
    app.setStyleSheet(dark_styles)
    if not os.path.exists(f"{data_folder}\\conf.json"):
        initialised = False
        print("Starting setup process...")
    win = QtWi.QMainWindow()
    win.setGeometry(100, 100,800, 650)
    win.setWindowTitle("td!Custom Icons")
    win.setCentralWidget(MyWidget())
    win.show()
    sys.exit(app.exec())