cd gamegridp
python setup.py install
python setup.py sdist
python setup.py bdist_egg
cd ..
cd doc
make html
cd ..
cd gamegridp
twine upload dist/*
cd ..