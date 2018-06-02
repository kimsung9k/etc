from maya import cmds, OpenMaya, OpenMayaUI, mel

if int(cmds.about(v=1)) < 2017:
    import shiboken
    from PySide import QtCore
    from PySide.QtGui import QPixmap, QImage, QLabel, QCursor, QPaintEvent, QFrame
    from PySide.QtCore import QFile, QIODevice
else:
    import shiboken2 as shiboken
    from PySide2 import QtCore
    from PySide2.QtGui import QPixmap, QImage, QPaintEvent, QCursor
    from PySide2.QtWidgets import QLabel, QFrame
    from PySide2.QtCore import QFile, QIODevice

import json, os

basePath = cmds.about(pd=1) + "/widget___edge_selector"

class Cmds_widgetInfo(object):

    def __init__(self, *args, **kwargs):
        pass


    def makeFolder(self, pathName):
        if os.path.exists(pathName) and os.path.isdir( pathName ): return None
        os.makedirs(pathName)
        return pathName


    def makeFile(self, filePath):
        if os.path.exists(filePath): return None
        filePath = filePath.replace("\\", "/")
        splits = filePath.split('/')
        folder = '/'.join(splits[:-1])
        self.makeFolder(folder)
        f = open(filePath, "w")
        json.dump({}, f)
        f.close()


    def writeData(self, key, value, filePath):
        self.makeFile(filePath)
        f = open( filePath, 'r' )
        data = json.load(f)
        f.close()
        data[ key ] = value
        f = open(filePath, 'w')
        json.dump(data, f, indent=2)
        f.close()


    def readData(self, key, filePath):
        self.makeFile(filePath)
        f = open(filePath, 'r')
        data = json.load(f)
        f.close()
        if data.has_key( key ):
            return data[ key ]


    def writeDatas(self, dictValues, filePath):
        self.makeFile(filePath)

        f = open( filePath, 'r' )
        data = json.load( f )
        f.close()
        data.update( dictValues )
        f = open(filePath, 'w')
        json.dump(data, f, indent=2)
        f.close()


    def readDatas(self, keys, filePath):
        self.makeFile( filePath )
        f = open( filePath, 'r' )
        data = json.load(f)
        f.close()
        values = []
        for key in keys:
            if data.has_key( key ):
                values.append( data[key] )
            else:
                values.append( None )
        return values


    def setPositionByCursor(self, offsetX=0, offsetY=0 ):
        if not offsetX: offsetX = 0
        if not offsetY: offsetY = 0
        pos = QCursor.pos()
        self.move( pos.x()+offsetX, pos.y()+offsetY )


    def save_shapeInfo(self, path):
        self.writeDatas( dict( x= self.x(), y= self.y(), width= self.width(), height= self.height() ), path )


    def load_shapeInfo(self, path):

        x, y, width, height = self.readDatas(['x','y','width','height'],path)
        try:self.move(x, y)
        except:pass
        try:self.resize(width, height)
        except:pass


    def resetPositionByParent(self):

        diffWidth  = self.width()  - self.parentWidget().width()
        diffHeight = self.height() - self.parentWidget().height()
        self.move(self.parentWidget().x() - diffWidth * 0.5, self.parentWidget().y() - diffHeight * 0.5 )


    def getWidgetInfomationPath(self, baseDirectory ):
        return baseDirectory + '/' + self.__class__.__name__ + '.txt'


    def getObjectName(self, baseObjectName ):
        return baseObjectName + '_' + self.__class__.__name__.lower()


    def get_csv_form_google_spreadsheets( self, url, targetPath ):

        import re, urllib, urllib2, os, ssl
        p = re.compile('/d/.+/')
        m = p.search(url)
        id_sheet = m.group()[3:-1]
        dirPath = os.path.dirname(targetPath)
        if not os.path.exists(dirPath): os.makedirs( dirPath )
        link_donwload_attributeList = 'https://docs.google.com/spreadsheets/d/%s/export?format=csv' % id_sheet
        try:
            context = ssl._create_unverified_context()
            response = urllib2.urlopen(link_donwload_attributeList,
                                       context=context)  # How should i pass authorization details here?
            data = response.read()
            f = open(targetPath, 'w')
            f.write(data)
            f.close()
        except:
            testfile = urllib.URLopener()
            testfile.retrieve(link_donwload_attributeList, targetPath)



class Widget_Separator( QFrame ):

    def __init__(self, *args, **kwargs ):
        super( Widget_Separator, self ).__init__( *args, **kwargs )
        self.setFrameShape(QFrame.HLine)