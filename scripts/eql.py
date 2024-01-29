#!/usr/bin/env python3


import argparse
import atexit
import cmd
import fractions
import numbers
import os
import re
import readline
import tempfile


from eql.evaluator import evaluate
from eql.infix import to_infix
from eql.parser import parse


def frac(n: numbers.Number) -> str:
    # as_integer_ratio works, but was only added in 3.8
    if type(n) == fractions.Fraction:
        return str(n)

    n, d = n.as_integer_ratio()
    if abs(d) < 1000:
        return f"{n}/{d}"
    return str(n)


def save_history(filename):
    readline.set_history_length(1000)
    readline.write_history_file(filename)


def load_history():
    tmp_dir = tempfile.gettempdir()
    tmp_name = 'eql.hist'
    hist_file = os.path.join(tmp_dir, tmp_name)
    if not os.path.exists(hist_file):
        open(hist_file, 'a').close()
    readline.read_history_file(hist_file)
    atexit.register(save_history, hist_file)


class EqlShell(cmd.Cmd):
    """
    Pronounced E.Q.L Shell
    """
    intro = """\
    eeeee  qqqq  ll
    e      q   q  ll
      eeeee  qqqq  ll
       e         q  ll
        eeeee      qq ll
    """
    prompt_format = "${}>"
    register_regex = re.compile("\$(\d+)")

    def __init__(self, fraction=False, verbose=False, sympy=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registers = ['']
        self.prompt = self.prompt_format.format(0)
        self.display_fraction = fraction
        self.verbose = verbose
        self.sympy = sympy
        self.evaluator = evaluate
        if sympy:
            import sympy
            self.sympy = sympy
            self.evaluator = lambda x: sympy.sympify(to_infix(x))

    def update_history(self):
        hlength = readline.get_current_history_length()
        readline.replace_history_item(hlength - 1, self.registers[-1])

    def preloop(self):
        load_history()

    # This is where we can make substitutions for $X
    def precmd(self, line):
        for register in set(re.findall(self.register_regex, line)):
            line = line.replace(
                f"${register}", f"({self.registers[int(register)]})")

        return line

    def default(self, line):
        if line == "EOF":
            return self.do_quit()

        eqn = line
        if self.registers[-1]:
            eqn = f"{self.registers[-1]} {line}"

        if self.verbose:
            print(eqn)

        try:
            result = self.evaluator(parse(eqn))
            if self.display_fraction and self.sympy:
                result = self.sympy.Rational(result)
            elif not self.display_fraction and not self.sympy:
                if type(result) != complex:
                    result = float(result)

            print(result)
            self.registers[-1] = eqn
            # self.update_history()
            # readline.add_history(self.registers[-1])
        except Exception as e:
            print(e)

    # advance to the next register
    def emptyline(self):
        if not self.registers[-1]:
            return

        print(
            f"{to_infix(parse(self.registers[-1]))} = {self.evaluator(parse(self.registers[-1]))}")
        readline.add_history(self.registers[-1])

        self.registers.append('')
        self.prompt = self.prompt_format.format(len(self.registers) - 1)

    def do_f(self, *args):
        """
        Toggle fraction mode
        """
        self.display_fraction = not self.display_fraction

    def do_v(self, *args):
        """
        Toggle verbose mode
        """
        self.verbose = not self.verbose

    def do_q(self, *args):
        """Quit"""
        return self.do_quit()

    def do_quit(self, *args):
        """Quit"""
        return True


def main():
    parser = argparse.ArgumentParser(description="eql is a mathematical grammar meant for simple keyboard only calculations.")

    parser.add_argument('equation', type=str, nargs='*', help='The equation. Wrap in quotes to avoid bash getting in the way.')
    parser.add_argument('-f', '--fraction', action='store_true',
                        default=False, help="Display decimal results as a fraction.")
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help="Output the entire equation at every step.")
    parser.add_argument('-s', '--sympy', action='store_true', default=False,
                        help="Use sympy as the execution engine. Not recommended because it's slow and the current version of eql does not take full advantage of it.")
    args = parser.parse_args()

    shell = EqlShell(args.fraction, args.verbose, args.sympy)

    if args.equation:
        shell.onecmd(' '.join(args.equation))
    else:
        shell.cmdloop()

if __name__ == "__main__":
    main()
