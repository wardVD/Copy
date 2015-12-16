#!/bin/sh
python cmgPostProcessing.py --skim=$1 $2 --samples=WWDouble   &
python cmgPostProcessing.py --skim=$1 $2 --samples=WpWpJJ   &
python cmgPostProcessing.py --skim=$1 $2 --samples=WWZ   &
python cmgPostProcessing.py --skim=$1 $2 --samples=WZZ   &
python cmgPostProcessing.py --skim=$1 $2 --samples=ZZZ   &
python cmgPostProcessing.py --skim=$1 $2 --samples=TTWToLNu   &
python cmgPostProcessing.py --skim=$1 $2 --samples=TTWToQQ   &
python cmgPostProcessing.py --skim=$1 $2 --samples=TTZToQQ   &
python cmgPostProcessing.py --skim=$1 $2 --samples=TTZToLLNuNu   &
python cmgPostProcessing.py --skim=$1 $2 --samples=TTGJets   &
