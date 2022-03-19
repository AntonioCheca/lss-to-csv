# lss-to-csv
Generate csv file from livesplit lss file

## Usage:

python LssToCsv.py TheMessenger.lss TheMessenger.csv [-time ms] [-h]

TIME can be nothing, which will create the csv with the hh:mm:ss.abcdefg format of lss files, or ms, which will transform that format to number of milliseconds. This way you can do graphics with the times in excel or calc.
