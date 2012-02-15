API_DEPENDENCIES =
API_DEPENDENCIES += preamble.tex
API_DEPENDENCIES += figures/CrIrreg.png
API_DEPENDENCIES += figures/CrGhostIr.png
API_DEPENDENCIES += figures/SetIrregDist.png
API_DEPENDENCIES += figures/StBlkCy.png
API_DEPENDENCIES += figures/SetBlkCyProcGrid.png
API_DEPENDENCIES += figures/GET.png
API_DEPENDENCIES += ga_api.tex

ga_api.pdf: $(API_DEPENDENCIES)
	pdflatex --shell-escape ga_api.tex
	pdflatex --shell-escape ga_api.tex

clean:
	rm -f *.log *.aux *.pdf *.dvi
