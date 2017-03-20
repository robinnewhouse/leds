
uint8_t ColorCorrectLookup[256] = {0,	1,	1,	1,	2,	2,	2,	3,	3,	4,	4,	4,	5,	5,	5,	6,	6,	7,	7,	7,	8,	8,	8,	9,	9,	10,	10,	10,	11,	11,	12,	12,	13,	13,	13,	14,	14,	15,	15,	16,	16,	17,	17,	17,	18,	18,	19,	19,	20,	20,	21,	21,	22,	22,	23,	23,	24,	24,	25,	25,	26,	26,	27,	27,	28,	28,	29,	29,	30,	30,	31,	31,	32,	32,	33,	34,	34,	35,	35,	36,	37,	37,	38,	39,	39,	40,	41,	41,	42,	42,	43,	44,	44,	45,	46,	46,	47,	48,	48,	49,	50,	50,	51,	52,	53,	54,	55,	56,	57,	57,	58,	59,	60,	61,	62,	63,	64,	64,	65,	66,	67,	68,	69,	70,	71,	72,	72,	73,	74,	75,	76,	77,	78,	79,	80,	81,	82,	83,	83,	84,	85,	86,	87,	88,	89,	90,	91,	92,	93,	94,	95,	96,	97,	98,	99,	100,	101,	102,	103,	105,	106,	107,	108,	109,	110,	111,	112,	114,	115,	116,	117,	118,	119,	120,	121,	123,	124,	125,	126,	128,	129,	130,	131,	133,	134,	135,	137,	138,	139,	140,	142,	143,	144,	146,	147,	148,	149,	151,	152,	153,	155,	156,	158,	159,	161,	163,	164,	166,	167,	169,	171,	172,	174,	175,	177,	179,	180,	182,	183,	185,	187,	188,	190,	191,	193,	195,	197,	199,	201,	203,	205,	207,	209,	211,	213,	215,	217,	219,	221,	223,	225,	227,	229,	231,	233,	235,	237,	239,	241,	243,	245,	247,	249,	251,	253,	255};

static int grbMode;

#define RED_OFFSET   0
#define GREEN_OFFSET 8
#define BLUE_OFFSET  16

#define MAX_NUMBER_OF_COLOR_CHARS        (300 * 16 * 6) /* Let's just call this the highest number of LEDs we support at the moment. Change if ever higher. */
#define NUMBER_OF_COLOR_CHARS_PER_PACKET ((16 / 2) * 3) /* 24 */

char copyBuffer[MAX_NUMBER_OF_COLOR_CHARS];
char modifiedBuffer[MAX_NUMBER_OF_COLOR_CHARS];



/* Return 0 if successful, 1 otherwise. */
int copy(Stoic *stoic)
{
    memset(&copyBuffer, '0', stoic.TOTAL_NUMBER_OF_COLOR_CHARS);

    double globalBrightness = getGlobalBrightness();

    /* define temp holder for RGB data */
    uint32_t sort, index, led_offset, group_offset = 0; /* vars used in routine */
    int      index2                                = 0;

    led_offset = 0;
    while (group_offset < 2) {
        index = sort = 0; /* start at lowest group offset and reset input buffer pointer */

        /* load the input buffer */
        while (sort < NUMBER_OF_COLOR_CHARS_PER_PACKET) {
            if (index < stoic.NUM_BOARDS) { /* data only generated for 12, or whatever number of, panels */
                LED *led = [((Board *)[stoic.boards objectAtIndex:group_offset + index]).leds objectAtIndex:led_offset];

                RGB rgb = [led getCurrentRGB:frameNumber];

                if (grbMode) {
                    copyBuffer[index2 + sort++] = (char)(((double)ColorCorrectLookup[rgb.g]) * globalBrightness);
                    copyBuffer[index2 + sort++] = (char)(((double)ColorCorrectLookup[rgb.r]) * globalBrightness);
                    copyBuffer[index2 + sort++] = (char)(((double)ColorCorrectLookup[rgb.b]) * globalBrightness);
                } else {
                    copyBuffer[index2 + sort++] = (char)(((double)ColorCorrectLookup[rgb.r]) * globalBrightness);
                    copyBuffer[index2 + sort++] = (char)(((double)ColorCorrectLookup[rgb.g]) * globalBrightness);
                    copyBuffer[index2 + sort++] = (char)(((double)ColorCorrectLookup[rgb.b]) * globalBrightness);
                }
            }
            else { /* fill last panels data with 0's */
                copyBuffer[index2 + sort++] = 0;
                copyBuffer[index2 + sort++] = 0;
                copyBuffer[index2 + sort++] = 0;
            }

            index += 2;
        }

        led_offset++; /* move led offset for next loop */

        /* catch reaching the end of the first panel */
        if (led_offset == stoic.NUM_LEDS) {

            led_offset = 0;
            group_offset++;  /* when this reaches 2 the iterations has completed */
        }

        index2 += NUMBER_OF_COLOR_CHARS_PER_PACKET;
    }

    return 0;
}


/* Return 0 if successful, 1 otherwise. */
int sendData(Stoic *stoic)
{
    int status = -1;
    char star = '*';

    status = write_data(serialDevice, &star, sizeof(star));
    if (status < 0) {
        printf("Error writing to serial device!\n");
        return status;
    }

    /* define temp holder for RGB data */
    char grabr = 0;
    char grabg = 0;
    char grabb = 0;
    uint32_t sort, index, light, led_offset, group_offset = 0; /* vars used in routine */
    int index2 = 0;

    led_offset = 0;
    while (group_offset < 2)
    {
        led_offset++; /* move led offset for next loop */

        /* catch reaching the end of the first panel */
        if (led_offset == stoic.NUM_LEDS)
        {
            led_offset = 0;
            group_offset++;  /* when this reaches 2 the iterations has completed */
        }

        /* clear buffer */
        memset(&modifiedBuffer, 0, NUMBER_OF_COLOR_CHARS_PER_PACKET);

        sort = light = 0;
        while (light < 8)
        {
            grabr = copyBuffer[index2 + sort++]; /* get red value   */
            grabg = copyBuffer[index2 + sort++]; /* get green value */
            grabb = copyBuffer[index2 + sort++]; /* get blue value  */

            index = 0;

            while (index < 8)
            {
                if (grabr & (1 << index)) { modifiedBuffer[RED_OFFSET   + (7 - index)] |= (1 << light); }
                if (grabg & (1 << index)) { modifiedBuffer[GREEN_OFFSET + (7 - index)] |= (1 << light); }
                if (grabb & (1 << index)) { modifiedBuffer[BLUE_OFFSET  + (7 - index)] |= (1 << light); }

                index++;
            }

            light++;
        }

        /* use the data */
        status = write_data(serialDevice, modifiedBuffer, NUMBER_OF_COLOR_CHARS_PER_PACKET);
        if (status < 0)
        {
            printf("Error writing to serial device!\n");
            return status;
        }

        index2 += NUMBER_OF_COLOR_CHARS_PER_PACKET;
    }

    return 0;
}
