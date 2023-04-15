import os
from pyteal import *
# 60 bytes per record

@Subroutine(TealType.bytes)
def getBox( X, Y ):
    # 0 0 = 0 + 11 * 0
    # 4534 2574 = 4 + 11 * 2 = 26
    # 4109 1427 = 4 + 11 * 1 = 15
    # 8634 1937 = 9 + 11 * 2 = 31
    # 10000 10000 = 10 + 11 * 10 = 120
    return Itob( X / Int(910) + Int(11) * ( Y / Int(910) ) )
    

def approval_program():
    is_creator = Txn.sender() == Global.creator_address()


    X = Btoi(Txn.application_args[5])
    Y = Btoi(Txn.application_args[6])
    boxname = getBox(X,Y)
    contents2 = App.box_get(boxname)
    index=Btoi(Substring(contents2.value(),Int(0),Int(8)))
    indexPlus1=Btoi(Substring(contents2.value(),Int(0),Int(8)))+Int(1)
    #nameFormatted = Concat(Bytes("            "), Txn.application_args[1])
    #data = Concat(Substring(nameFormatted,Len(nameFormatted) - Int(12), Int(12)),Txn.application_args[2] ,Txn.application_args[3],Txn.application_args[4],Txn.application_args[5],Txn.application_args[6],Txn.application_args[7])
    data = Concat(Txn.application_args[1], Txn.application_args[2], Txn.application_args[3], Txn.application_args[4], Txn.application_args[5], Txn.application_args[6], Txn.application_args[7])

    AddMonster = Seq(
        [
            Assert(is_creator),
            Assert(Len(Txn.application_args[2]) == Int(8)),
            Assert(Len(Txn.application_args[3]) == Int(8)),
            Assert(Len(Txn.application_args[4]) == Int(8)),
            Assert(Len(Txn.application_args[5]) == Int(8)),
            Assert(Len(Txn.application_args[6]) == Int(8)),
            Assert(Len(Txn.application_args[7]) == Int(8)),
            contents := App.box_get(boxname),
            If(Not(contents.hasValue()),
                Seq([
                    Assert(App.box_create(boxname, Int(4000))),
                    contents := App.box_get(boxname),
                    App.box_replace(boxname, Int(0), Itob(Int(0))),
                ])
            ),
            contents2,
            Assert(contents2.hasValue()),
            
            App.box_replace(boxname, Int(0), Itob(indexPlus1)),
            Assert(Len(data) == Int(60)),
            App.box_replace(boxname, index * Int(60) + Int(8), data),
            
            Return(Int(1))
        ]
    )



    FindX = Btoi(Txn.application_args[1])
    FindY = Btoi(Txn.application_args[2])
    FindInBoxname = getBox(FindX,FindY)
    FindContents = App.box_get(FindInBoxname)
    MaxIndex = Btoi(Substring(FindContents.value(),Int(0),Int(8)))
    Radius = Btoi(Txn.application_args[3])
    FindXMin = If(FindX > Radius, FindX, Int(0))
    FindXMax = If(FindX + Radius < Int(10000), FindX + Radius, Int(10000))
    FindYMin = If(FindY > Radius, FindY, Int(0))
    FindYMax = If(FindY + Radius < Int(10000), FindY + Radius, Int(10000))
    i = ScratchVar(TealType.uint64)
    storedX =Btoi(App.box_extract(FindInBoxname, i.load() * Int(60) + Int(8+12+3*8), Int(8)))
    storedY =Btoi(App.box_extract(FindInBoxname, i.load() * Int(60) + Int(8+12+4*8), Int(8)))
    storedObject =App.box_extract(FindInBoxname, i.load() * Int(60) + Int(8), Int(60))
    storedXScratch = ScratchVar(TealType.uint64)
    storedYScratch = ScratchVar(TealType.uint64)
    FindMonstersInLocation = Seq(
        [
            FindContents,
            For(i.store(Int(0)), i.load() < MaxIndex, i.store(i.load() + Int(1))).Do(
                Seq([
                    storedXScratch.store(storedX),
                    storedYScratch.store(storedY),
                    If(And(storedXScratch.load() >= FindXMin, storedXScratch.load() <= FindXMax, storedYScratch.load() >= FindYMin, storedYScratch.load() <= FindYMax) , Log(storedObject)),
                ])
            ),
            Return(Int(1)),
        ]
    )

    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.application_args[0] == Bytes("NONE"), Approve()],
        [Txn.application_args[0] == Bytes("CREATE"), AddMonster],
        [Txn.application_args[0] == Bytes("LOOKUP_BY_LOC"), FindMonstersInLocation],
    )

    return program


def clear_state_program():
    return Approve()


APPROVAL_SRC = os.path.join('.', 'contracts', "BoxBasedDB_ApprovalProgram.teal")
CLEARSTATE_SRC = os.path.join('.', 'contracts', "BoxBasedDB_ClearStateProgram.teal")

if __name__ == "__main__":
    with open(APPROVAL_SRC, "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=8)
        f.write(compiled)

    with open(CLEARSTATE_SRC, "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=8)
        f.write(compiled)