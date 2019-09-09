# Makefile for Sphinx documentation
#
SPHINXBUILD = sphinx-build
PAPER       = letter
BUILDDIR    = _build
BIBFILE     = xraydb.bib

.PHONY: html all epub latex pdf clean

html: bib
	$(SPHINXBUILD) -a . $(BUILDDIR)/html

epub:
	$(SPHINXBUILD) -a -b epub . $(BUILDDIR)/html

bib:
	touch $(BIBFILE)

all: html pdf

latex: bib
	$(SPHINXBUILD) -a -b latex . $(BUILDDIR)/latex

pdf: latex
	cd $(BUILDDIR)/latex && make all-pdf
	cp -pr $(BUILDDIR)/latex/xraydb.pdf $(BUILDDIR)/html/xraydb.pdf

clean:
	-rm -rf $(BUILDDIR)/*
