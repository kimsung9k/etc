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

        if len( connectedFaces ) > 2: return []

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


    def getNextEdge(self, currentIndex, prevIndex=None ):
        sideEdges = self.getSideEdges(currentIndex)
        if len( sideEdges ) > 2: return None
        nextEdge = None
        for sideEdge in sideEdges:
            if prevIndex == sideEdge: continue
            nextEdge = sideEdge
            break
        return nextEdge


    def getOrderedEdges(self):

        firstIndex = self.baseIndex
        secondIndex = self.getNextEdge(firstIndex)
        checkedList = [firstIndex, secondIndex]

        def isNewIndex(index, checkedList):
            if type(index) != int: return False
            if index in checkedList: return False
            return True

        first = copy.copy(firstIndex)
        second = copy.copy(secondIndex)
        while True:
            next = self.getNextEdge(second, first )
            #print "next f: ", next, checkedList
            if not isNewIndex(next, checkedList): break
            checkedList.append(next)
            first = second
            second = next

        first = copy.copy(secondIndex)
        second = copy.copy(firstIndex)
        while True:
            next = self.getNextEdge(second, first)
            #print "next b: ", next, checkedList
            if not isNewIndex(next, checkedList): break
            checkedList.insert(0, next)
            first = second
            second = next
        return checkedList


    def getIntervaredEdges(self, selNum, skipNum ):
        orderedEdges = self.getOrderedEdges()
        #print "orderedEdges : ", orderedEdges
        rootIndex = orderedEdges.index( self.baseIndex )

        selIndices = []
        currentIndex = copy.copy( rootIndex )
        while True:
            selIndices.append(currentIndex)
            for i in range(selNum - 1):
                currentIndex += 1
                if currentIndex >= len(orderedEdges): break
                selIndices.append(currentIndex)
            for i in range(skipNum + 1):
                currentIndex += 1
                if currentIndex >= len(orderedEdges): break
            if currentIndex >= len(orderedEdges): break

        currentIndex = copy.copy( rootIndex )
        while True:
            for i in range( skipNum ):
                currentIndex -= 1
                if currentIndex <= 0: break
            for i in range( selNum ):
                currentIndex -= 1
                if currentIndex <= 0: break
                selIndices.append(currentIndex)
            if currentIndex <= 0: break
        return [ orderedEdges[i] for i in selIndices ]


    def selectIntervaredEdges(self, selNum, skipNum ):

        from maya import cmds
        indices = self.getIntervaredEdges( selNum, skipNum )
        #print "indices : ", indices
        edges = []
        for index in indices:
            edges.append( self.meshName + '.e[%d]' % index )
        cmds.select( edges )