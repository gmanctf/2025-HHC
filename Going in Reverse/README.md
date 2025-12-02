The .bas file is written in FreeBASIC using the QBASIC syntax. If you would like to test the program, you can install FreeBasic, compile the program, and run it.

# Install FreeBasic

The steps below were followed in Ubuntu 24.04:

```
wget https://sourceforge.net/projects/fbc/files/FreeBASIC-1.10.1/Binaries-Linux/FreeBASIC-1.10.1-ubuntu-22.04-x86_64.tar.xz
tar -xf FreeBASIC-1.10.1-ubuntu-22.04-x86_64.tar.xz
sudo ./FreeBASIC-1.10.1-ubuntu-22.04-x86_64/install.sh -i
```
# Compile and execute the program

You can compile the program with the following command (note that -lang qb is required to select the QBASIC syntax):

`fbc -lang qb login.bas`

If the command runs successfully, now we can execute the program:

`./login`

# Code explanation line by line

`10 REM *** COMMODORE 64 SECURITY SYSTEM *****`
REM = Remark (comment). Remarks are used as comments in the code and are not printed, the line will be ignore when the program is executed.

`20 ENC_PASS$ = "D13URKBT"`
Stores an encrypted password string in the variable ENC_PASS$.

`30 ENC_FLAG$ = "DSA|auhts*wkfi=dhjwubtthut+dhhkfis+hnkz" ' old "DSA|qnisf`bX_huXariz"`
Stores an encrypted flag string in ENC_FLAG$. ' is used to denote a comment, in this case it says the old string was "DSA|qnisfbX_huXariz".

`40 INPUT "ENTER PASSWORD: "; PASS$`
Prompts the user to enter a password and stores it in PASS$.

`50 IF LEN(PASS$) <> LEN(ENC_PASS$) THEN GOTO 90`
Compares lengths: if the input length ≠ encrypted password length (8), jump to line 90 (ACCESS DENIED).

`60 FOR I = 1 TO LEN(PASS$)`
Start a loop I from 1 to the password length.

`70 IF CHR$(ASC(MID$(PASS$,I,1)) XOR 7) <> MID$(ENC_PASS$,I,1) THEN GOTO 90`

MID$(PASS$,I,1) means that MID$ = the I-th character of the input (stored in PASS$). Then ASC will convert it to ASCII.
Then the XOR operation with the key 7 is done and finally CHR$(...) converts the result back to a character.
If that character ≠ the I-th character of ENC_PASS$, go to line 90 (deny access).

`80 NEXT I`
End of loop; if loop completes, password is correct.

`85 FLAG$ = "" : FOR I = 1 TO LEN(ENC_FLAG$) : FLAG$ = FLAG$ + CHR$(ASC(MID$(ENC_FLAG$,I,1)) XOR 7) : NEXT I : PRINT FLAG$`

FLAG$ = "" initializes the flag string. Then a loop is done over each character of ENC_FLAG$. For each character: get ASCII, XOR with 7, convert back to char, append to FLAG$.
Finally, the decrypted flag is printed.

`90 PRINT "ACCESS DENIED"`
Printed if either length check fails or any character mismatch occurs.

`100 END`
Ends the program.
