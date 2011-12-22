API_DEPENDENCIES =
API_DEPENDENCIES += preamble.tex
API_DEPENDENCIES += CrIrreg.png
API_DEPENDENCIES += CrGhostIr.png
API_DEPENDENCIES += SetIrregDist.png
API_DEPENDENCIES += StBlkCy.png
API_DEPENDENCIES += SetBlkCyProcGrid.png
API_DEPENDENCIES += GET.png
API_DEPENDENCIES += ga_api.tex

ga_api.pdf: $(API_DEPENDENCIES)
	pdflatex --shell-escape ga_api.tex
	pdflatex --shell-escape ga_api.tex

clean:
	rm -f *.log *.aux *.pdf *.dvi
