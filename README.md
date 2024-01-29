eql
=======

eql is a mathematical grammar meant for simple keyboard only calculations. The purpose is to enable low friction calculations that I've grown accustomed to on my [Casio fx-260SOLAR](https://github.com/CalebJohn/eql/blob/master/media/casio.png).

eql uses most of the same bedmas (pemdas) operations that you're probably already accustomed to, but adds whitespace as a new operator (wbedmas). Whitespace functions as an accumulator that enables grouping of operations without parenthesis. Let's see what that looks like.

`1+2 *6` is equivalent to `(1+2)*6`

In the above example, the calculation is "accumulated" after 1+2. This demonstrates the primary benefit of accumulation, namely, it allows you to benefit from parenthesis as you type (rather than having to plan out the entire calculation ahead of time).

eql follows bedmas in most areas, which means that logical grouping by operator still works as expected.

```
2+2 *3+4 = (2+2)*3+4 = 12+4 = 16
2+2 +3*3 = (2+2)+3*3 = 4+9 = 13
```

Parenthesis also work as expected.

```
(1+2 *6+2)*3 = ((1+2)*6+3)*3 = 60
```

eql also supports some functions. Functions use Polish notation, and can drop the parenthesis for single number argument functions.

```
gcd(9,8) *32+4 = gcd(9, 8)*32+4
sin(2+4 *6) = sin((2+4)*6)
tan(2)+ 6*sin58 = tan(2)+6*sin(58)
```

## Command line usage
Place the cli.py script in your bin/ folder (I named mine `=` so it's accessible from anywhere as `=`, example: `= 2+2`). Note: when in bash some symbols (e.g. \(\)) have special meaning so you'll need to invoke the script with quotes (example: `= "2*2"`).

Invoking the cli without arguments will enter a **very** basic interactive mode. This is sometimes helpful for longer calculations, if doing a lot of long calculations please consider an environment better suited for it (e.g. using a script).

If you want to use the optional sympy evaluator, you'll need to install sympy version 1.9 (or greater)

For NixOS users (with flakes enabled) you can test it out easily with

```
nix run github:CalebJohn/eql
```
