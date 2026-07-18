#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <limits.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#define MAX_CAMERAS 11
#define MINIMUM_LENGTH 20 //Don't have an exact minumum, but I don't think it'll be necessary, honestly
#define INTEGER_START_INDEX 2

static PyObject *
parse_state(PyObject *self, PyObject *args) {
    //('1', '[Vec3(0.5, 1.05, 0.5)]', '[Vec3(0, 10.277778, 0)]', 'DNE', 'DNE', '5.0', 'False', 'Vec3(0.5, 1.05, 0.5)', 'Vec3(0, 10.277778, 0)')
    //('amount of player cams', 'player cams position: list[vec3]', 'player cams rotation: list[vec3]', 'bullet trail: entity', 'bullet trail position: vec3', 'reload time: float', 'player dead: bool', 'player world position: vec3', 'player rotation: vec3')
    const char * stateString;
    int cameraCount;
    int playerDead;
    double playerPos[3];
    double playerRotation[3];

    if (!PyArg_ParseTuple(args, "s", &stateString)) {
        return NULL;
    }
    //Check that the string is at least 3 characters long (I assume that it is later on)
    if (strlen(stateString) > MINIMUM_LENGTH) {
        PyErr_SetString(PyExc_ValueError, "String is not long enough to contain all the parsed information");
        return NULL;
    }
    //The string is a list converted to a string, so the third character is always an integer
    int count = INTEGER_START_INDEX;
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
        PyErr_SetString(PyExc_ValueError, "A maximum camera amount must be provided");
        return NULL;
    } else {
        //The integer is over 99
        PyErr_Format(PyExc_ValueError, "Maximum cameras must be at most %d!", MAX_CAMERAS);
        return NULL;
    }
    //Check if the number is over 11
    if (cameraCount > 11) {
        PyErr_Format(PyExc_ValueError, "Maximum cameras must be at most %d!", MAX_CAMERAS);
        return NULL;
    }
    //Count is now at the index of the comma
    for (int i = count; i < count; i++) {

    }
    while (stateString[count] != '\0') {
        
    }
}