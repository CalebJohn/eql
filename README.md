eql
=======

eql is a mathematical grammar meant for simple keyboard only calculations. The purpose is to enable low friction calculations that I've grown accustomed to on my Casio fx-260SOLAR.

![Casio fx-260SOLAR calculator](https://github.com/CalebJohn/eql/blob/master/media/casio.png)

# Command line usage
Place the cli.py script in your bin/ folder (I named mine `=` so it's accessible from anywhere as `=`, example: `= 2+2`). Note: when in bash some symbols (e.g. \(\)) have special meaning so you'll need to invoke the script with quotes (example: `= "2*2"`).

Invoking the cli without arguments will enter a **very** basic interactive mode. This is sometimes helpful for longer calculations, if doing a lot of long calculations please consider an environment better suited for it (e.g. using a script).

If you want to use the optional sympy evaluator, you'll need to install sympy version 1.9 (or greater)
