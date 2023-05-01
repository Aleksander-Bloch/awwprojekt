var editor1 = (function () {
    var aceEditor = ace.edit("program-viewer");
    // default theme
    aceEditor.setTheme("ace/theme/monokai");
    aceEditor.getSession().setMode("ace/mode/c_cpp");
    aceEditor.setOptions({
        fontSize: "14pt"
    });
    aceEditor.setValue(`#include <stdio.h>
#include <ctype.h>
#include <assert.h>
#include "error.h"
#include "input-utilities.h"
#include "hex-utilities.h"


/*
* Parses through the prefix of the hexadecimal number.
* If it is not in the correct format, it throws line number error.
*  currentCharacter - pointer to currently read character
*  lineNumber - line number of the hexadecimal prefix (1-indexed)
*/
static void parseHexPrefix(int *currentCharacter, int lineNumber) {
    ignoreWhitespace(currentCharacter);
    if (*currentCharacter != '0') {
        handleError(lineNumber);
    }
    *currentCharacter = getchar();
    if (*currentCharacter != 'x') {
        handleError(lineNumber);
    }
    *currentCharacter = getchar();

    if (isxdigit(*currentCharacter)) {
        if (*currentCharacter == '0') {
            skipLeadingZeroes(currentCharacter);
            // Traversed all zeroes and potentially this is valid 0x0.
            if (!isxdigit(*currentCharacter)) {
                ungetc(*currentCharacter, stdin);
                *currentCharacter = '0';
            }
        }
    }
    else {
        // 0x alone is invalid.
        handleError(lineNumber);
    }
}

/*
* Sets hexadecimal digit in the bitset.
* It is represented in big-endian notation.
*  b - binary number represented by bitset
*  hex - hexadecimal digit to be set
*  startingBit - position of the first bit to be set (0-indexed)
*/
void setHex(Bitset b, unsigned char hex, size_t startingBit) {
    // Hex digits are allocated continuously as 4-bits.
    assert(startingBit % 4 == 0);
    // Bitset is represented by an array of 8-bit memory blocks.
    // Because of that two hex digits have to fit in a block.
    if (startingBit % UNIT_SIZE == 4) {
        hex <<= (UNIT_SIZE / 2);
    }
    b[startingBit / UNIT_SIZE] |= hex;

    // Switch from little-endian to big-endian
    for (int i = 0; i < 2; i++) {
        swapBits(b, startingBit + i, startingBit + 3 - i);
    }
}

/*
* Parses hexadecimal number from stdin to binary number represented
* by bitset. Returns number of bits read including leading zeroes.
*  currentCharacter - pointer to currently read character
*  binaryNumber - loading destination of hexadecimal number
*  hexDigitsLimit - upper threshold of hex digits allowed to be loaded
*  lineNumber - number of line where the hexadecimal is
*/
size_t parseHexToBinary(int *currentCharacter, Bitset binaryNumber,
                        size_t hexDigitsLimit, int lineNumber) {
    parseHexPrefix(currentCharacter, lineNumber);

    size_t hexDigitsRead = 0;

    while (hexDigitsRead < hexDigitsLimit && isxdigit(*currentCharacter)) {
        *currentCharacter = tolower(*currentCharacter);
        // Utility char used to convert from ASCII code
        // of hex digit to its decimal value.
        unsigned char special = (isdigit(*currentCharacter)) ? '0':('a' - 10);
        // Hex digit in decimal base.
        unsigned char indexOfHexDigit = (*currentCharacter) - special;
        setHex(binaryNumber, indexOfHexDigit, 4 * hexDigitsRead);
        hexDigitsRead++;
        *currentCharacter = getchar();
    }

    // Returns number of bits read.
    return 4 * hexDigitsRead;
}`, 1)
    return aceEditor;
})();

var editor2 = (function () {
    var aceEditor = ace.edit("fragment-viewer");
    // default theme
    aceEditor.setTheme("ace/theme/monokai");
    aceEditor.getSession().setMode("ace/mode/c_cpp");
    aceEditor.setOptions({
        fontSize: "14pt"
    });
    aceEditor.setValue(`/*
* Sets hexadecimal digit in the bitset.
* It is represented in big-endian notation.
*  b - binary number represented by bitset
*  hex - hexadecimal digit to be set
*  startingBit - position of the first 
*                bit to be set (0-indexed)
*/
void setHex(Bitset b, unsigned char hex, 
            size_t startingBit) {
    // Hex digits are allocated 
    // continuously as 4-bits.
    assert(startingBit % 4 == 0);
    // Bitset is represented by an array
    // of 8-bit memory blocks.
    // Because of that two hex digits have
    //  to fit in a block.
    if (startingBit % UNIT_SIZE == 4) {
        hex <<= (UNIT_SIZE / 2);
    }
    b[startingBit / UNIT_SIZE] |= hex;

    // Switch from little-endian to 
    // big-endian
    for (int i = 0; i < 2; i++) {
        swapBits(b, startingBit + i, 
        startingBit + 3 - i);
    }
}`, 1)
    return aceEditor;
})();

var theme_icon = document.getElementById("theme-icon");
var current_theme = localStorage.getItem("theme");

if (current_theme == "light") {
    theme_icon.className = "fa-regular fa-moon";
    document.body.classList.toggle("light-theme");
    editor1.setTheme("ace/theme/light");
    editor2.setTheme("ace/theme/light");
}

theme_icon.onclick = function () {
    document.body.classList.toggle("light-theme");
    if (document.body.classList.contains("light-theme")) {
        localStorage.setItem("theme", "light");
        theme_icon.className = "fa-regular fa-moon";
        editor1.setTheme("ace/theme/light");
        editor2.setTheme("ace/theme/light");
        window.location.reload();
    } else {
        localStorage.setItem("theme", "dark");
        theme_icon.className = "fa-regular fa-sun";
        editor1.setTheme("ace/theme/monokai");
        editor2.setTheme("ace/theme/monokai");
        window.location.reload();
    }
}
