#!/usr/bin/python3

import sys
import subprocess
import pathlib
import tempfile

def latex_document(latex):
    return r"""
        \documentclass[14pt,border=12pt]{minimal}

        \usepackage[utf8]{inputenc}
        \usepackage[T1]{fontenc}
        \usepackage{textcomp}
        \usepackage{amsmath, amssymb}
        \usepackage{xcolor}

        \begin{document}
        \pagestyle{empty}
    """ + latex + r"\end{document}"

def main(latex):
    m = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    print(latex_document(latex))
    m.write(latex_document(latex))
    m.close()

    working_directory = tempfile.gettempdir()
    subprocess.run(
        ['pdflatex', m.name],
        cwd=working_directory,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    print(m.name)
    subprocess.run(
        ['pdf2svg', f'{m.name}.pdf', f'{m.name}.svg'],
        cwd=working_directory,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    with open(f'{m.name}.svg') as svg:
        subprocess.run(
            ['xclip', '-selection', 'c', '-target', 'image/x-inkscape-svg'],
            stdin=svg
        )

if __name__ == "__main__":
    latex = pathlib.Path(sys.argv[1]).read_text()
    main(latex)
