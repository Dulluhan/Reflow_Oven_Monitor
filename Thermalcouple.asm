$MODDE2
org 0000H
   ljmp MyProgram



FREQ   EQU 33333333
BAUD   EQU 115200
T2LOAD EQU 65536-(FREQ/(32*BAUD))
;---------------------------------
CE_ADC EQU P0.3
SCLK EQU P0.2
MOSI EQU P0.1
MISO EQU P0.0

DSEG at 30H
x:   ds 4
y:   ds 4
bcd: ds 5
chan0: ds 4
chan1: ds 4
;---------------------------------

BSEG

	mf: dbit 1
	$include(math32.asm)

CSEG

T_7seg:
    DB 0C0H, 0F9H, 0A4H, 0B0H, 099H
    DB 092H, 082H, 0F8H, 080H, 090H
    DB 088H, 083H

; Configure the serial port and baud rate using timer 2
InitSerialPort:
	clr TR2 ; Disable timer 2
	mov T2CON, #30H ; RCLK=1, TCLK=1
	mov RCAP2H, #high(T2LOAD)
	mov RCAP2L, #low(T2LOAD)
	setb TR2 ; Enable timer 2
	mov SCON, #52H
	ret

; Send a character through the serial port
putchar:
    JNB TI, putchar
    CLR TI
    MOV SBUF, a
    RET

; Send a constant-zero-terminated string through the serial port
SendString:
    CLR A
    MOVC A, @A+DPTR
    JZ SSDone
    LCALL putchar
    INC DPTR
    SJMP SendString
SSDone:
    ret

Hello_World:
    DB  'Hello, World!', '\r', '\n', 0

Delay:
	mov R2, #90
L3: mov R1, #250
L2: mov R0, #250
L1: djnz R0, L1
	djnz R1, L2
	djnz R2, L3
	ret

Display_BCD_F:

	mov dptr, #T_7seg

	;mov a, bcd+3
	;anl a, #0FH
	;movc a, @a+dptr
	;mov HEX7, a

	;mov a, bcd+2
	;swap a
	;anl a, #0FH
	;movc a, @a+dptr
	;mov HEX7, a

	mov a, bcd+2
	anl a, #0FH
	movc a, @a+dptr
	mov HEX7, a

	mov a, bcd+1
	swap a
	anl a, #0FH
	movc a, @a+dptr
	mov HEX6, a

	mov a, bcd+1
	anl a, #0FH
	movc a, @a+dptr
	mov HEX5, a

	mov a, bcd+0
	swap a
	anl a, #0FH
	movc a, @a+dptr
	mov HEX4, a

	mov a, bcd+0
	anl a, #0FH
	movc a, @a+dptr
	mov HEX3, a

	mov HEX2, #11111111b

	mov HEX1, #10011100b

	mov HEX0, #10001110b

	ret
;--------------------------------------------------

Display_BCD:

	mov dptr, #T_7seg

	;mov a, bcd+3
	;anl a, #0FH
	;movc a, @a+dptr
	;mov HEX7, a

	;mov a, bcd+2
	;swap a
	;anl a, #0FH
	;movc a, @a+dptr
	;mov HEX7, a

	mov a, bcd+2
	anl a, #0FH
	movc a, @a+dptr
	mov HEX7, a

	mov a, bcd+1
	swap a
	anl a, #0FH
	movc a, @a+dptr
	mov HEX6, a

	mov a, bcd+1
	anl a, #0FH
	movc a, @a+dptr
	mov HEX5, a

	mov a, bcd+0
	swap a
	anl a, #0FH
	movc a, @a+dptr
	mov HEX4, a

	mov a, bcd+0
	anl a, #0FH
	movc a, @a+dptr
	mov HEX3, a

	mov HEX2, #11111111b

	mov HEX1, #10011100b

	mov HEX0, #11000110b

	ret
;--------------------------------------------------

MyProgram:
    MOV SP, #7FH
    mov LEDRA, #0
    mov LEDRB, #0
    mov LEDRC, #0
    mov LEDG, #0
    mov chan0, #0
    mov chan1, #0
orl P0MOD, #00001000b ; make CE_ADC (P0.3) output

    LCALL InitSerialPort
    lcall INI_SPI
Forever:

CheckCH0: ; this finds the temp of the LM335
	clr CE_ADC
	mov R0, #00000001B ; Start bit:1
	lcall DO_SPI_G

	mov R0, #10000000B ; Single-ended, channel 0
	lcall DO_SPI_G
	mov a, R1 ; bits 8 and 9
	anl a, #03H ; Make sure other bits are zero
	mov x+1, a
	mov R0, #55H ; It doesn't matter what we transmit...
	lcall DO_SPI_G

	mov a, R1 ; bits 7 - 0
	setb CE_ADC

	mov x+0, a
	mov x+2, #0
	mov x+3, #0

	load_y(5000)
	lcall mul32

	load_y(1023)
	lcall div32

	load_y(2730)
	lcall sub32

	mov a, x+1
	;mov LEDRB, a
	mov a, x+0
	;mov LEDRA, a

	mov a, x+0
	mov chan0+0, a  ; transfer to temporary storage
	mov a, x+1
	mov chan0+1, a
	mov a, x+2
	mov chan0+2, a
	mov a, x+3
	mov chan0+3, a  ; this block just stores it later in order to sum together

CheckCH1:    ; this finds the temp difference between the thermocouple and the LM335 sensor
	clr CE_ADC
	mov R0, #00000001B ; Start bit:1
	lcall DO_SPI_G

  mov R0, #10010000B ; Single ended, read channel 1
	;mov R0, #00010000B
	lcall DO_SPI_G

	mov a, R1 ; bits 8 and 9
	anl a, #03H ; Make sure other bits are zero
	mov x+1,a
	mov R0, #55H ; It doesn't matter what we transmit...
	lcall DO_SPI_G

  mov a, R1 ; bits 7 - 0
	setb CE_ADC

	mov x+0, a
	mov x+2, #0
	mov x+3, #0

	mov a, x+1
	;mov LEDRB, a
	mov a, x+0
	;mov LEDRA, a

	load_y(8200) ; this needs to be changed tho... 99% sure it's the wrong value
	lcall mul32

	load_y(1000) ; we do this because the first one would be load_y(0008.2)...
	lcall div32  ; which we can't do. Just trying this to compensate.


	;; put back here

	mov a, x+0
	mov chan1+0, a  ; transfer to temporary storage
	mov a, x+1
	mov chan1+1, a
	mov a, x+2
	mov chan1+2, a
	mov a, x+3
	mov chan1+3, a  ; this block just stores it later in order to sum together

	mov a, chan0+0
	mov y, a
	mov a, chan0+1
	mov y, a
	mov a, chan0+2
	mov y, a
	mov a, chan0+3
	mov y, a

	lcall add32
	load_y(1700) ;find calibration constant here...
	lcall sub32
	mov a, x+1
	mov LEDRB, a ;display bits 8 and 9
	mov a, x+0
 	mov LEDRA, a ;display bits 7 - 0


    lcall hex2bcd ; hex to decimal conversion and display stuff below
    mov a, swa
    cjne a, #00000001B, displayC
    mov a, bcd

    mov bcd, a
    lcall Display_BCD_F
    lcall Delay
    displayC:
    mov a, swa
    cjne a, #00000000B, display
	lcall Display_BCD
	lcall Delay
	display:
	lcall temperature
	lcall Delay
ljmp Forever

temperature:

    mov a, bcd+1
	swap a
	anl a, #0FH
	orl a, #30H
	lcall putchar
	mov a, bcd+1
	anl a, #0FH
	orl a, #30h
	lcall putchar

    mov a, bcd+0
	swap a
	anl a, #0FH
	orl a, #30H
	lcall putchar

	mov a, #'.'
	lcall putchar

	mov a, bcd+0
	anl a, #0FH
	orl a, #30h
	lcall putchar

	mov a, #'\r'
	lcall putchar

	mov a, #'\n'
	lcall putchar


;-------------------------------------------------------
;--------------------------------------------------
INI_SPI:
orl P0MOD, #00000110b ; Set SCLK, MOSI as outputs
anl P0MOD, #11111110b ; Set MISO as input
clr SCLK ; Mode 0,0 default
ret
DO_SPI_G:
mov R1, #0 ; Received byte stored in R1
mov R2, #8 ; Loop counter (8-bits)
DO_SPI_G_LOOP:
mov a, R0 ; Byte to write is in R0
rlc a ; Carry flag has bit to write
mov R0, a
mov MOSI, c
setb SCLK ; Transmit
mov c, MISO ; Read received bit
mov a, R1 ; Save received bit in R1
rlc a
mov R1, a
clr SCLK
djnz R2, DO_SPI_G_LOOP
ret



END
