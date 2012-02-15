API_DEPENDENCIES =
API_DEPENDENCIES += preamble/preamble.tex
API_DEPENDENCIES += figures/create-irreg.png
API_DEPENDENCIES += figures/create-ghosts-irreg.png
API_DEPENDENCIES += figures/set-irreg-dist.png
API_DEPENDENCIES += figures/set-block-cyclic.png
API_DEPENDENCIES += figures/set-block-cyclic-proc-grid.png
API_DEPENDENCIES += figures/get.png
API_DEPENDENCIES += ga_api.tex

ga_api.pdf: $(API_DEPENDENCIES)
	pdflatex --shell-escape ga_api.tex
	pdflatex --shell-escape ga_api.tex

clean:
	rm -f *.log *.aux *.pdf *.dvi
