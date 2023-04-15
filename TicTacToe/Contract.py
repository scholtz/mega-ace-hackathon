import os
from pyteal import * 

@Subroutine(TealType.none)
def copyFromByteField(bytes):
    p11 = ScratchVar(TealType.uint64, 1)
    p12 = ScratchVar(TealType.uint64, 2)
    p13 = ScratchVar(TealType.uint64, 3)
    p21 = ScratchVar(TealType.uint64, 4)
    p22 = ScratchVar(TealType.uint64, 5)
    p23 = ScratchVar(TealType.uint64, 6)
    p31 = ScratchVar(TealType.uint64, 7)
    p32 = ScratchVar(TealType.uint64, 8)
    p33 = ScratchVar(TealType.uint64, 9)
    logic = Seq([
        p11.store(Btoi(Substring(bytes,Int(0),Int(1)))),
        p12.store(Btoi(Substring(bytes,Int(1),Int(2)))),
        p13.store(Btoi(Substring(bytes,Int(2),Int(3)))),
        p21.store(Btoi(Substring(bytes,Int(3),Int(4)))),
        p22.store(Btoi(Substring(bytes,Int(4),Int(5)))),
        p23.store(Btoi(Substring(bytes,Int(5),Int(6)))),
        p31.store(Btoi(Substring(bytes,Int(6),Int(7)))),
        p32.store(Btoi(Substring(bytes,Int(7),Int(8)))),
        p33.store(Btoi(Substring(bytes,Int(8),Int(9)))),
    ])
    return logic

@Subroutine(TealType.bytes)
def updateField(bytes, position, value):
    logic = Seq([
        If(Btoi(Substring(bytes,position - Int(1),position)) == Int(0),
            # store to position user move
            Seq([
                Return(Concat(
                    Substring(bytes,Int(0),position- Int(1)),
                    value,
                    Substring(bytes,position,Int(9)),
                )),
            ])
            ,
            # else bad move
            Return(bytes)
        ),
    ])
    return logic
# returns the position to place (the index + 1)
@Subroutine(TealType.uint64)
def getMyMove(bytes):
    logic = Seq([
        If(Btoi(Substring(bytes,Int(4),Int(5))) == Int(0), # if middle is empty, go there
            Return(Int(5))
        ),
        # be offsensive if we are missing one field to win

        #11,12,13
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "02"), Substring(bytes,Int(1),Int(2)) == Bytes("base16", "02"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "00")),
            Return(Int(3)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "02"), Substring(bytes,Int(1),Int(2)) == Bytes("base16", "00"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "02")),
            Return(Int(2)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "00"), Substring(bytes,Int(1),Int(2)) == Bytes("base16", "02"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "02")),
            Return(Int(1)),
        ),

        # 11,21,31
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "02"), Substring(bytes,Int(3),Int(4)) == Bytes("base16", "02"), Substring(bytes,Int(6),Int(7)) == Bytes("base16", "00")),
            Return(Int(7)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "02"), Substring(bytes,Int(3),Int(4)) == Bytes("base16", "00"), Substring(bytes,Int(6),Int(7)) == Bytes("base16", "02")),
            Return(Int(4)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "00"), Substring(bytes,Int(3),Int(4)) == Bytes("base16", "02"), Substring(bytes,Int(6),Int(7)) == Bytes("base16", "02")),
            Return(Int(1)),
        ),

        # 11,22,33
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "02"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "02"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "00")),
            Return(Int(9)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "02"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "00"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "02")),
            Return(Int(5)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "00"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "02"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "02")),
            Return(Int(1)),
        ),
        # 21,22,23
        If(And(Substring(bytes,Int(3),Int(4)) == Bytes("base16", "02"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "02"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "00")),
            Return(Int(6)),
        ),
        If(And(Substring(bytes,Int(3),Int(4)) == Bytes("base16", "02"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "00"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "02")),
            Return(Int(5)),
        ),
        If(And(Substring(bytes,Int(3),Int(4)) == Bytes("base16", "00"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "02"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "02")),
            Return(Int(4)),
        ),

        # 31,32,33
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "02"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "02"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "00")),
            Return(Int(9)),
        ),
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "02"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "00"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "02")),
            Return(Int(8)),
        ),
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "00"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "02"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "02")),
            Return(Int(7)),
        ),

        # 31,22,13
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "02"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "02"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "00")),
            Return(Int(3)),
        ),
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "02"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "00"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "02")),
            Return(Int(5)),
        ),
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "00"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "02"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "02")),
            Return(Int(7)),
        ),

        # 12,22,32
        If(And(Substring(bytes,Int(1),Int(2)) == Bytes("base16", "02"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "02"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "00")),
            Return(Int(8)),
        ),
        If(And(Substring(bytes,Int(1),Int(2)) == Bytes("base16", "02"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "00"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "02")),
            Return(Int(5)),
        ),
        If(And(Substring(bytes,Int(1),Int(2)) == Bytes("base16", "00"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "02"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "02")),
            Return(Int(2)),
        ),

        # 13,23,33
        If(And(Substring(bytes,Int(2),Int(3)) == Bytes("base16", "02"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "02"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "00")),
            Return(Int(9)),
        ),
        If(And(Substring(bytes,Int(2),Int(3)) == Bytes("base16", "02"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "00"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "02")),
            Return(Int(6)),
        ),
        If(And(Substring(bytes,Int(2),Int(3)) == Bytes("base16", "00"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "02"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "02")),
            Return(Int(3)),
        ),

        # be defensive

        #11,12,13
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "01"), Substring(bytes,Int(1),Int(2)) == Bytes("base16", "01"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "00")),
            Return(Int(3)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "01"), Substring(bytes,Int(1),Int(2)) == Bytes("base16", "00"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "01")),
            Return(Int(2)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "00"), Substring(bytes,Int(1),Int(2)) == Bytes("base16", "01"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "01")),
            Return(Int(1)),
        ),

        # 11,21,31
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "01"), Substring(bytes,Int(3),Int(4)) == Bytes("base16", "01"), Substring(bytes,Int(6),Int(7)) == Bytes("base16", "00")),
            Return(Int(7)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "01"), Substring(bytes,Int(3),Int(4)) == Bytes("base16", "00"), Substring(bytes,Int(6),Int(7)) == Bytes("base16", "01")),
            Return(Int(4)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "00"), Substring(bytes,Int(3),Int(4)) == Bytes("base16", "01"), Substring(bytes,Int(6),Int(7)) == Bytes("base16", "01")),
            Return(Int(1)),
        ),

        # 11,22,33
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "01"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "01"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "00")),
            Return(Int(9)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "01"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "00"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "01")),
            Return(Int(5)),
        ),
        If(And(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "00"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "01"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "01")),
            Return(Int(1)),
        ),
        # 21,22,23
        If(And(Substring(bytes,Int(3),Int(4)) == Bytes("base16", "01"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "01"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "00")),
            Return(Int(6)),
        ),
        If(And(Substring(bytes,Int(3),Int(4)) == Bytes("base16", "01"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "00"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "01")),
            Return(Int(5)),
        ),
        If(And(Substring(bytes,Int(3),Int(4)) == Bytes("base16", "00"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "01"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "01")),
            Return(Int(4)),
        ),

        # 31,32,33
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "01"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "01"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "00")),
            Return(Int(9)),
        ),
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "01"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "00"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "01")),
            Return(Int(8)),
        ),
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "00"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "01"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "01")),
            Return(Int(7)),
        ),

        # 31,22,13
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "01"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "01"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "00")),
            Return(Int(3)),
        ),
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "01"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "00"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "01")),
            Return(Int(5)),
        ),
        If(And(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "00"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "01"), Substring(bytes,Int(2),Int(3)) == Bytes("base16", "01")),
            Return(Int(7)),
        ),

        # 12,22,32
        If(And(Substring(bytes,Int(1),Int(2)) == Bytes("base16", "01"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "01"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "00")),
            Return(Int(8)),
        ),
        If(And(Substring(bytes,Int(1),Int(2)) == Bytes("base16", "01"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "00"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "01")),
            Return(Int(5)),
        ),
        If(And(Substring(bytes,Int(1),Int(2)) == Bytes("base16", "00"), Substring(bytes,Int(4),Int(5)) == Bytes("base16", "01"), Substring(bytes,Int(7),Int(8)) == Bytes("base16", "01")),
            Return(Int(2)),
        ),
        # 13,23,33
        If(And(Substring(bytes,Int(2),Int(3)) == Bytes("base16", "01"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "01"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "00")),
            Return(Int(9)),
        ),
        If(And(Substring(bytes,Int(2),Int(3)) == Bytes("base16", "01"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "00"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "01")),
            Return(Int(6)),
        ),
        If(And(Substring(bytes,Int(2),Int(3)) == Bytes("base16", "00"), Substring(bytes,Int(5),Int(6)) == Bytes("base16", "01"), Substring(bytes,Int(8),Int(9)) == Bytes("base16", "01")),
            Return(Int(3)),
        ),

        # if we do not need to be offensive nor defensive select any

        If(Substring(bytes,Int(4),Int(5)) == Bytes("base16", "01"),
            Seq([
                If(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "00"),
                    Return(Int(1)),
                ),
                If(Substring(bytes,Int(2),Int(3)) == Bytes("base16", "00"),
                    Return(Int(3)),
                ),
                If(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "00"),
                    Return(Int(7)),
                ),
                If(Substring(bytes,Int(8),Int(9)) == Bytes("base16", "00"),
                    Return(Int(9)),
                ),
                If(Substring(bytes,Int(1),Int(2)) == Bytes("base16", "00"),
                    Return(Int(2)),
                ),
                If(Substring(bytes,Int(3),Int(4)) == Bytes("base16", "00"),
                    Return(Int(4)),
                ),
                If(Substring(bytes,Int(5),Int(6)) == Bytes("base16", "00"),
                    Return(Int(6)),
                ),
                If(Substring(bytes,Int(7),Int(8)) == Bytes("base16", "00"),
                    Return(Int(8)),
                ),
            ]),
            Seq([
                If(Substring(bytes,Int(1),Int(2)) == Bytes("base16", "00"),
                    Return(Int(2)),
                ),
                If(Substring(bytes,Int(3),Int(4)) == Bytes("base16", "00"),
                    Return(Int(4)),
                ),
                If(Substring(bytes,Int(5),Int(6)) == Bytes("base16", "00"),
                    Return(Int(6)),
                ),
                If(Substring(bytes,Int(7),Int(8)) == Bytes("base16", "00"),
                    Return(Int(8)),
                ),
                If(Substring(bytes,Int(0),Int(1)) == Bytes("base16", "00"),
                    Return(Int(1)),
                ),
                If(Substring(bytes,Int(2),Int(3)) == Bytes("base16", "00"),
                    Return(Int(3)),
                ),
                If(Substring(bytes,Int(6),Int(7)) == Bytes("base16", "00"),
                    Return(Int(7)),
                ),
                If(Substring(bytes,Int(8),Int(9)) == Bytes("base16", "00"),
                    Return(Int(9)),
                ),
            ]),
        ),
        Err() # we should not get here
    ])
    return logic

@Subroutine(TealType.bytes)
def updateState(bytes, position, value, status):
    ret = ScratchVar(TealType.bytes)
    pos11 = Substring(bytes,Int(0),Int(1))
    pos21 = Substring(bytes,Int(3),Int(4))
    pos31 = Substring(bytes,Int(6),Int(7))
    pos12 = Substring(bytes,Int(1),Int(2))
    pos13 = Substring(bytes,Int(2),Int(3))
    logic = Seq([
        #If(status == Bytes("bad move"), Return(Bytes("bad move"))),# do not rewrite bad move status
        If(status == Bytes("player won"), Return(Bytes("player won"))),# do not rewrite player won
        If(status == Bytes("contract won"), Return(Bytes("contract won"))),# do not rewrite player won
        If(Substring(bytes,position-Int(1),position) != value,
            # last action lead to bad move
            Return(Bytes("bad move"))
        ),
        # check first row
        If(pos11 != Bytes("base16","00"),
            Seq([
                If(pos11 == Bytes("base16","01"),ret.store(Bytes("player won")),ret.store(Bytes("contract won"))),
                #11,12,13
                If(And(Substring(bytes,Int(1),Int(2)) == pos11, Substring(bytes,Int(2),Int(3)) == pos11),
                Return(ret.load()),
                ),
                # 11,21,31
                If(And(Substring(bytes,Int(3),Int(4)) == pos11, Substring(bytes,Int(6),Int(7)) == pos11),
                Return(ret.load()),
                ),
                # 11,22,33
                If(And(Substring(bytes,Int(4),Int(5)) == pos11, Substring(bytes,Int(8),Int(9)) == pos11),
                Return(ret.load()),
                ),
            ]),
        ),
        If(pos21 != Bytes("base16","00"),
            Seq([
                If(pos21 == Bytes("base16","01"),ret.store(Bytes("player won")),ret.store(Bytes("contract won"))),
                # 21,22,23
                If(And(Substring(bytes,Int(4),Int(5)) == pos21, Substring(bytes,Int(5),Int(6)) == pos21),
                Return(ret.load()),
                ),
            ]),
        ),
        If(pos31 != Bytes("base16","00"),
            Seq([
            If(pos31 == Bytes("base16","01"),ret.store(Bytes("player won")),ret.store(Bytes("contract won"))),
            # 31,32,33
            If(And(Substring(bytes,Int(7),Int(8)) == pos31, Substring(bytes,Int(8),Int(9)) == pos31),
            Return(ret.load()),
            ),
            # 31,22,13
            If(And(Substring(bytes,Int(4),Int(5)) == pos31, Substring(bytes,Int(2),Int(3)) == pos31),
            Return(ret.load()),
            ),
            ]),
        ),
        If(pos12 != Bytes("base16","00"),
            Seq([
                If(pos12 == Bytes("base16","01"),ret.store(Bytes("player won")),ret.store(Bytes("contract won"))),
                # 12,22,32
                If(And(Substring(bytes,Int(4),Int(5)) == pos12, Substring(bytes,Int(7),Int(8)) == pos12),
                Return(ret.load()),
                ),
            ]),
        ),
        
        If(pos13 != Bytes("base16","00"),
            Seq([
                If(pos13 == Bytes("base16","01"),ret.store(Bytes("player won")),ret.store(Bytes("contract won"))),
                # 12,22,32
                If(And(Substring(bytes,Int(5),Int(6)) == pos13, Substring(bytes,Int(8),Int(9)) == pos13),
                Return(ret.load()),
                ),
            ]),
        ),
        
        If(Or(
            Substring(bytes,Int(0),Int(1)) == Bytes("base16","00"), 
            Substring(bytes,Int(1),Int(2)) == Bytes("base16","00"), 
            Substring(bytes,Int(2),Int(3)) == Bytes("base16","00"), 
            Substring(bytes,Int(3),Int(4)) == Bytes("base16","00"), 
            Substring(bytes,Int(4),Int(5)) == Bytes("base16","00"), 
            Substring(bytes,Int(5),Int(6)) == Bytes("base16","00"), 
            Substring(bytes,Int(6),Int(7)) == Bytes("base16","00"), 
            Substring(bytes,Int(7),Int(8)) == Bytes("base16","00"), 
            Substring(bytes,Int(8),Int(9)) == Bytes("base16","00")
            )
            ,
            Return(Bytes("playing")),
        ),
        Return(Bytes("draw")),
    ])
    return logic

def approval_program():
    status = ScratchVar(TealType.bytes, 0)
    byteField = ScratchVar(TealType.bytes, 10) # 0 = p11, 1 = p12 ..
    debug = ScratchVar(TealType.bytes, 99)

    Init = Seq(
        [
            debug.store(Bytes("INIT")),
            status.store(Bytes("playing")),
            byteField.store(Bytes("base16", "000000000000000000")),
            #status.store(Bytes("playing")),
            copyFromByteField(byteField.load()),
            debug.store(Bytes("INIT END")),
            
        ]
    )
    #move0 = Bytes())
    move1=Btoi(Substring(Txn.application_args[0],Int(0),Int(1)))
    move2=Btoi(Substring(Txn.application_args[0],Int(1),Int(2)))
    move3=Btoi(Substring(Txn.application_args[0],Int(2),Int(3)))
    move4=Btoi(Substring(Txn.application_args[0],Int(3),Int(4)))
    move5=Btoi(Substring(Txn.application_args[0],Int(4),Int(5)))

    myMove1=ScratchVar(TealType.uint64)
    myMove2=ScratchVar(TealType.uint64)
    myMove3=ScratchVar(TealType.uint64)
    myMove4=ScratchVar(TealType.uint64)


    Game = Seq(
        [
            # \x01\x03\x04\x05\x08\x00\x00\x00
            Init,
            debug.store(Concat(Bytes("USER MOVE1: "),Itob(move1+Int(48)))),
            byteField.store(updateField(byteField.load(),move1,Bytes('base16','01'))),
            status.store(updateState(byteField.load(),move1,Bytes('base16','01'),status.load())),
            debug.store(Concat(Bytes("USER MOVE1 ..: "),status.load())),
            copyFromByteField(byteField.load()),

            myMove1.store(Int(5)), # lets go to the middle if user did not start there
            If(move1 == Int(5), myMove1.store(Int(1))), # else go to top left corner
            debug.store(Concat(Bytes("MY MOVE1: "),Itob(myMove1.load()+Int(48)))),
            
            byteField.store(updateField(byteField.load(),myMove1.load(),Bytes('base16','02'))),
            status.store(updateState(byteField.load(),myMove1.load(),Bytes('base16','02'),status.load())),
            debug.store(Concat(Bytes("MY MOVE1 ..: "),status.load())),
            copyFromByteField(byteField.load()),
            
            debug.store(Concat(Bytes("USER MOVE2: "),Itob(move2+Int(48)))),
            byteField.store(updateField(byteField.load(),move2,Bytes('base16','01'))),
            status.store(updateState(byteField.load(),move2,Bytes('base16','01'),status.load())),
            debug.store(Concat(Bytes("USER MOVE2 ..: "),status.load())),
            copyFromByteField(byteField.load()),

            myMove2.store(getMyMove(byteField.load())),
            debug.store(Concat(Bytes("MY MOVE2: "),Itob(myMove2.load()+Int(48)))),
            byteField.store(updateField(byteField.load(),myMove2.load(),Bytes('base16','02'))),
            status.store(updateState(byteField.load(),myMove2.load(),Bytes('base16','02'),status.load())),
            debug.store(Concat(Bytes("MY MOVE2 ..: "),status.load())),
            copyFromByteField(byteField.load()),
            
            debug.store(Concat(Bytes("USER MOVE3: "),Itob(move3+Int(48)))),
            byteField.store(updateField(byteField.load(),move3,Bytes('base16','01'))),
            status.store(updateState(byteField.load(),move3,Bytes('base16','01'),status.load())),
            debug.store(Concat(Bytes("USER MOVE3 ..: "),status.load())),
            copyFromByteField(byteField.load()),

            myMove3.store(getMyMove(byteField.load())),
            debug.store(Concat(Bytes("MY MOVE3: "),Itob(myMove3.load()+Int(48)))),
            byteField.store(updateField(byteField.load(),myMove3.load(),Bytes('base16','02'))),
            status.store(updateState(byteField.load(),myMove3.load(),Bytes('base16','02'),status.load())),
            debug.store(Concat(Bytes("MY MOVE3 ..: "),status.load())),
            copyFromByteField(byteField.load()),
            
            debug.store(Concat(Bytes("USER MOVE4: "),Itob(move4+Int(48)))),
            byteField.store(updateField(byteField.load(),move4,Bytes('base16','01'))),
            status.store(updateState(byteField.load(),move4,Bytes('base16','01'),status.load())),
            debug.store(Concat(Bytes("USER MOVE4 ..: "),status.load())),
            copyFromByteField(byteField.load()),

            myMove4.store(getMyMove(byteField.load())),
            debug.store(Concat(Bytes("MY MOVE4: "),Itob(myMove4.load()+Int(48)))),
            byteField.store(updateField(byteField.load(),myMove4.load(),Bytes('base16','02'))),
            status.store(updateState(byteField.load(),myMove4.load(),Bytes('base16','02'),status.load())),
            debug.store(Concat(Bytes("MY MOVE4 ..: "),status.load())),
            copyFromByteField(byteField.load()),

            debug.store(Concat(Bytes("USER MOVE5: "),Itob(move5+Int(48)))),
            byteField.store(updateField(byteField.load(),move5,Bytes('base16','01'))),
            status.store(updateState(byteField.load(),move5,Bytes('base16','01'),status.load())),
            debug.store(Concat(Bytes("USER MOVE5 ..: "),status.load())),
            copyFromByteField(byteField.load()),
            #status.store(Bytes("x")),
            #pos:=Int(move0),
            #If(pos == Int(1), p11.store(Int(1)) ),
            Return(Int(1))
        ]
    )
    program = Cond(
        [Txn.application_id() == Int(0), Game],
        #[Len(Txn.application_args[0]) > Int(0), Game],
    )

    return program


def clear_state_program():
    return Approve()


APPROVAL_SRC = os.path.join('.', 'contracts', "approval_program.teal")
CLEARSTATE_SRC = os.path.join('.', 'contracts', "clear_state_program.teal")

if __name__ == "__main__":
    with open(APPROVAL_SRC, "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=8)
        f.write(compiled)

    with open(CLEARSTATE_SRC, "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=8)
        f.write(compiled)