#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <limits.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#define MAX_CAMERAS 11
#define MINIMUM_LENGTH 20 //Don't have an exact minumum, but I don't think it'll be necessary, honestly
#define INTEGER_START_INDEX 2
#define SIZE_CHAR sizeof(char)
//This is written in c for optimization reasons
//Cause the string needs to be parsed once per player every server tick

//This is terrible code quality c code and I know it
//But it works (hopefully) and is optimized, okay?

static PyObject *
parse_state(PyObject *self, PyObject *args) {
    //('1', '[Vec3(0.5, 1.05, 0.5)]', '[Vec3(0, 10.277778, 0)]', 'DNE', 'DNE', '5.0', 'False', 'Vec3(0.5, 1.05, 0.5)', 'Vec3(0, 10.277778, 0)')
    //('amount of player cams', 'player cams position: list[vec3]', 'player cams rotation: list[vec3]', 'bullet trail: entity', 'bullet trail position: vec3', 'reload time: float', 'player dead: bool', 'player world position: vec3', 'player rotation: vec3')
    const char * stateString;
    int cameraCount;
    int playerDead;
    double playerPos[3];
    double playerRotation[3];
    double camLocations[MAX_CAMERAS][3];
    double camRotations[MAX_CAMERAS][3];
    int length_left = strlen(stateString);
    //The string is a list converted to a string, so the third character is always an integer
    int count = INTEGER_START_INDEX;

    if (!PyArg_ParseTuple(args, "s", &stateString)) {
        return NULL;
    }
    //Check that the string is at least 3 characters long (I assume that it is later on)
    if (length_left > MINIMUM_LENGTH) {
        goto strLengthError;
    }
    //Iterates through from index 2 and checks until there's no digit
    while (isdigit(stateString[count])) {
        count++;
    }
    //The maximum cameras should be 2 characters long
    //I am doing this check because I don't want to check for overflow
    if (count-INTEGER_START_INDEX == 2) {
        cameraCount = (stateString[3] - '0') * 10 + stateString[2]-'0';
    } else if (count-INTEGER_START_INDEX == 1) {
        cameraCount = stateString[2] - '0';
    } else if (count-INTEGER_START_INDEX == 0) {
        //There is no integer
        goto noCamAmount;
    } else {
        //The integer is over 99
        goto camAmountError;
    }
    //Check if the number is over 11
    if (cameraCount > 11) {
        goto camAmountError;
    }
    //Count is now at the index of the comma
    //So at this point I realize that it's kinda just easier to parse through the string with straight
    //pointer arithmetic rather than with a counter...
    stateString += count * sizeof(char);
    length_left -= count;

    //gotos are unironically good error handling
    //These are only the errors that could be raised directly from from the parse_state function
    strLengthError:
        PyErr_Format(PyExc_ValueError, "String is not long enough to contain all the parsed information at %s", stateString);
        return NULL;
    noCamAmount:
        PyErr_SetString(PyExc_ValueError, "A maximum camera amount must be provided");
        return NULL;
    camAmountError:
        PyErr_Format(PyExc_ValueError, "Maximum cameras must be at most %d!", MAX_CAMERAS);
        return NULL;
}

int safe_remove_from_string(char **state, int* length_left, int count) {
    //Safely remove {count} characters from string and remaining length
    if (*length_left < count) {
        PyErr_Format(PyExc_ValueError, "String is not long enough to contain all the parsed information at %s", state);
        return -1;
    }
    *length_left -= count;
    *state += count * SIZE_CHAR;
    return 0;
}

int parseDouble(char **state, int *length_left, double *variable) {
    //Parses a double from the first number, state becomes the first value after 
    char *end;
    errno = 0;
    *variable = strtod(*state, &end);
    if (errno == ERANGE) {
        PyErr_Format(PyExc_ValueError, "Float too large at %s", state);
        return -1;
    } else if (*state == end) {
        PyErr_Format(PyExc_ValueError, "No float found at %s", state);
        return -1;
    }
    *length_left += (*state - end);
    *state = end;
    return 0;
}

int parseVec3(char **state, int *length_left, double **variable) {
    //Parses a Vec3 from the index of the 'V', state becomes first value after the Vec3 quotation
    #define VEC3CHARLENGTH 5 // "Vec3(" is 5 characters long
    int err;
    err = safe_remove_from_string(state, length_left, VEC3CHARLENGTH);
    if (err == -1) {return -1;}
    for (int i = 0; i < 3; i++) {
        err = parseDouble(state, length_left, *variable);
        if (err == -1) {return -1;}
        //Next index
        *variable += sizeof(double);
        //+2 for the ", "
        err = safe_remove_from_string(state, length_left, 2);
        if (err == -1) {return -1;}
    }
}