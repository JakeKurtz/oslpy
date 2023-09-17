class Opcode():
    def __init__(self, OSO, index):
        self.OSO = OSO
        self.InstructionIndex = index
        self.Instuction = self.OSO.Instructions[index]
        self.Tag = self.OSO.Instructions[index].Tag

    def Instruction(self):
        return self.Instruction

    def InstructionIndex(self):
        return self.InstructionIndex

    def NextIndex(self):
        return self.InstructionIndex + 1

    def Tag(self):
        return self.Tag

    def Generate(self, nodeGraph):
        print("Generate not implemented for %s" % self.Instuction.Opcode)


# Destination Source
class Opcode_DS(Opcode):
    def __init__(self, OSO, index):
        Opcode.__init__(self, OSO, index)
        self.Destination = OSO.GetVariable(self.Instuction.Parameters[0])
        self.Source = OSO.GetVariable(self.Instuction.Parameters[1])

    def Destination(self):
        return self.Destination

    def Source(self):
        return self.Source

class Opcode_D(Opcode):
    def __init__(self, OSO, index):
        Opcode.__init__(self, OSO, index)
        self.Destination = OSO.GetVariable(self.Instuction.Parameters[0])
        
    def Destination(self):
        return self.Destination

# Destination Source1 Source2


class Opcode_DSS(Opcode):
    def __init__(self, OSO, index):
        Opcode.__init__(self, OSO, index)
        self.Destination = OSO.GetVariable(self.Instuction.Parameters[0])
        self.Source1 = OSO.GetVariable(self.Instuction.Parameters[1])
        self.Source2 = OSO.GetVariable(self.Instuction.Parameters[2])

    def Destination(self):
        return self.Destination

    def Source1(self):
        return self.Source1

    def Source2(self):
        return self.Source2


class Opcode_SDD(Opcode):
    def __init__(self, OSO, index):
        Opcode.__init__(self, OSO, index)
        self.Source = OSO.GetVariable(self.Instuction.Parameters[0])
        self.Destination1 = OSO.GetVariable(self.Instuction.Parameters[1])
        self.Destination2 = OSO.GetVariable(self.Instuction.Parameters[2])

    def Destination1(self):
        return self.Destination1

    def Destination2(self):
        return self.Destination2

    def Source(self):
        return self.Source


# Destination Source1 Source2
class Opcode_DSSS(Opcode):
    def __init__(self, OSO, index):
        Opcode.__init__(self, OSO, index)
        self.Destination = OSO.GetVariable(self.Instuction.Parameters[0])
        self.Source1 = OSO.GetVariable(self.Instuction.Parameters[1])
        self.Source2 = OSO.GetVariable(self.Instuction.Parameters[2])
        self.Source3 = OSO.GetVariable(self.Instuction.Parameters[3])

    def Destination(self):
        return self.Destination

    def Source1(self):
        return self.Source1

    def Source2(self):
        return self.Source2

    def Source3(self):
        return self.Source3

# Destination Source1 index


class Opcode_DSI(Opcode):
    def __init__(self, OSO, index):
        Opcode.__init__(self, OSO, index)
        self.Destination = OSO.GetVariable(self.Instuction.Parameters[0])
        self.Source = OSO.GetVariable(self.Instuction.Parameters[1])
        self.Index = OSO.GetVariable(self.Instuction.Parameters[2])

    def Destination(self):
        return self.Destination

    def Source(self):
        return self.Source1

    def Index(self):
        return self.Index


class Opcode_DIS(Opcode):
    def __init__(self, OSO, index):
        Opcode.__init__(self, OSO, index)
        self.Destination = OSO.GetVariable(self.Instuction.Parameters[0])
        self.Index = OSO.GetVariable(self.Instuction.Parameters[1])
        self.Source = OSO.GetVariable(self.Instuction.Parameters[2])

    def Destination(self):
        return self.Destination

    def Source(self):
        return self.Source

    def Index(self):
        return self.Index


class Opcode_basicMath(Opcode_DSS):
    def __init__(self, OSO, index, operation):
        Opcode_DSS.__init__(self, OSO, index)
        self.Operation = operation

    def GenerateFloatFloat(self, nodeGraph):
        node = nodeGraph.CreateNode("ShaderNodeMath")
        node.SetProperty("operation", self.Operation)
        nodeGraph.AddLink(node, 0, self.Source1)
        nodeGraph.AddLink(node, 1, self.Source2)
        nodeGraph.SetVar(self.Destination, node, 0)

    def GeneratePointPoint(self, nodeGraph):
        node = nodeGraph.CreateNode("ShaderNodeVectorMath")
        if self.Operation in ['ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'CROSS_PRODUCT', 'PROJECT', 'REFLECT', 'DOT_PRODUCT', 'DISTANCE', 'MINIMUM', 'MAXIMUM', 'MODULO', 'SNAP', ]:
            node.SetProperty("operation", self.Operation)
            nodeGraph.AddLink(node, 0, self.Source1)
            nodeGraph.AddLink(node, 1, self.Source2)
            nodeGraph.SetVar(self.Destination, node, 0)
        else:
            raise ValueError(str('Unsupported math operation %s %s %s' % (
                self.Source1.dataType, self.Operation, self.Source2.dataType)))

    def GeneratePointFloat(self, nodeGraph, vec, flt):
        node = nodeGraph.CreateNode("ShaderNodeVectorMath")
        node.SetProperty("operation", self.Operation)
        nodeGraph.AddLink(node, 0, self.Source1)
        nodeGraph.AddLink(node, 1, self.Source2)
        nodeGraph.SetVar(self.Destination, node, 0)

    def GenerateFloatPoint(self, nodeGraph):
        node = nodeGraph.CreateNode("ShaderNodeVectorMath")
        node.SetProperty("operation", self.Operation)
        nodeGraph.AddLink(node, 0, self.Source1)
        nodeGraph.AddLink(node, 1, self.Source2)
        nodeGraph.SetVar(self.Destination, node, 0)

    def Generate(self, nodeGraph):
        if self.Source1.IsNumeric() and self.Source2.IsNumeric():
            self.GenerateFloatFloat(nodeGraph)
        elif self.Source1.IsNumeric() and self.Source2.IsPointLike():
            self.GenerateFloatPoint(nodeGraph)
        elif self.Source1.IsPointLike() and self.Source2.IsNumeric():
            self.GeneratePointFloat(nodeGraph, self.Source1, self.Source2)
        elif self.Source1.IsPointLike() and self.Source2.IsPointLike():
            self.GeneratePointPoint(nodeGraph)
        else:
            raise ValueError(str('Unsupported math operation %s %s %s' % (
                self.Source1.dataType, self.Operation, self.Source2.dataType)))

class Opcode_basicMath1(Opcode_DS):
    def __init__(self, OSO, index, operation):
        Opcode_DS.__init__(self, OSO, index)
        self.Operation = operation

    def GenerateFloat(self, nodeGraph):
        node = nodeGraph.CreateNode("ShaderNodeMath")
        if self.Operation in ['SQRT', 'INVERSE_SQRT', 'ABSOLUTE', 'EXPONENT', 'SIGN', 'FLOOR', 'CEIL', 'TRUNCATE', 'FRACT', 'SINE', 'COSINE', 'TANGENT', 'ARCSINE', 'ARCCOSINE', 'ARCTANGENT', 'ARCTAN2', 'SINH', 'COSH', 'TANH', 'RADIANS', 'DEGREES']:
            node.SetProperty("operation", self.Operation)
            nodeGraph.AddLink(node, 0, self.Source)
            nodeGraph.SetVar(self.Destination, node, 0)
        else:
            raise ValueError(str('Unsupported math operation %s %s' % (
                self.Source.dataType, self.Operation)))

    def GeneratePoint(self, nodeGraph):
        node = nodeGraph.CreateNode("ShaderNodeVectorMath")
        if self.Operation in ['LENGTH', 'NORMALIZE', 'ABSOLUTE', 'FLOOR', 'CEIL', 'FRACTION', 'SINE', 'COSINE', 'TANGENT']:
            node.SetProperty("operation", self.Operation)
            nodeGraph.AddLink(node, 0, self.Source)
            nodeGraph.SetVar(self.Destination, node, 0)
        else:
            raise ValueError(str('Unsupported math operation %s %s' % (
                self.Source.dataType, self.Operation)))

    def Generate(self, nodeGraph):
        if self.Source.IsNumeric():
            self.GenerateFloat(nodeGraph)
        elif self.Source.IsPointLike():
            self.GeneratePoint(nodeGraph)
        else:
            raise ValueError(str('Unsupported math operation %s %s' %
                                 (self.Source.dataType, self.Operation)))
