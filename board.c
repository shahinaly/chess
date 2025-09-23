#include<stdio.h>
#include<string.h>
#include<stdint.h>
#include"bbhelp.c"

/* 
 * This module is for the Board Representation.
 *
 * What we need for a proper board:
 * 
 * 1. The board itself - data structure?
 * 2. Piece Representation
 * 3. Board Logic
 * 4. make() and unmake() move.
 *
 * */

void imp_board(void);
void showbits(long long unsigned );

int main() {
   imp_board(); 
}

struct board {
    
    /* Board will consist of the following bitboards:
     * 1. Pawns
     * 2. Knights
     * 3. Bishops
     * 4. Rooks
     * 5. Queens
     * 6. Kings
     * 7. White Pieces
     * 8. Black Pieces
     * */
    
    unsigned long long pawns; 
    unsigned long long knights;
    unsigned long long bishops;
    
    unsigned long long rooks;
    unsigned long long queens;
    unsigned long long kings;
    
    unsigned long long white;
    unsigned long long black;

};

void imp_board() {
    
    struct board b;
   
    b.pawns = 0x00FF00000000FF00;
    b.knights = (0b01000010ULL << 56) + 0b01000010;
    b.bishops = (0b00100100ULL << 56) + 0b00100100;
    
    b.rooks =  (0b10000001ULL << 56) + 0b10000001;
    b.queens =  (0b00010000ULL << 56) + 0b00010000;
    b.kings =  (0b00001000ULL << 56) + 0b00001000;
    
    b.white = 0x000000000000FFFFULL;
    b.black = 0xFFFF000000000000ULL;
   
    showbits(b.white | b.black);

}

// Edited from Wikipedia: Bitwise Operators in C
void showbits( long long unsigned x) { 
    
    for (int i = 8; i > 0; i--) {
        for (int j = 8; j > 0; j--) {
            
            putchar( (x & 1LLU <<  (i*8 - j)) ? '1' : '_');
            if(j == 1) printf("\n");
        }
    }
    printf("\n");
}

