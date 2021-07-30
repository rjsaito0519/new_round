import sys

def get_digit(number):
    numberList = list("{:e}".format(number))
    return int("{}{}{}".format(numberList[-3],numberList[-2],numberList[-1]))

def stderr_analysis(err):
    err = list("{:e}".format(abs(err)))

    roundDigit = 0
    textErr = ""
    stderr = None
    for i, item in enumerate(err):
        if i == roundDigit + 2:
            if int(item) >= 5:
                stderr = round(float(textErr) + 1*10**(-roundDigit), roundDigit)
            else:
                stderr = round(float(textErr), roundDigit)
            break
        textErr += item
        if i == 0 and int(item) < 5: roundDigit += 1
    
    return stderr, roundDigit

def value_analysis(valueNum, digitMove):
    sign = int(valueNum/abs(valueNum))
    valueNum = list("{:e}".format(valueNum))
    valueDigit = int("{}{}{}".format(valueNum[-3],valueNum[-2],valueNum[-1]))

    counter = 0
    countStart = False
    addText = True
    maxDigit = valueDigit+digitMove
    valueText = ""
    value = None
    for item in valueNum:
        
        if counter == maxDigit:
            try:
                if int(item) >= 5:
                    value = round(float(valueText) + sign*10**(-maxDigit), maxDigit)
                else:
                    value = round(float(valueText), maxDigit)
                break
            except:
                value = round(float(valueText), maxDigit)
                break
        if item == "e":
            addText = False
        if addText:
            valueText += item
        else:
            valueText += "0"
        if countStart:
            counter += 1
        if item == ".":
            countStart = True
        if item == valueNum[-1]:
            value = round(float(valueText), maxDigit)

    return value

def new_round(rawValue, rawStderr, style = "number", dimension = ""):
    stderrDigit = get_digit(rawStderr)
    valueDigit = get_digit(rawValue)
    stderr, roundDigit = stderr_analysis(rawStderr)
    value = value_analysis(rawValue, roundDigit - stderrDigit)
    if style == "number":
        if stderrDigit >= roundDigit:
            return int(value*10**valueDigit), int(stderr*10**stderrDigit)
        else:
            return value*10**valueDigit, stderr*10**stderrDigit
    elif style == "latex":
        if dimension != "":
            return r"$({} \pm {}) \times 10^{} [{}]$".format( value, stderr, valueDigit, dimension)
        else:
            return r"$({} \pm {}) \times 10^{}$".format( value, stderr, valueDigit)
    elif style == "legend":
        if stderrDigit >= roundDigit:
            if dimension != "":    
                return "{} ± {} [{}]".format( int(value*10**valueDigit), int(stderr*10**stderrDigit), dimension)
            else:
                return "{} ± {}".format( int(value*10**valueDigit), int(stderr*10**stderrDigit) )
        else:
            if dimension != "":    
                return "{} ± {} [{}]".format( value*10**valueDigit, stderr*10**stderrDigit, dimension)
            else:
                return "{} ± {}".format( value*10**valueDigit, stderr*10**stderrDigit )
    elif style == "legend_e":
        if dimension != "":
            return "({} ± {}) × 10$^{}$ [{}]".format( value, stderr, valueDigit, dimension)
        else:
            return "({} ± {}) × 10$^{}$".format( value, stderr, valueDigit)

if __name__ == '__main__':
    print(new_round(float(sys.argv[1]), float(sys.argv[2])))