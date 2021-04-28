# -*- coding: utf-8 -*-
"""build.py - sets up Latex structure to compile beamer lectures."""

import os
import sys


def create_main_to_compile(nm,subtit):
    """Create minimum beamer template to compile lecture contents.
        input: source .tex file; lecture subtitle (first line of source .tex )
        output: template file
        return: template file name
    """

    fname = "aula-"+str(nm)+".tex"
    f = open(fname,'w')

    # check existence
    file_checking('./usepacks.tex')         # required packages list
    file_checking('./utilityCommands.tex')  # macros

    # all Latex commands for preamble (should have metropolis theme)
    header="\\documentclass[12pt,xcolor=svgnames]{beamer}\n \
    \\mode<presentation>{\n \
    \\usetheme[sectionpage=progressbar,subsectionpage=progressbar,block=fill]{metropolis}\n \
    \\setbeamertemplate{items}[default]\n \
    \\setbeamertemplate{bibliography item}[book]\n \
    }\n \
    \\input{usepacks}\n \
    \\input{utilityCommands}\n"

    # title, subtitle
    tit = "\\title{Aula " + str(nm) + "}\n"
    subtit = "\\subtitle{" + subtit + "}\n"


    # authorship and institution
    head_info ="\\author{Prof. Dr. Gustavo PEIXOTO DE OLIVEIRA}\n\
    \institute{\n\
    Programa de Pós-Graduação em Engenharia Mecânica \\\\ \n\
    Centro de Tecnologia \\\\ \n\
    Universidade Federal da Paraíba \\\\ \n\
    Brasil \\\\ \n\
    \\texttt{ gcpeixoto.github.io}}\n\
    \\date[]{\\scriptsize{Atualizado em: \\today}}\n"

    # begin,...input,... end
    beg = "\\begin{document}\n"
    beh = "\\begin{frame}\n\
    \\titlepage\n\
    \\end{frame}\n\
    \\begin{frame}{Escopo}\n\
    \\tableofcontents\n\
    \\end{frame}\n"

    inc = "\\input{source/aula-" + str(nm) + "}\n" # include from source

    end = "\\end{document}"

    # write everything to file
    for s in [header,tit,subtit,head_info,beg,beh,inc,end]:
        f.write(s)    

    f.close()

    return fname


def file_checking(fid):
    """Check existence of dependent files."""

    try:
        open(fid,"r")
    except IOError:
      print("Error: missing file " + fid)
      return 0


# main program
if __name__ == '__main__':

    # dir where to save produced lectures
    outDir = 'pdf'
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    # check for argument
    farg = sys.argv
    if len(sys.argv) > 1:        
        aux = farg[1].split(sep='.')
        # check if is .tex file            
        if aux[1] != "tex":
            raise ValueError("Invalid argument for file name! Is a .tex file?")
                    
    if len(farg) == 1:
        
        # go through source files
        for filename in os.listdir('./source'):
            
            if filename.endswith(".tex"):

                nm,ext = os.path.splitext(filename)                
        
                print("Getting " + filename + "...\n" )
            
                nm = nm.split(sep='-')[1] # lecture number

                this = "./source/"+filename
                f = open(this,'r')
                subtitle = f.readline() # assumes to be like '%Subject'
                subtitle = subtitle[1:] # ignore the latex comment char %
                f.close()

                fname = create_main_to_compile(nm,subtitle)

                # command line compilation
                cmd = "latexmk -silent -xelatex " + fname
                print("Compiling " + filename + " with xelatex...\n")
                os.system(cmd)
                fin = fname.split(".")[0] + ".pdf"
                to = "pdf/" + fin
                os.rename(fin,to)

                # remove auxiliary files
                cmdrm = "rm *.aux *.log *.nav *.out *.snm *.toc *.fls *.xdv *.fdb_latexmk " + fname
                os.system(cmdrm)
                        
           
    elif len(farg) == 2: # compile passed file             
        
        filename = farg[1]
        nm = aux[0]
                                                      
        print("Getting " + filename + "...\n" )

        nm = nm.split(sep='-')[1] # lecture number

        this = "./source/"+filename
        f = open(this,'r')
        subtitle = f.readline() # assumes to be like '%Subject'
        subtitle = subtitle[1:] # ignore the latex comment char %
        f.close()

        fname = create_main_to_compile(nm,subtitle)

        # command line compilation
        cmd = "latexmk -xelatex " + fname
        print("Compiling " + filename + " with xelatex...\n")
        os.system(cmd)
        fin = fname.split(".")[0] + ".pdf"
        to = "pdf/" + fin
        os.rename(fin,to)

        # remove auxiliary files
        cmdrm = "rm *.aux *.log *.nav *.out *.snm *.toc *.fls *.xdv *.fdb_latexmk " + fname
        os.system(cmdrm)
            
    print("We're done!")
            