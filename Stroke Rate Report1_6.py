import time
import statistics
import keyboard
import os
import numpy as np
import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv
from datetime import datetime

### CHANGE THE BELOW ###
# Define the base file path (this can be dynamically set based on user input or a predefined location)
file_path = "H:\\ASU\\ASU Race Reports\\Eddie Reese\\200 Fly\\"
# Define the opponent name at the top of the script
opponent_name = "Eddie Reese"
### NO MORE CHANGES ###


class Stopwatch:
    def __init__(self, csv_file="C:\\Python\\Stroke Rates\\Stroke_Rates.csv", pdf_file="C:\\Python\\Stroke Rates\\Stroke_Rates.pdf", threshold=2):
        self.start_time = None
        self.previous_lap_time = None  # To track the last cycle's time
        self.cycles = []
        self.lap_times = []  # To store lap times
        self.lap_strokes = {}  # To store stroke times per lap
        self.csv_file = csv_file
        self.pdf_file = pdf_file
        self.threshold = threshold  # Threshold set to 2 seconds for strokes
        self.lap_number = 1  # Track the lap number, start at 1
        self.lap_start_time = None  # Time when the current lap started
        self.turn_count = 0  # Track the number of turns
        self.lap_cycles = {}  # To track the number of cycles per lap
        self.cycle_counter = 0  # This will keep track of valid cycles
        self.start_recorded = False  # To track if the "Start" has been recorded
        self.first_stroke_time = None  # To store the time of the first stroke after the race starts
        self.skip_next_stroke = False  # Flag to skip first stroke after a turn
        self.distance = 0
        self.splits = []  # Store the manually entered 50m splits

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)

    def start(self):
        print("Script loaded. Press Backspace to start the timer.")
        while not keyboard.is_pressed('backspace'):
            pass  # Wait until Backspace is pressed to start the race
        self.reaction_time_adjustment = .3  # Automatically apply 1-second adjustment for breakout time if needed
        self.start_time = time.time()  # Start the timer (Backspace press)
        self.lap_start_time = self.start_time  # Initialize the start of the first lap
        self.previous_lap_time = self.start_time  # Initialize previous cycle time with the start time
        self.skip_next_stroke = True  # Flag to skip the breakout stroke at the race start
        self.breakout_time = None  # Initialize breakout time to None
        self.breakout_registered = False  # Track if the first breakout stroke has been registered
        self.turn_skip_next_stroke = False  # Separate flag for skipping strokes after turns
        print("Timer started! Press Enter for the breakout stroke (won't be counted), then press Enter again for the first cycle.")

    def cycle(self):
        current_time = time.time()
        cycle_time = current_time - self.previous_lap_time  # Time since the last cycle or turn

        if self.skip_next_stroke and not self.breakout_registered:
            if self.breakout_time is None:  # Only set this once for the first breakout stroke
                self.breakout_time = (current_time - self.start_time) + self.reaction_time_adjustment  # Add the adjustment
                print(f"First breakout stroke registered (not counted). Breakout time: {self.breakout_time:.2f} seconds")
            self.previous_lap_time = current_time  # Reset the timer for the next stroke
            self.breakout_registered = True  # Mark the breakout stroke as registered
            self.skip_next_stroke = False  # Disable the skip flag now that the breakout is registered
            return  # Do not count this as a cycle

        if self.turn_skip_next_stroke:
            print(f"Skipping first stroke after turn. Lap {self.lap_number}")
            self.previous_lap_time = current_time  # Reset the timer for the next stroke
            self.turn_skip_next_stroke = False  # Reset the turn flag after skipping
            return  # Do not count this as a cycle

        self.cycle_counter += 1  # Increment only for valid strokes
        self.cycles.append((self.cycle_counter, cycle_time, self.lap_number))  # Append cycle number, time, and lap number
        self.lap_strokes.setdefault(self.lap_number, []).append(cycle_time)  # Store stroke time for this lap
        self.lap_cycles[self.lap_number] = self.lap_cycles.get(self.lap_number, 0) + 1  # Add 1 full cycle to the lap count
        print(f"Cycle {self.cycle_counter}: {cycle_time:.2f} seconds, Lap {self.lap_number}")

        self.previous_lap_time = current_time  # Update the previous cycle time

    def half_cycle(self):
        current_time = time.time()
        half_cycle_time = current_time - self.previous_lap_time  # Time since the last cycle
        self.cycles.append(("Half Cycle", half_cycle_time, self.lap_number))  # Append half cycle
        print(f"Half Cycle detected: {half_cycle_time:.2f} seconds, Lap {self.lap_number}")
        self.previous_lap_time = current_time  # Update the previous cycle time

    def record_lap(self):
        current_time = time.time()
        lap_time = current_time - self.lap_start_time  # Calculate the time for the current lap
        self.lap_times.append((self.lap_number, lap_time))  # Store lap time
        print(f"Lap {self.lap_number} completed in {lap_time:.2f} seconds.")
        self.lap_number += 1  # Move to the next lap
        self.lap_start_time = current_time  # Reset lap start time for the next lap

    def detect_turn(self):
        current_time = time.time()
        turn_time = current_time - self.previous_lap_time  # Time since the last event
        self.cycles.append(("Turn", "Turn", self.lap_number))  # Record a turn
        self.previous_lap_time = current_time  # Update the previous cycle time
        self.turn_skip_next_stroke = True  # Skip the next stroke after the turn
        print(f"Turn detected: Lap {self.lap_number}. Next stroke will be recorded (but not counted as a cycle).")

    def stop(self):
        # Add the pop-up prompts for swimmer's last name, swim event, and race date
        root = tk.Tk()
        root.withdraw()  # Hide the main Tkinter window
        self.swimmer_last_name = simpledialog.askstring("Input", "Swimmer Name:", parent=root)
        self.swim_event_name = simpledialog.askstring("Input", "Swim Event Name:", parent=root)
        self.race_date = simpledialog.askstring("Input", "Race Date (YYYY-MM-DD):", parent=root)

        # Validate and parse the race date format
        try:
            race_date_obj = datetime.strptime(self.race_date, '%Y-%m-%d')
            self.formatted_race_date = race_date_obj.strftime('%B %Y')  # Format for filename
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return

        # Reference the globally defined opponent_name
        self.opponent_name = opponent_name  # Use the pre-defined opponent name

        # Update the file paths with user input, including the custom race date
        self.csv_file = f"{file_path}{self.swimmer_last_name}_{self.swim_event_name}_vs_{self.opponent_name}_{self.formatted_race_date}.csv"
        self.pdf_file = f"{file_path}{self.swimmer_last_name}_{self.swim_event_name}_vs_{self.opponent_name}_{self.formatted_race_date}.pdf"

        self.input_splits()  # Ask for splits before generating PDF and CSV

        current_time = time.time()
        total_race_time = sum(self.splits) if self.splits else (current_time - self.start_time)

        last_lap_time = current_time - self.lap_start_time
        self.lap_times.append((self.lap_number, last_lap_time))
        print(f"Lap {self.lap_number} completed in {last_lap_time:.2f} seconds.")
        print(f"Total race time: {total_race_time:.2f} seconds.")

        self.save_to_csv(total_race_time)  # Save data to CSV
        self.generate_pdf()  # Create the PDF report
        self.reset()

    def input_splits(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main Tkinter window

        distance_options = ["50", "100", "200", "400", "500", "1000", "1650"]
        self.distance = simpledialog.askstring("Race Distance", "Enter race distance (50, 100, 200, 400, 500, 1000, 1650):", parent=root)
        
        if self.distance not in distance_options:
            print("Invalid distance entered.")
            return
        
        num_splits = int(self.distance) // 50
        self.splits = []
        for i in range(1, num_splits + 1):
            split = simpledialog.askfloat(f"50 Split {i}", f"Enter split time for {i*50} meters:", parent=root)
            self.splits.append(split)
        print(f"Splits entered: {self.splits}")

    def format_time(self, time_in_seconds):
        minutes, seconds = divmod(time_in_seconds, 60)
        if minutes > 0:
            return f"{int(minutes)}:{seconds:05.2f}"
        return f"{seconds:.2f}"

    def analyze_data(self):
        stroke_rates = [cycle_time for cycle_number, cycle_time, lap_num in self.cycles if isinstance(cycle_number, int)]

        analysis_data = {}
        if stroke_rates:
            avg_stroke_rate = sum(stroke_rates) / len(stroke_rates)
            std_dev = statistics.stdev(stroke_rates) if len(stroke_rates) > 1 else 0

            analysis_data["Whole Race Summary"] = {
                "Average Stroke Rate": avg_stroke_rate,
                "Tempo Trend": std_dev
            }

            analysis_data["Lap Breakdown"] = []
            for lap_num, cycle_count in self.lap_cycles.items():
                lap_strokes = [cycle_time for cycle_number, cycle_time, lap in self.cycles if lap == lap_num and isinstance(cycle_number, int)]
                avg_lap_stroke_rate = sum(lap_strokes) / len(lap_strokes) if lap_strokes else 0
                std_dev_lap = statistics.stdev(lap_strokes) if len(lap_strokes) > 1 else 0

                full_cycles = len([cycle_number for cycle_number, _, lap in self.cycles if lap == lap_num and isinstance(cycle_number, int)])
                half_cycles = len([cycle_number for cycle_number, _, lap in self.cycles if lap == lap_num and cycle_number == "Half Cycle"])
                total_cycles = full_cycles + (half_cycles * 0.5)

                analysis_data["Lap Breakdown"].append({
                    "Lap Number": lap_num,
                    "Number of Cycles": total_cycles,
                    "Average Stroke Rate": avg_lap_stroke_rate,
                    "Tempo Trend": std_dev_lap
                })
        return analysis_data

    def save_to_csv(self, total_race_time=None):
        # Analyze data before saving
        analysis_data = self.analyze_data()

        # Use the last entered split as the total race time if splits are available
        total_race_time = self.splits[-1] if self.splits else (time.time() - self.start_time)

        # Open CSV file with enhanced filename structure
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Metadata Section for quick reference
            writer.writerow(["Swimmer", self.swimmer_last_name])
            writer.writerow(["Event", self.swim_event_name])
            writer.writerow(["Opponent", self.opponent_name])
            writer.writerow(["Race Date", self.race_date])  # Use the user-specified race date
            writer.writerow(["Distance", self.distance])
            writer.writerow([])  # Blank line for separation

            # Main Data Section Headers for clarity
            writer.writerow(["Cycle Number", "Stroke Rate (seconds)", "Lap Number"])
            for cycle_number, cycle_time, lap_num in self.cycles:
                writer.writerow([cycle_number, cycle_time, lap_num])

            writer.writerow([])  # Blank line for clarity

            # Whole Race Summary with corrected Total Race Time
            writer.writerow(["Whole Race Summary"])
            writer.writerow(["Average Stroke Rate", "Tempo Trend", "Breakout Time", "Total Race Time"])
            whole_race_summary = analysis_data.get("Whole Race Summary", {})
            writer.writerow([
                f"{whole_race_summary.get('Average Stroke Rate', 0):.2f}",
                f"{whole_race_summary.get('Tempo Trend', 0):.2f}",
                f"{self.breakout_time:.2f}" if self.breakout_time else "N/A",
                f"{self.format_time(total_race_time)}"
            ])

            writer.writerow([])  # Blank line for clarity

            # Lap Breakdown with correct 50 splits as differences between entered times
            writer.writerow(["Lap Summary"])
            writer.writerow(["Lap Number", "Cycles", "Avg Stroke Rate (seconds)", "Tempo Trend (seconds)", "50 Splits"])

            for i, (lap_number, lap_time) in enumerate(self.lap_times):
                lap_strokes = [cycle_time for cycle_number, cycle_time, lap_num in self.cycles if lap_num == lap_number and isinstance(cycle_number, int)]
                avg_lap_stroke_rate = sum(lap_strokes) / len(lap_strokes) if lap_strokes else 0
                std_dev_lap = statistics.stdev(lap_strokes) if len(lap_strokes) > 1 else 0

                full_cycles = len([cycle_number for cycle_number, _, lap in self.cycles if lap == lap_number and isinstance(cycle_number, int)])
                half_cycles = len([cycle_number for cycle_number, _, lap in self.cycles if lap == lap_number and cycle_number == "Half Cycle"])
                total_cycles = full_cycles + (half_cycles * 0.5)

                # Calculate 50 splits based on consecutive differences
                if i % 2 == 1:  # Only on alternate lap rows (e.g., second and fourth rows)
                    if (i - 1) // 2 < len(self.splits):
                        # Calculate the split as the difference between consecutive times
                        current_split = self.splits[(i - 1) // 2]
                        previous_split = self.splits[(i - 1) // 2 - 1] if (i - 1) // 2 > 0 else 0
                        split = current_split - previous_split
                    else:
                        split = ""
                else:
                    split = ""  # No split on non-alternate rows

                writer.writerow([
                    lap_number,
                    f"{total_cycles:.1f}",
                    f"{avg_lap_stroke_rate:.2f}" if lap_strokes else "N/A",
                    f"{std_dev_lap:.2f}" if len(lap_strokes) > 1 else "N/A",
                    split
                ])



        print(f"Data saved to {self.csv_file}")



    def generate_pdf(self, title=None):
        if not title:
            title = f"{self.swimmer_last_name} {self.swim_event_name} {self.opponent_name}"

        analysis_data = self.analyze_data()

        with PdfPages(self.pdf_file) as pdf:
            # Page 1: Curve of Best Fit for the Entire Race (from the first script)
            plt.figure(figsize=(11.69, 8.27))  # A4 paper size in landscape
            plt.suptitle(title, fontsize=16)

            stroke_rates = [cycle_time for cycle_number, cycle_time, _ in self.cycles if isinstance(cycle_number, int)]
            cycle_numbers = [cycle_number for cycle_number, _, _ in self.cycles if isinstance(cycle_number, int)]

            if stroke_rates and cycle_numbers:
                degree = 2  # Polynomial degree for curve fit
                coefficients = np.polyfit(cycle_numbers, stroke_rates, degree)
                polynomial = np.poly1d(coefficients)

                x_fit = np.linspace(min(cycle_numbers), max(cycle_numbers), 100)
                y_fit = polynomial(x_fit)

                plt.scatter(cycle_numbers, stroke_rates, label='Stroke Rate Data', color='blue')
                plt.plot(x_fit, y_fit, color='red', label=f'Curve of Best Fit')

                plt.title('Stroke Rate vs Cycle Number')
                plt.xlabel('Cycle Number')
                plt.ylabel('Stroke Rate (seconds)')
                plt.legend()

                pdf.savefig()  # Save the first page
                plt.close()

            # Page 2: Multiple Scatter Plots with Line of Best Fit for Each Lap (from the second script)
            num_laps = len(analysis_data.get("Lap Breakdown", []))
            if num_laps > 0:
                cols = 2
                rows = (num_laps + 1) // cols  # Calculate rows for grid layout

                plt.figure(figsize=(11.69, 8.27))  # A4 landscape
                for i, lap in enumerate(analysis_data.get("Lap Breakdown", []), start=1):
                    lap_num = lap["Lap Number"]
                    lap_strokes = [cycle_time for cycle_number, cycle_time, lap in self.cycles if lap == lap_num and isinstance(cycle_number, int)]
                    cycle_numbers = list(range(1, len(lap_strokes) + 1))

                    plt.subplot(rows, cols, i)
                    plt.scatter(cycle_numbers, lap_strokes, label=f'Lap {lap_num} Stroke Rates', color='blue')

                    if len(cycle_numbers) > 1:
                        slope, intercept = np.polyfit(cycle_numbers, lap_strokes, 1)
                        best_fit_line = [slope * x + intercept for x in cycle_numbers]
                        plt.plot(cycle_numbers, best_fit_line, color='red', label='Best Fit Line')

                    plt.title(f'Lap {lap_num} Stroke Rate')
                    plt.xlabel('Cycle Number')
                    plt.ylabel('Stroke Rate (seconds)')
                    plt.grid(False)

                plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout for main title
                plt.suptitle(title, fontsize=16)
                pdf.savefig()  # Save all lap plots to one PDF page
                plt.close()

            # Page 3: Summary Tables (Whole Race Summary and Lap Breakdown)
            plt.figure(figsize=(11.69, 8.27))
            plt.subplot(211)  # 2 rows, 1 column, position 1 (Whole Race Summary)

            plt.title('Whole Race Summary', fontsize=12)
            summary_data = analysis_data.get("Whole Race Summary", {})
            total_time = self.splits[-1] if self.splits else (sum([lap_time for _, lap_time in self.lap_times]))
            breakout_time = f"{self.breakout_time:.2f}" if self.breakout_time else "N/A"

            summary_table = plt.table(
                cellText=[[f"{summary_data.get('Average Stroke Rate', 0):.2f}",
                           f"{summary_data.get('Tempo Trend', 0):.2f}",
                           breakout_time,
                           f"{self.format_time(total_time)}"]],
                colLabels=["Avg Stroke Rate", "Tempo Trend", "Breakout Time", "Total Race Time"],
                cellLoc='center',
                loc='center'
            )
            summary_table.scale(1, 2)
            plt.axis('off')

            plt.subplot(212)
            plt.title('Lap Breakdown', fontsize=12)

            breakdown_data = [[lap["Lap Number"],
                               f"{lap['Number of Cycles']:.1f}",
                               f"{lap['Average Stroke Rate']:.2f}",
                               f"{lap['Tempo Trend']:.2f}",
                               round(self.splits[i // 2] - self.splits[i // 2 - 1], 2) if i % 2 == 1 and i // 2 > 0 and (len(self.splits) * 2 == len(analysis_data.get("Lap Breakdown", []))) else (round(self.splits[0], 2) if i == 1 else "")]
                              for i, lap in enumerate(analysis_data.get("Lap Breakdown", []))]

            breakdown_table = plt.table(
                cellText=breakdown_data,
                colLabels=["Lap Number", "Cycles", "Avg Stroke Rate", "Tempo Trend (St. Dev)", "50 Splits"],
                cellLoc='center',
                loc='center'
            )
            breakdown_table.scale(1, 2)
            plt.axis('off')

            pdf.savefig()  # Save the summary and breakdown tables to the PDF
            plt.close()

        print(f"PDF report saved to {self.pdf_file}")



    def reset(self):
        self.start_time = None
        self.previous_lap_time = None  # Reset previous cycle time
        self.cycles = []
        self.lap_times = []  # Reset lap times
        self.lap_strokes = {}  # Reset stroke times per lap
        self.lap_number = 1  # Reset lap number to 1
        self.turn_count = 0  # Reset turn count
        self.lap_cycles = {}  # Reset lap cycle count
        self.cycle_counter = 0  # Reset the cycle counter
        self.start_recorded = False  # Reset the start recorded flag
        self.first_stroke_time = None  # Reset the first stroke time
        self.skip_next_stroke = False  # Reset the skip flag
        self.splits = []  # Reset the splits
        print("Stopwatch reset.")

# Example usage:
stopwatch = Stopwatch()
stopwatch.start()

while True:
    if keyboard.is_pressed('enter'):  # Record full cycle when Enter is pressed
        stopwatch.cycle()
        time.sleep(0.2)  # To avoid multiple triggers

    if keyboard.is_pressed('shift'):  # Record half cycle when Shift is pressed
        stopwatch.half_cycle()
        time.sleep(0.2)  # To avoid multiple triggers

    if keyboard.is_pressed('space'):  # Detect turn when Spacebar is pressed
        stopwatch.detect_turn()
        stopwatch.record_lap()
        time.sleep(0.2)  # To avoid multiple triggers

    if keyboard.is_pressed('esc'):  # Stop stopwatch when Esc is pressed
        stopwatch.stop()
        break
