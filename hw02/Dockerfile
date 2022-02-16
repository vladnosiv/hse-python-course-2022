FROM python:3.9

COPY hw02.py hw02.py
COPY fib.py fib.py

RUN apt-get update
RUN apt-get install -y graphviz graphviz-dev python3-pygraphviz
RUN apt-get install -y texlive
RUN python3.9 -m pip install poetry

WORKDIR artifacts
RUN poetry install
RUN poetry run hw02.py
RUN pdflatex hw02.tex
