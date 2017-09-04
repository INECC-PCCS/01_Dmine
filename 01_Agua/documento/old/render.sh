if [[ -f *.pdf ]]; then
 rm *.pdf;
fi
Rscript -e "library(rmarkdown); render('agua.Rmd')";
