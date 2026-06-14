#include <stdio.h>
#include <stdlib.h>

int current_brightness(){
    FILE * current = fopen("/sys/class/backlight/radeon_bl0/brightness", "r");
    if (current == NULL){
        return -1;
    }
    int value;
    fscanf(current, "%d", &value);
    fclose(current);
    return value;
}

void write_brightness(int brightness){
    FILE * current = fopen("/sys/class/backlight/radeon_bl0/brightness", "w");
    fprintf(current, "%d", brightness);
    fclose(current);
}

int main(int argc, char *argv[]){
    if (argc < 2){
        perror("error code 0.");
        return 1;
    }
    else if (argc == 2){
        FILE * max_brightness = fopen("/sys/class/backlight/radeon_bl0/max_brightness", "r");
        if (max_brightness == NULL){
            perror("wrong file directory error code 1");
            return 1;
        }
        int max_brightness_val;
        fscanf(max_brightness, "%d", &max_brightness_val);

        int brightness;
        if (argv[1][0] == '+'){
            brightness = atoi(&argv[1][1]);
            //get current from file than add to it write new val
            int current = current_brightness();
            brightness += current;
        }
        else if (argv[1][0] == '-'){
            int val = atoi(argv[1]);
            int current = current_brightness();
            brightness = current + val;
        }
        else{
            int input = atoi(argv[1]);
            brightness = (max_brightness_val * input)/100;
        }
        if (brightness <= max_brightness_val && brightness >= 0){
                write_brightness(brightness);
                fclose(max_brightness);
                return 0;
        }
        else{
            fclose(max_brightness);
            return 1;
        }
    }
    return 0;
}
