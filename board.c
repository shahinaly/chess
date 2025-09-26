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
int move(struct board *, long long unsigned *, int from, int to);
void parse_move(char []);

/* Board Declaration */
int main() {
    struct board b;
    impboard(&b);
    move(&b, &(b.white), 12, 20); 
    showbits(b);
}

// Edited from Wikipedia: Bitwise Operators in C
void showbits(struct board b) { 
    long long unsigned x = (b.white);

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

int move(struct board *pb, unsigned long long *mvrpieces, int from, int to) {
   
    /* move() must check:
     *  - in check?
     *  - legal?
     *      - can it be reached by piece?
     *      - square occupied by same colour?
     *      - does it put king in check?
     **/
    
    long long unsigned pick = 1ULL << from;
    long long unsigned put = 1ULL << to;   
    
    // in check?
    //if incheck() return 1;
        
    
    // legality: Can it be reach by piece?
    // TODO
    
    // legality: Is there a piece there to be moved?
    //if((*mvrpieces & pick) != 0ULL) return 1; 
    
    // legality: Square occupied by same colour?
    //if((*mvrpieces & put) != 0ULL) return 1; 
    
    (*pb).white = ((*pb).white ^ pick ^ put);
    
}

// Accepts String in algebraic notation and returns [int from, int to] 
void parse_move(char move[]) {
    // move[] can look like: e4, Na5, Rdf8, Qh4e1, 0-0, 0-0-0, e8=Q
    
    return ;

}
