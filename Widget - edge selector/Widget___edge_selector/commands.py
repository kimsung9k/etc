from maya import cmds, OpenMaya, mel
import pymel.core
import copy


class EdgeSelector():

    @staticmethod
    def getMObject( meshName ):

        oNode = OpenMaya.MObject()
        selList = OpenMaya.MSelectionList()
        selList.add( meshName )
        selList.getDependNode( 0, oNode )
        return oNode


    def __init__(self, mesh, baseIndex, prevEdgeIndex=None ):

        self.baseIndex = baseIndex
        self.prevIndex = prevEdgeIndex
        self.meshName = mesh
        self.oMesh = EdgeSelector.getMObject( self.meshName )
        self.fnMesh = OpenMaya.MFnMesh( self.oMesh )
        self.itMeshEdge = OpenMaya.MItMeshEdge( self.oMesh )
        self.itMeshPolygon = OpenMaya.MItMeshPolygon( self.oMesh )
        self.checkedEdgeList = []


    def getSideEdges(self, edgeIndex ):

        util = OpenMaya.MScriptUtil()
        util.createFromInt(0)
        self.ptrIndex = util.asIntPtr()

        self.itMeshEdge.setIndex( edgeIndex, self.ptrIndex)
        intArrFaceIndices = OpenMaya.MIntArray()
        intArrEdgeIndices = OpenMaya.MIntArray()
        self.itMeshEdge.getConnectedFaces( intArrFaceIndices )
        self.itMeshEdge.getConnectedEdges( intArrEdgeIndices )
        connectedFaces = [intArrFaceIndices[i] for i in range(intArrFaceIndices.length())]
        connectedEdges = [ intArrEdgeIndices[i] for i in range(intArrEdgeIndices.length())]

        sideEdges = []
        for fIndex in connectedFaces:
            self.itMeshPolygon.setIndex(fIndex, self.ptrIndex )
            edgeIndices = OpenMaya.MIntArray()
            self.itMeshPolygon.getEdges( edgeIndices )
            edgeIndices = [ edgeIndices[i] for i in range( edgeIndices.length() ) ]
            for eIndex in edgeIndices:
                if eIndex in connectedEdges: continue
                if eIndex == edgeIndex: continue
                if eIndex in sideEdges: continue
                sideEdges.append( eIndex )
        return sideEdges


    def getNextEdge(self, currentIndex=None, prevIndex=None ):
        if not currentIndex: currentIndex = self.baseIndex
        sideEdges = self.getSideEdges(currentIndex)
        if len( sideEdges ) > 2: return None
        nextEdge = None
        for sideEdge in sideEdges:
            if self.prevIndex == sideEdge: continue
            if prevIndex == sideEdge: continue
            nextEdge = sideEdge
            break
        self.checkedEdgeList.append(nextEdge)
        return nextEdge


    def getPrevEdge(self, currentIndex=None, prevIndex=None ):
        if not currentIndex: currentIndex = self.baseIndex
        sideEdges = self.getSideEdges(currentIndex)
        if len(sideEdges) > 2: return None
        prevEdge = None
        if type( self.prevIndex ) == int:
            for sideEdge in sideEdges:
                if self.prevIndex == sideEdge: continue
                if prevIndex == sideEdge: continue
                prevEdge = sideEdge
                break
        else:
            if len( sideEdges ) == 1:
                prevEdge = sideEdges[0]
            else:
                prevEdge = sideEdges[1]
        self.checkedEdgeList.append( prevEdge )
        return prevEdge


    def selectAllEdges(self, selNum, skipNum ):

        import pymel.core
        def getIntervaledIndicesNext( startIndex, prevEdge=None ):
            nextEdge = startIndex
            selEdges = [startIndex]
            for i in range(selNum-1):
                keepPrev = copy.copy(nextEdge)
                nextEdge = self.getNextEdge(nextEdge, prevEdge)
                selEdges.append(nextEdge)
                prevEdge = keepPrev
            for i in range(skipNum+1):
                keepPrev = copy.copy(nextEdge)
                nextEdge = self.getNextEdge(nextEdge, prevEdge)
                prevEdge = keepPrev
            return selEdges, nextEdge, prevEdge

        def getIntervaledIndicesPrev( startIndex, prevEdge=None ):
            nextEdge = startIndex
            for i in range(skipNum):
                keepPrev = copy.copy(nextEdge)
                nextEdge = self.getPrevEdge(nextEdge, prevEdge)
                prevEdge = keepPrev
            selEdges = []
            for i in range(selNum):
                keepPrev = copy.copy(nextEdge)
                nextEdge = self.getPrevEdge(nextEdge, prevEdge)
                selEdges.append(nextEdge)
                prevEdge = keepPrev
            return selEdges, self.getNextEdge( selEdges[-1] )

        startIndex = self.baseIndex
        resultSelEdges = []
        maxIndex = 100
        currentIndex = 0
        prevEdge = None
        while True:
            currentList = copy.copy( self.checkedEdgeList )
            selEdges, startIndex, prevEdge = getIntervaledIndicesNext( startIndex, prevEdge )
            if startIndex in currentList:
                break
            resultSelEdges += selEdges
            currentIndex+=1
            if currentIndex > maxIndex: break
        startIndex = self.baseIndex
        breakLoop = False

        selEdgeNames = []
        for selEdge in resultSelEdges:
            if type( selEdge ) != int: continue
            selEdgeNames.append( self.meshName + '.e[%d]' % selEdge )
        pymel.core.select( selEdgeNames )


    def selectNextEdge(self, selNum, intervalNum ):
        prevEdge = None
        nextEdge = self.baseIndex
        for i in range( intervalNum ):
            keepPrev = copy.copy( nextEdge )
            nextEdge = self.getNextEdge( nextEdge, prevEdge )
            prevEdge = keepPrev
        selEdges = []
        for i in range( selNum ):
            keepPrev = copy.copy(nextEdge)
            nextEdge = self.getNextEdge(nextEdge, prevEdge)
            selEdges.append( nextEdge )
            prevEdge = keepPrev

        edgeNames = []
        for indexEdge in selEdges:
            edgeNames.append( self.meshName + '.e[%d]' % indexEdge )
        pymel.core.select( edgeNames )
        return edgeNames[-1]


    def selectPrevEdge(self, selNum, intervalNum ):
        prevEdge = None
        nextEdge = self.baseIndex
        for i in range( intervalNum ):
            keepPrev = copy.copy( nextEdge )
            nextEdge = self.getPrevEdge( nextEdge, prevEdge )
            prevEdge = keepPrev
        selEdges = []
        for i in range( selNum ):
            keepPrev = copy.copy(nextEdge)
            nextEdge = self.getPrevEdge(nextEdge, prevEdge)
            selEdges.append( nextEdge )
            prevEdge = keepPrev

        edgeNames = []
        for indexEdge in selEdges:
            edgeNames.append( self.meshName + '.e[%d]' % indexEdge )
        pymel.core.select( edgeNames )
        return edgeNames[-1]

    def addNextEdge(self, selNum, intervalNum ):
        prevEdge = None
        nextEdge = self.baseIndex
        for i in range( intervalNum ):
            keepPrev = copy.copy( nextEdge )
            nextEdge = self.getNextEdge( nextEdge, prevEdge )
            prevEdge = keepPrev
        selEdges = []
        for i in range( selNum ):
            keepPrev = copy.copy(nextEdge)
            nextEdge = self.getNextEdge(nextEdge, prevEdge)
            selEdges.append( nextEdge )
            prevEdge = keepPrev

        edgeNames = []
        for indexEdge in selEdges:
            edgeNames.append( self.meshName + '.e[%d]' % indexEdge )
        pymel.core.select( edgeNames, add=1 )
        return edgeNames[-1]


    def addPrevEdge(self, selNum, intervalNum ):
        prevEdge = None
        nextEdge = self.baseIndex
        for i in range( intervalNum ):
            keepPrev = copy.copy( nextEdge )
            nextEdge = self.getPrevEdge( nextEdge, prevEdge )
            prevEdge = keepPrev
        selEdges = []
        for i in range( selNum ):
            keepPrev = copy.copy(nextEdge)
            nextEdge = self.getPrevEdge(nextEdge, prevEdge)
            selEdges.append( nextEdge )
            prevEdge = keepPrev

        edgeNames = []
        for indexEdge in selEdges:
            edgeNames.append( self.meshName + '.e[%d]' % indexEdge )
        pymel.core.select( edgeNames, add=1 )
        return edgeNames[-1]



