cd gamegridp
python setup.py install
python setup.py sdist
python setup.py bdist_egg
twine upload dist/*
cd ..