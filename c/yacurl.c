#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#define BUFFER_SIZE 800000

int main(int argc, char *argv[]){
    if(argc != 3){
        printf("Usage is ./yacurl <url> <port>\n");
        exit(0);
    }
    char *url = argv[1];
    int *port = argv[2];

    return 1;
}

int create_socket(url, port){
    struct sockaddr_in client;
    struct hostent *server;
    server = gethostbyname(url);
    if(server==NULL){
        printf("Bad host");
        return 1;
    }
    
}




