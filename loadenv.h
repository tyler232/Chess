#ifndef LOADENV_H
#define LOADENV_H

#define MAX_LINE_LENGTH 256

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * Function to remove leading and trailing whitespace from a string
 * @param str The string to trim
 * @return The trimmed string
 */
char *trim_whitespace(char *str) {
    while (*str == ' ' || *str == '\t') str++;
    char *end = str + strlen(str) - 1;
    while (end > str && (*end == ' ' || *end == '\t')) end--;
    *(end + 1) = '\0';
    return str;
}

/**
 * Function to load environment variables from a file
 * @param filename The name of the file to load
 */
void load_env(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Unable to open .env file");
        return;
    }

    char line[MAX_LINE_LENGTH];
    while (fgets(line, sizeof(line), file)) {
        // Skip empty lines and comments
        if (line[0] == '\n' || line[0] == '#') continue;

        // Split line into key and value
        char *key = strtok(line, "=");
        char *value = strtok(NULL, "\n");

        if (key && value) {
            // Remove leading/trailing whitespace
            key = trim_whitespace(key);
            value = trim_whitespace(value);

            // Set environment variable
            setenv(key, value, 1);
        }
    }

    fclose(file);
}

#endif