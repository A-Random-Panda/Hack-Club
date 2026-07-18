#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <limits.h>

static PyObject *
parse_state(PyObject *self, PyObject *args) {
    //('Vec3(0.5, 1.05, 0.5)', 'Vec3(0, -11.712962, 0)', 'DNE', 'DNE', '5.0', 'False', 'Vec3(0.5, 1.05, 0.5)', 'Vec3(0, -11.712962, 0)')
    const char * state_string;
    int cameraCount;
    int player_dead;
    double player_pos[3];
    double player_rotation[3];

    if (!PyArg_ParseTuple(args, "s", &state_string)) {
        return NULL;
    }
    int count = 0;
    while (state_string[count] != '\0') {
        //
    }
}