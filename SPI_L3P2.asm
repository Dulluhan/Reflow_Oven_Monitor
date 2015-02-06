$MODDE2 
org 000H 
	ljmp MyProgram
	
FREQ   EQU 33333333
BAUD   EQU 115200
T2LOAD EQU 65536-(FREQ/(32*BAUD))

CE_ADC EQU P0.3
SCLK EQU P0.2
MOSI EQU P0.1
MISO EQU P0.0

DSEG at 30H
x:   ds 4
y:   ds 4
bcd: ds 5

BSEG
mf: dbit 1

$include(math32.asm)

CSEG

; Look-up table for 7-seg displays
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

; An unsigned 32-bit number results in a 10-digit BCD number.
; Since there are only eight 7-segment displays on the DE2
; board, wer are limited to just 8-digits BCD numbers.
Display_BCD:
	
	mov dptr, #T_7seg
	
	mov a, bcd+1
	anl a, #0FH
	movc a, @a+dptr
	mov HEX7, a

	mov a, bcd+0
	swap a
	anl a, #0FH
	movc a, @a+dptr
	mov HEX6, a
	
	mov a, bcd+0
	anl a, #0FH
	movc a, @a+dptr
	mov HEX5, a
	
	ret
	
MyProgram:
	mov sp, #07FH ; Initialize the stack pointer
	; For the health of your eyes, turn off all LEDs!
	clr a
	mov LEDG,  #0
	mov LEDRA, #0
	mov LEDRB, #0
	mov LEDRC, #0
	orl P0MOD, #00001000b
	lcall InitSerialPort
	lcall INI_SPI
	
Forever:
	clr CE_ADC
	mov R0, #00000001B ; Start bit:1
	lcall DO_SPI_G
	mov R0, #10000000B ; Single ended, read channel 0
	lcall DO_SPI_G
	mov a, R1 ; R1 contains bits 8 and 9
	anl a, #03H ; Make sure other bits are zero
	mov LEDRB, a ; Display the bits
	mov x+1,a	
	mov R0, #55H ; It doesn't matter what we transmit...  55H is easier to see on the Oscilloscope 
	lcall DO_SPI_G
	mov LEDRA, R1 ; R1 contains bits 0 to 7
	setb CE_ADC
	
	mov x+0,r1
	mov x+2, #0
	mov x+3, #0
	setb CE_ADC

	load_y(5000)
	lcall mul32
	
	load_y(1023)
	lcall div32
	
	load_y(2870)
	lcall sub32
	
	lcall hex2bcd 
	lcall Display_BCD
	lcall temp
	lcall Delay
	
	sjmp Forever

temp:
;serial output
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
	
	;mov a, #'Degrees'
	;lcall putchar
	
	mov a, #'\r'
	lcall putchar
	
	mov a, #'\n'
	lcall putchar
	
	ret
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

end 