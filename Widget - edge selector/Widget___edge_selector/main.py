from maya import cmds, OpenMayaUI

if int(cmds.about(v=1)) < 2017:
    from PySide import QtGui, QtCore
    import shiboken
    from PySide.QtGui import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QColor, QLabel, \
        QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu, QCursor, QMessageBox, QBrush, \
        QSplitter, \
        QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QDoubleValidator, QSlider, \
        QIntValidator, \
        QImage, QPixmap, QTransform, QPaintEvent, QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, \
        QGroupBox, QAction, \
        QFont, QGridLayout, QSpinBox
else:
    from PySide2 import QtGui, QtCore, QtWidgets
    import shiboken2 as shiboken
    from PySide2.QtWidgets import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QVBoxLayout, QLabel, \
        QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu, QMessageBox, QSplitter, \
        QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QSlider, \
        QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox, QAction, QGridLayout, QSpinBox

    from PySide2.QtGui import QColor, QCursor, QBrush, QDoubleValidator, QIntValidator, QImage, QPixmap, QTransform, \
        QPaintEvent, QFont


import commands, base


class Widget_interval( QWidget, base.Cmds_widgetInfo ):

    def __init__(self, *args, **kwargs ):

        labelName = ''
        if kwargs.has_key( 'label' ):
            labelName = kwargs.pop( 'label' )
        self.path_uiInfo = base.basePath + "/Widget_interval_%s.uiInfo" % labelName

        super( Widget_interval, self ).__init__( *args, **kwargs )
        mainLayout = QHBoxLayout( self ); mainLayout.setContentsMargins( 0,0,0,0 ); mainLayout.setSpacing( 10 )
        label = QLabel( labelName )
        label.setAlignment( label.alignment() | QtCore.Qt.AlignRight )
        spinBox = QSpinBox( )
        mainLayout.addWidget( label )
        mainLayout.addWidget( spinBox )

        self.spinBox = spinBox
        spinBox.setMinimum( 1 )
        spinBox.valueChanged.connect( self.cmd_valueChanged )

        value = self.readData( 'index', self.path_uiInfo )
        if type( value ) == int:
            self.spinBox.setValue( value )

    def cmd_valueChanged( self, index ):
        self.writeData( 'index', self.spinBox.value(), self.path_uiInfo )



class Widget_buttons( QWidget ):

    def __init__(self, *args, **kwargs ):

        super( Widget_buttons, self ).__init__( *args, **kwargs )
        mainLayout = QGridLayout( self ); mainLayout.setContentsMargins( 0,0,0,0 ); mainLayout.setSpacing( 5 )

        b_selNext = QPushButton("Select Next")
        b_selPrev = QPushButton("Select Previous")
        b_addNext = QPushButton("Add Next")
        b_addPrev = QPushButton("Add Previous")
        b_selAll  = QPushButton( "Select All" )

        mainLayout.addWidget(b_selNext, 0, 0)
        mainLayout.addWidget(b_selPrev, 0, 1)
        mainLayout.addWidget(b_addNext, 1, 0)
        mainLayout.addWidget(b_addPrev, 1, 1)
        mainLayout.addWidget(b_selAll, 0, 2, 2, 1 )
        self.lastEdge = None

        b_selNext.clicked.connect(self.cmd_selectNextEdge)
        b_selPrev.clicked.connect(self.cmd_selectPrevEdge)
        b_addNext.clicked.connect(self.cmd_addNextEdge)
        b_addPrev.clicked.connect(self.cmd_addPrevEdge)
        b_selAll.clicked.connect( self.cmd_selectAll )


    def cmd_selectNextEdge(self):
        selNum  = Window.currentInstance.w_selectNum.spinBox.value()
        skipNum = Window.currentInstance.w_skipNum.spinBox.value()

        import pymel.core
        if self.lastEdge:
            pymel.core.select( self.lastEdge )
        sels = pymel.core.ls(sl=1)
        meshName = sels[0].node().name()
        edgeIndex = sels[0].index()
        inst = commands.EdgeSelector(meshName, edgeIndex)
        lastEdge = inst.selectNextEdge(selNum, skipNum)


    def cmd_selectPrevEdge(self):
        selNum  = Window.currentInstance.w_selectNum.spinBox.value()
        skipNum = Window.currentInstance.w_skipNum.spinBox.value()

        import pymel.core
        if self.lastEdge:
            pymel.core.select( self.lastEdge )
        sels = pymel.core.ls(sl=1)
        meshName = sels[0].node().name()
        edgeIndex = sels[0].index()
        inst = commands.EdgeSelector(meshName, edgeIndex)
        lastEdge = inst.selectPrevEdge(selNum, skipNum)


    def cmd_addNextEdge(self):
        selNum  = Window.currentInstance.w_selectNum.spinBox.value()
        skipNum = Window.currentInstance.w_skipNum.spinBox.value()

        import pymel.core
        if self.lastEdge:
            pymel.core.select( self.lastEdge )
        sels = pymel.core.ls(sl=1)
        meshName = sels[0].node().name()
        edgeIndex = sels[0].index()
        inst = commands.EdgeSelector(meshName, edgeIndex)
        lastEdge = inst.addNextEdge(selNum, skipNum)


    def cmd_addPrevEdge(self):
        selNum  = Window.currentInstance.w_selectNum.spinBox.value()
        skipNum = Window.currentInstance.w_skipNum.spinBox.value()

        import pymel.core
        if self.lastEdge:
            pymel.core.select( self.lastEdge )
        sels = pymel.core.ls(sl=1)
        meshName = sels[0].node().name()
        edgeIndex = sels[0].index()
        inst = commands.EdgeSelector(meshName, edgeIndex)
        lastEdge = inst.addPrevEdge(selNum, skipNum)


    def cmd_selectAll(self):
        import pymel.core
        selNum = Window.currentInstance.w_selectNum.spinBox.value()
        skipNum = Window.currentInstance.w_skipNum.spinBox.value()
        sels = pymel.core.ls(sl=1)
        meshName = sels[0].node().name()
        edgeIndex = sels[0].index()
        inst = commands.EdgeSelector(meshName, edgeIndex, [] )
        inst.selectAllEdges( selNum, skipNum )




class Window( QDialog, base.Cmds_widgetInfo ):

    mayawin = shiboken.wrapInstance( long( OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    defaultSize = [ 400, 100 ]
    path_uiInfo = base.basePath + "/Window.uiInfo"
    title = "Widget - Edge Selector"
    objectName = "widget__edge_selector"
    currentInstance = None

    def __init__(self, *args, **kwargs ):

        Window.currentInstance = self

        existing_widgets = Window.mayawin.findChildren(QWidget, self.objectName)
        if existing_widgets: map(lambda x: x.deleteLater(), existing_widgets)

        super( Window, self ).__init__( *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Window.title )
        self.setObjectName( Window.objectName )

        mainLayout = QVBoxLayout( self )

        w_interVal = QWidget()
        lay_interVal = QHBoxLayout( w_interVal ); lay_interVal.setContentsMargins( 0,0,0,0 ); lay_interVal.setSpacing( 15 )
        w_selectNum = Widget_interval( self, label="Select num" )
        w_skipNum = Widget_interval( self, label="Skip num" )
        lay_interVal.addWidget( w_selectNum )
        lay_interVal.addWidget( w_skipNum )
        label = QLabel( "ABC")
        mainLayout.addWidget( w_interVal )

        separator = base.Widget_Separator( self )
        mainLayout.addWidget( separator )

        w_buttons = Widget_buttons( self )
        mainLayout.addWidget( w_buttons )

        self.w_selectNum = w_selectNum
        self.w_skipNum   = w_skipNum

        self.resize( *Window.defaultSize )
        self.load_shapeInfo( Window.path_uiInfo )


    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type( ) in [ QtCore.QEvent.Resize, QtCore.QEvent.Move ]:
            try:self.save_shapeInfo( Window.path_uiInfo )
            except:pass


def show( evt=0 ):
    Window( Window.mayawin ).show()