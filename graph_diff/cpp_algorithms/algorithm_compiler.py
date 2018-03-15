import os
import subprocess

import stringcase

from graph_diff.cpp_algorithms import parameters


class AlgorithmCompiler:
    FILENAME = parameters.FILENAME
    EXE_FILENAME = parameters.EXE_FILENAME
    SUPPORTED_ALGORITHMS = parameters.SUPPORTED_ALGORITHMS
    CPP_COMPILER = parameters.CPP_COMPILER
    CPP_OPTIMIZATION = parameters.CPP_OPTIMIZATION
    CPP_STANDARD = parameters.CPP_STANDARD

    def __init__(self):
        for algo in self.SUPPORTED_ALGORITHMS:
            def new_method():
                """Refer to docstring of method `new_method`."""
                return self.compile(algo)

            name = 'compile_{}'.format(stringcase.snakecase(algo))
            self.__setattr__(name, new_method)

    def compile(self, algorithm: str) -> str:
        assert algorithm in self.SUPPORTED_ALGORITHMS

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        print(os.getcwd())
        print(__file__)
        print(os.path.dirname(__file__))

        print(__location__)
        filename = os.path.join(__location__, self.FILENAME)

        cmd = [self.CPP_COMPILER,
               self.CPP_OPTIMIZATION,
               self.CPP_STANDARD,
               filename,
               '-o', self.EXE_FILENAME,
               '-D', 'Algorithm={}'.format(algorithm)]
        p = subprocess.Popen(cmd)
        p.wait()

        return self.EXE_FILENAME
