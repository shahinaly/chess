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


/* Bitboard Structure */
struct board {
    unsigned long long pawns; 
    unsigned long long knights;
    unsigned long long bishops;
    
    unsigned long long rooks;
    unsigned long long queens;
    unsigned long long kings;
    
    unsigned long long white;
    unsigned long long black;
};

/* Declaring all module functions */
void showbits(struct board);
void impboard(struct board *);
void move(struct board);

/* Board Declaration */
int main() {
    struct board b;
    impboard(&b);
    
    showbits(b);
}

// Edited from Wikipedia: Bitwise Operators in C
void showbits(struct board b) { 
    
    long long unsigned x = (b.white | b.black);

    for (int i = 8; i > 0; i--) {
        for (int j = 8; j > 0; j--) {
            
            putchar( (x & 1LLU <<  (i*8 - j)) ? '1' : '_');
            if(j == 1) printf("\n");
        }
    }
    printf("\n");
}

void impboard(struct board *pb) {

    (*pb).pawns = 0x00FF00000000FF00;
    (*pb).knights = (0b01000010ULL << 56) + 0b01000010;
    (*pb).bishops = (0b00100100ULL << 56) + 0b00100100;
   
    (*pb).rooks =  (0b10000001ULL << 56) + 0b10000001;
    (*pb).queens =  (0b00010000ULL << 56) + 0b00010000;
    (*pb).kings =  (0b00001000ULL << 56) + 0b00001000;
    
    (*pb).white = 0x000000000000FFFFULL;
    (*pb).black = 0xFFFF000000000000ULL;
}

