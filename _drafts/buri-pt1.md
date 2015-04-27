---
layout: post
title: Buri 1
tags: buri
---

My little homebrew 6502 project has reached the point where I can do some real
experimentation with it. Before that point, however, I need a stable way of
interacting with it. Getting some real video output and keyboard input is almost
immediately next on my "to do" list but for the time being, I'm using a good
old-fashioned [RS-232](http://en.wikipedia.org/wiki/RS-232) serial port.

## Hardware: the 6551

The 6500-series chips come with their own "serial port on a chip" solution: the
[6551](http://en.wikipedia.org/wiki/MOS_Technology_6551). Hooking it up to Buri
is fairly simple. The first thing to do is to connect the data bus and processor
control lines. Secondly, we need to find a way to map the chip into the address
space.

Buri has the concept of the "IO area". Address decode circuitry on the main
board will pull one of eight IO lines low when the CPU tries to access addresses
in the range DF80h to DFFFh inclusive. The IO0 line goes low when addresses
DF80h to DF8Fh are accessed, IO1 goes low for DF90h to DF9Fh, etc. Wiring up the
<span class="overline">CS1</span> to <span class="overline">IO7</span> and
wiring CS0 high will select the 6551 when addresses DFF0h to DFFFh inclusive are
accessed. We can wire A0 and A1 to RS0 an RS1 on the 6551 to map the four 6551
registers four times into those sixteen bytes.

The four 6551 registers are data, status command and control. In the OS source
we can expose their location as constants:

```x86asm
; ACIA1 is at *end* of final IO page
ACIA1_DATA      = $DFFC
ACIA1_STATUS    = $DFFD
ACIA1_CMD       = $DFFE
ACIA1_CTRL      = $DFFF
```

Setting up the chip for the right baud rate, parity, etcetera is simply a matter
of writing the correct value into the command and control registers. In the Buri
OS this is performed in the [initio
function](https://github.com/rjw57/buri/blob/801742751c869ab6af42fe87f023e70fc04e1a27/os/src/serial/initio.s).

Reading and writing data is pretty simple; writing a byte to the data register
sends it and reading a byte returns the latest character received. The trixky
part is knowing when to write the next byte when sending or when there is data
to read when receiving. The answer is to test two bits in the status register.
We define two masks for the corresponding bits as constants:

```x86asm
; ACIA-related constants
ACIA_ST_TDRE = %00010000    ; status: transmit data register empty
ACIA_ST_RDRF = %00001000    ; status: read data register full
```

Getting the next character is now simply a case of waiting for the next
character to arrive:

```x86asm

; srl_getc - wait for the next character from the serial port
;
; on exit:
; 	A - the ASCII code of the character read
.proc srl_getc
	lda	#ACIA_ST_RDRF		; load RDRF mask into A

wait_rx_full:
	bit	ACIA1_STATUS		; is the rx register full?
	beq	wait_rx_full		; ... no, loop

	lda	ACIA1_DATA		; read character from ACIA
	rts				; return
.endproc
```

Outputting a byte is nearly as easy:

```x86asm
; srl_putc - send a character along the serial connection
;
; on entry:
; 	A - the ASCII code of the character to send
; on exit:
; 	A - preserved
.proc srl_putc
	pha				; save A on stack
	
	lda	#ACIA_ST_TDRE		; load TDRE mask into A
wait_tx_free:
	bit	ACIA1_STATUS		; is the tx register empty?
	beq	wait_tx_free		; ... no, loop

	pla				; retrieve input from stack
	sta	ACIA1_DATA		; write character to tx data reg
	rts				; return
.endproc
```
