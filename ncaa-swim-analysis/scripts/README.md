# Scripts

Python files for data collection and processing.

Includes:
- `Stroke Rate Report.py`: The original script that kicked off this whole project.  It outputs the swimmers race information by aggreageting a series of key presses coinciding with the race.  Each time a swimmer takes a cycle, you press the enter key.  At each turn you press the space key and at the start of the race you press the Backspace key.  After the race the script will ask for various identifying information as well as a swimmer's splits (usually collected from MeetMobile).  It then output a pdf report for the swimmer and coach to view as well as a csv containing all the information from the race, which is then aggreated in the following scripts.
- `MetaDataaggregate.py`: Compiles metadata information from a collection of reports/csvs ran with "Stroke Rate Report.py".  Used for identifying information in Tableau.
- `ExtractWholeRaceSummary.py`:  Compiles the whole race summary from a collection of reports/csvs ran with "Stroke Rate Report.py".  Used to display entire race statistics in Tableau
- `ExtractLapBreakdown.py`: Compiles lap summary information from a collection of reports/csvs ran with "Stroke Rate Report.py".  Used to display lap summary race statistics in Tableau.
