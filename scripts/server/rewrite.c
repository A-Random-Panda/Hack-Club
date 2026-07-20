//So I just realized I had no idea what I was smoking with the parser...
//So I am just gonna remake it and pretend the original never happened
//Right now the errors aren't the best
//But I'll only make them more deccriptive if it ever becomes an issue
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_CAMERAS 11
#define MAX_QUOTATIONS 50 //Guessimate; For cameras, 11*2 is 22, shouldn't be more than this
//1460 is kinda the absolute max packet size
#define MAX_PACKET_SIZE 1024 //Not max packet size, but if much it's bigger than this, we should probably switch to a different format

int parseVec3(char *str, double *result);
int parseDouble(char *str, double *result);
int parseListVec3(char *str, double (*result)[3], int amount);

static PyObject *
parse_state(PyObject *self, PyObject *args) {
    //The idea behind this is to create a copy of the input in a buffer, and edit the buffer
    //Such that each quotation in the list gets turned into a null terminated string
    //With the first character being stored into a string

    //('1', '[Vec3(0.5, 1.05, 0.5)]', '[Vec3(0, 10.277778, 0)]', '5.0', 'False', 'Vec3(0.5, 1.05, 0.5)', 'Vec3(0, 10.277778, 0)')
    //('amount of player cams', 'player cams position: list[vec3]', 'player cams rotation: list[vec3]', 'reload time: float', 'player dead: bool', 'player world position: vec3', 'player rotation: vec3'), 'player dead: bool', 'player world position: vec3', 'player rotation: vec3')
    
    //Variable declarations
    PyObject *stateDict = PyDict_New();
    //Used in the output
    int cameraCount;
    int playerDead;
    //Technically, these can all be one buffer, but I think it's gonna be fine either way
    double dblBuf;
    double vec3Buf[3];
    double listVec3Buf[3][MAX_CAMERAS]; 
    
    //Used in the implementation
    int stateLen;
    int quoteIndex;
    int secondQuotation;
    char *stateBuffer;
    char *quotedStrings[MAX_QUOTATIONS]; //Things in the quotes

    //Get the string from the args
    const char * stateString;
    if (!PyArg_ParseTuple(args, "s", &stateString)) {
        return NULL;
    }

    //Check that the string fits our max packet size
    stateLen = strlen(stateString);
    if (stateLen * sizeof(char) > MAX_PACKET_SIZE) {
        goto dataSizeError;
    }
    
    //Puts the string into a seperate buffer
    stateBuffer = (char*)malloc(stateLen * sizeof(char) + 1);
    if (stateBuffer == NULL) {
        goto memoryError;
    }
    strcpy(stateBuffer, stateString); //Unsafe function but I explicitily created the buffer to be the size
    //And I cannot be bothered to learn the safe portable version right now

    //Seperates each quotation
    quoteIndex = 0;
    secondQuotation = false;
    //Iterates through the string until a '
    for (int i = 0; i < stateLen; i++) {
        //If there's more than the maximum, error
        if (quoteIndex >= 50) {
            goto inputError;
        }
        //If it's the first quotation mark, put the index plus one into the quotes list, add one to the quoteIndex
        //Worst case scenario it's the null terminator, and we check if the secondQuotation is true
        //After the loop to catch the error anyways
        if (stateBuffer[i] == '\'' && !secondQuotation) {
            quotedStrings[quoteIndex+1] = stateBuffer[i];
            quoteIndex++;
            secondQuotation = true;
        }
        //If it's the second quotation mark, set it to a null terminator
        else if (stateBuffer[i] == '\'' && secondQuotation) {
            stateBuffer[i] = '\0';
            secondQuotation = false;
        }
    }

    //Checks if it expects a second quotation
    if (secondQuotation) {
        goto inputError;
    }

    //Now we should have a null terminated list of all the quotes
    //With quoteIndex being 1 over the maximum defined

    //Error management
    inputError:
        PyErr_SetString(PyExc_ValueError, "The value inputted is incorrect.");
        return NULL;
    dataSizeError:
        PyErr_SetString(PyExc_BufferError, "Too much data got sent.");
        return NULL;
    memoryError:
        PyErr_SetString(PyExc_MemoryError, "Program ran out of memory.");
        return NULL;
}

int parseListVec3(char *str, double (*result)[3], int amount) {
    //I uh, can't be bothered to learn how to do this properly
    //Takes a pointer a list of 3 as input
    int matched;
    if (amount == 1) {
        matched = sscanf(str, "[Vec3(%lf, %lf, %lf)]", &result[0][0], &result[0][1], &result[0][2]);
        if (matched != 3) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    else if (amount == 2) {
        matched = sscanf(str, "[Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)]", &result[0][0], &result[0][1], &result[0][2], &result[1][0], &result[1][1], &result[1][2]);
        if (matched != 6) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    else if (amount == 3) {
        matched = sscanf(str, "[Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)]", &result[0][0], &result[0][1], &result[0][2], &result[1][0], &result[1][1], &result[1][2], &result[2][0], &result[2][1], &result[2][2]);
        if (matched != 9) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    else if (amount == 4) {
        matched = sscanf(str, "[Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)]", &result[0][0], &result[0][1], &result[0][2], &result[1][0], &result[1][1], &result[1][2], &result[2][0], &result[2][1], &result[2][2], &result[3][0], &result[3][1], &result[3][2]);
        if (matched != 12) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    else if (amount == 5) {
        matched = sscanf(str, "[Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)]", &result[0][0], &result[0][1], &result[0][2], &result[1][0], &result[1][1], &result[1][2], &result[2][0], &result[2][1], &result[2][2], &result[3][0], &result[3][1], &result[3][2], &result[4][0], &result[4][1], &result[4][2]);
        if (matched != 15) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    else if (amount == 6) {
        matched = sscanf(str, "[Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)]", &result[0][0], &result[0][1], &result[0][2], &result[1][0], &result[1][1], &result[1][2], &result[2][0], &result[2][1], &result[2][2], &result[3][0], &result[3][1], &result[3][2], &result[4][0], &result[4][1], &result[4][2], &result[5][0], &result[5][1], &result[5][2]);
        if (matched != 18) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    else if (amount == 7) {
        matched = sscanf(str, "[Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)]", &result[0][0], &result[0][1], &result[0][2], &result[1][0], &result[1][1], &result[1][2], &result[2][0], &result[2][1], &result[2][2], &result[3][0], &result[3][1], &result[3][2], &result[4][0], &result[4][1], &result[4][2], &result[5][0], &result[5][1], &result[5][2], &result[6][0], &result[6][1], &result[6][2]);
        if (matched != 21) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    else if (amount == 8) {
        matched = sscanf(str, "[Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)]", &result[0][0], &result[0][1], &result[0][2], &result[1][0], &result[1][1], &result[1][2], &result[2][0], &result[2][1], &result[2][2], &result[3][0], &result[3][1], &result[3][2], &result[4][0], &result[4][1], &result[4][2], &result[5][0], &result[5][1], &result[5][2], &result[6][0], &result[6][1], &result[6][2], &result[7][0], &result[7][1], &result[7][2]);
        if (matched != 24) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    else if (amount == 9) {
        matched = sscanf(str, "[Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)]", &result[0][0], &result[0][1], &result[0][2], &result[1][0], &result[1][1], &result[1][2], &result[2][0], &result[2][1], &result[2][2], &result[3][0], &result[3][1], &result[3][2], &result[4][0], &result[4][1], &result[4][2], &result[5][0], &result[5][1], &result[5][2], &result[6][0], &result[6][1], &result[6][2], &result[7][0], &result[7][1], &result[7][2], &result[8][0], &result[8][1], &result[8][2]);
        if (matched != 27) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    else if (amount == 10) {
        matched = sscanf(str, "[Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)]", &result[0][0], &result[0][1], &result[0][2], &result[1][0], &result[1][1], &result[1][2], &result[2][0], &result[2][1], &result[2][2], &result[3][0], &result[3][1], &result[3][2], &result[4][0], &result[4][1], &result[4][2], &result[5][0], &result[5][1], &result[5][2], &result[6][0], &result[6][1], &result[6][2], &result[7][0], &result[7][1], &result[7][2], &result[8][0], &result[8][1], &result[8][2], &result[9][0], &result[9][1], &result[9][2]);
        if (matched != 30) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    else if (amount == 11) {
        matched = sscanf(str, "[Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)]", &result[0][0], &result[0][1], &result[0][2], &result[1][0], &result[1][1], &result[1][2], &result[2][0], &result[2][1], &result[2][2], &result[3][0], &result[3][1], &result[3][2], &result[4][0], &result[4][1], &result[4][2], &result[5][0], &result[5][1], &result[5][2], &result[6][0], &result[6][1], &result[6][2], &result[7][0], &result[7][1], &result[7][2], &result[8][0], &result[8][1], &result[8][2], &result[9][0], &result[9][1], &result[9][2], &result[10][0], &result[10][1], &result[10][2]);
        if (matched != 33) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    else {
        printf("Amount was not in range");
        return -1;
    }
    printf("returned 0\n");
    return 0;
}

int parseVec3(char *str, double *result) {
    //Takes a list of 3 as input
    //Not exactly sure how sscanf works, but I'm just praying that it works at this point
	int matched = sscanf(str, "Vec3(%lf, %lf, %lf)", result, result+1, result+2);
    if (matched != 3) {
		printf("%d Matched\n", matched);
        return -1;
    }
    return 0;
}

int parseDouble(char *str, double *result) {
    //Takes a pointer to a double as input
	int matched = sscanf(str, "%lf", result);
    if (matched != 1) {
		printf("%d Matched\n", matched);
        return -1;
    }
    return 0;
}
