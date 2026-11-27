// Box.asm -- filled box. PLACEHOLDER VALUES: replace with your K-based numbers.
// Example: start word column 10, row 100 -> 16384 + 100*32 + 10 = 19594
// Width = 4 words (64 px), height = 50 rows.
@19594      // START = 16384 + row*32 + col
D=A
@addr
M=D
@50         // H (rows)
D=A
@rows
M=D
(LOOP)
@rows
D=M
@END
D;JEQ
@4          // W (words per row)
D=A
@cols
M=D
@addr
D=M
@p
M=D
(ROW)
@cols
D=M
@NEXTROW
D;JEQ
@p
A=M
M=-1
@p
M=M+1
@cols
M=M-1
@ROW
0;JMP
(NEXTROW)
@32
D=A
@addr
M=D+M
@rows
M=M-1
@LOOP
0;JMP
(END)
@END
0;JMP
