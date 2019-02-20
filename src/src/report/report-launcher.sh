jupyter nbconvert --to html "notebooks/$1.ipynb" --TemplateExporter.exclude_input=True --execute
mv -f notebooks/$1.html email.html
