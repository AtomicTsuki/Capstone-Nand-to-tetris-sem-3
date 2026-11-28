// Box.asm - draws a box (W = 4 words = 64 pixels wide, H = K = 43 rows)
// Start address = 16384 + row*32 + col = 16384 + 100*32 + 10 = 19594
@19594
D=A
@addr
M=D // addr = start address
@43
D=A
@rows
M=D // rows = H = K = 43
(LOOP)
@rows
D=M
@END
D;JEQ // if rows == 0 goto END
@4
D=A
@cols
M=D // cols = W = 4
@addr
D=M
@p
M=D // p = addr
(ROW)
@cols
D=M
@NEXT
D;JEQ // if cols == 0 goto NEXT
@p
A=M
M=-1 // 16 black pixels
@p
M=M+1 // next word
@cols
M=M-1
@ROW
0;JMP
(NEXT)
@32
D=A
@addr
M=D+M // addr = addr + 32 (next pixel row)
@rows
M=M-1
@LOOP
0;JMP
(END)
@END
0;JMP
