API_DEPENDENCIES =
API_DEPENDENCIES += preamble.tex
API_DEPENDENCIES += otype.tex
API_DEPENDENCIES += CrIrreg.png
API_DEPENDENCIES += CrGhostIr.png
API_DEPENDENCIES += SetIrregDist.png
API_DEPENDENCIES += StBlkCy.png
API_DEPENDENCIES += SetBlkCyProcGrid.png
API_DEPENDENCIES += GET.png
API_DEPENDENCIES += ga_api_FR.tex

ga_api_FR.pdf: $(API_DEPENDENCIES)
	pdflatex ga_api_FR.tex

jefftest.pdf: jefftest.tex
	pdflatex --shell-escape jefftest.tex

clean:
	rm -f *.log *.aux *.pdf *.dvi
