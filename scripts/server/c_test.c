#include <stdio.h>

int main() {
    double dbl[3];
    double d;
    double doob[3][2];
    //parseVec3("Vec3(2, 10.277778, 2)", dbl);
    //parseDouble("3.6969", &d);
    parseListVec3("[Vec3(69, 1, 2), Vec3(5, 6, 7)]", &doob, 2);
    //printf("Vec3:\n%lf\n%lf\n%lf\n", dbl[0], dbl[1], dbl[2]);
    //printf("Double:\n%lf\n", d);
    printf("ListVec3:\n%lf\n%lf\n%lf\n%lf\n%lf\n%lf\n",
        doob[0][0],doob[0][1],doob[0][2],doob[1][0],doob[1][1],doob[1][2]);
    return 0;
}

int parseListVec3(char *str, double (*result)[3], int amount) {
    //Not exactly sure how sscanf works, but I'm just praying that it works at this point
    int matched;
    if (amount == 1) {
        matched = sscanf(str, "Vec3(%lf, %lf, %lf)", result+4, result+5,result+6);
    if (matched != 3) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    if (amount == 2) {
        matched = sscanf(str, "Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)", result+7, result+8,result+9);
        if (matched != 6) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    if (amount == 3) {
        matched = sscanf(str, "Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)", result+10, result+11,result+12);
        if (matched != 9) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    if (amount == 4) {
        matched = sscanf(str, "Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)", result+13, result+14,result+15);
        if (matched != 12) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    if (amount == 5) {
        matched = sscanf(str, "Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)", result+16, result+17,result+18);
        if (matched != 15) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    if (amount == 6) {
        matched = sscanf(str, "Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)", result+19, result+20,result+21);
        if (matched != 18) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    if (amount == 7) {
        matched = sscanf(str, "Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)", result+22, result+23,result+24);
        if (matched != 21) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    if (amount == 8) {
        matched = sscanf(str, "Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)", result+25, result+26,result+27);
        if (matched != 24) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    if (amount == 9) {
        matched = sscanf(str, "Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)", result+28, result+29,result+30);
        if (matched != 27) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    if (amount == 10) {
        matched = sscanf(str, "Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)", result+31, result+32,result+33);
        if (matched != 30) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    if (amount == 11) {
        matched = sscanf(str, "Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf), Vec3(%lf, %lf, %lf)", result+34, result+35,result+36);
        if (matched != 33) {
            printf("%d Matched\n", matched);
            return -1;
        }
    }
    printf("returned 0");
    return 0;
}

int parseVec3(char *str, double *result) {
    //Not exactly sure how sscanf works, but I'm just praying that it works at this point
	int matched = sscanf(str, "Vec3(%lf, %lf, %lf)", result, result+1, result+2);
    if (matched != 3) {
		printf("%d Matched\n", matched);
        return -1;
    }
    return 0;
}

int parseDouble(char *str, double *result) {
	int matched = sscanf(str, "%lf", result);
    if (matched != 1) {
		printf("%d Matched\n", matched);
        return -1;
    }
    return 0;
}
main();