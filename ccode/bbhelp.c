int getbin(char *result, uint64_t c) {
    
    int rmdr; // remainder
    int b = c;
    
    while( b >= 1 ) {
        
        rmdr = b % 2;
        
        if(rmdr == 0){
            *result = '0';
            printf("%c", *result);
        } else {
            *result = '1';
            printf("%c", *result);
        }
        result++;
        b = ( b - rmdr) / 2;
    }
    printf("\n");
} 

void strrev(char *str) { // Returns a pointer to the temp array
    int strlen = 64; // We only work with 64-bit ints.
    char temp[strlen]; // temp storage to hold correct order
    
    int i = 0;
    while (i < strlen) { 
        temp[strlen - i - 1] = *str;
        i++;
        str++;
    }
    
    i = 0; // Reset idx to start copying array from the back
    str--; // Get back to last object in the array
    
    while(i < strlen) {
        *str = temp[strlen - i - 1];
        i++;
        str--;
    }
}
