int main() {
    // 1. Define the address as a pointer. 
    // Use 'volatile' to prevent the compiler from optimizing the write away.
    char *ptr = (char *)0xc0000000; 

    *ptr = 41; 

    return 0;
}