# Makefile for xray periodic table

TARGET = xray_table
PDFLATEX = pdflatex


.PHONY: clean distclean all sees

all:
	make xray_table_50in_Barkla.pdf
	make xray_table_50in_Curie.pdf
	make xray_table_50in_Mendeleev.pdf
	make xray_table_50in_Moseley.pdf
	make xray_table_36in_Barkla.pdf
	make xray_table_36in_Curie.pdf
	make xray_table_36in_Mendeleev.pdf
	make xray_table_36in_Moseley.pdf
	make xray_table_36in_SEES.pdf
	make xray_table_50in_SEES.pdf

sees:
	make xray_table_36in_SEES.pdf
	make xray_table_50in_SEES.pdf

atoms.tex:  gen_atoms.py
	python gen_atoms.py > atoms.tex

xray_table_36in_SEES.pdf: atoms.tex elines.tex ptable_seeslogo.tex header.tex xray_table_36in_SEES.tex
	$(PDFLATEX) xray_table_36in_SEES.tex

xray_table_50in_SEES.pdf: atoms.tex elines.tex ptable_seeslogo.tex header.tex xray_table_50in_SEES.tex
	$(PDFLATEX) xray_table_50in_SEES.tex

xray_table_50in_Curie.pdf: atoms.tex elines.tex ptable.tex xray_table_50in_Curie.tex
	$(PDFLATEX) xray_table_50in_Curie.tex

xray_table_50in_Barkla.pdf: atoms.tex elines.tex ptable.tex xray_table_50in_Barkla.tex
	$(PDFLATEX) xray_table_50in_Barkla.tex

xray_table_50in_Mendeleev.pdf: atoms.tex elines.tex ptable.tex xray_table_50in_Mendeleev.tex
	$(PDFLATEX) xray_table_50in_Mendeleev.tex

xray_table_50in_Moseley.pdf: atoms.tex elines.tex ptable.tex xray_table_50in_Moseley.tex
	$(PDFLATEX) xray_table_50in_Moseley.tex

xray_table_36in_Curie.pdf: atoms.tex elines.tex ptable.tex xray_table_36in_Curie.tex
	$(PDFLATEX) xray_table_36in_Curie.tex

xray_table_36in_Barkla.pdf: atoms.tex elines.tex ptable.tex xray_table_36in_Barkla.tex
	$(PDFLATEX) xray_table_36in_Barkla.tex

xray_table_36in_Mendeleev.pdf: atoms.tex elines.tex ptable.tex xray_table_36in_Mendeleev.tex
	$(PDFLATEX) xray_table_36in_Mendeleev.tex

xray_table_36in_Moseley.pdf: atoms.tex elines.tex ptable.tex xray_table_36in_Moseley.tex
	$(PDFLATEX) xray_table_36in_Moseley.tex


clean:
	rm -f *.log *.aux *.pyc *.synctex.gz

distclean:
	make clean
	rm -f *.pdf atoms.tex
