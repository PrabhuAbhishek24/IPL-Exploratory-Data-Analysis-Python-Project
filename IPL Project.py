import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

class IPL_Data_Analytics_App:
    def __init__(self, root):
        self.root = root
        self.root.title("IPL Data Analytics App")
        self.load_background_image()
        self.create_widgets()

    def load_background_image(self):
        bg_image = Image.open("C:\\Users\\Office PC\\AppData\\Local\\Programs\\Python\\Python312\\ipl_bg.jpg")
        bg_photo = ImageTk.PhotoImage(bg_image)
        self.background_label = tk.Label(self.root, image=bg_photo)
        self.background_label.image = bg_photo
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Load CSV File button
        self.load_button = tk.Button(main_frame, text="Load CSV File", command=self.load_file, width=30, height=2)
        self.load_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Label for dropdown menu
        self.select_team_label = tk.Label(main_frame, text="Select a team:")
        self.select_team_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        # Dropdown menu for team selection
        self.team_var = tk.StringVar()
        self.team_dropdown = ttk.Combobox(main_frame, textvariable=self.team_var, state="readonly")
        self.team_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        # Button to show team statistics
        self.show_stats_button = tk.Button(main_frame, text="Show Statistics", command=self.show_team_stats, width=30, height=2)
        self.show_stats_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        # Button to show total runs scored by team
        self.total_runs_button = tk.Button(main_frame, text="Total Runs Scored by Team", command=self.show_total_runs, width=30, height=2)
        self.total_runs_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        # Button to show highest score in both innings by team
        self.highest_score_button = tk.Button(main_frame, text="Highest Score in Both Innings", command=self.show_highest_scores, width=30, height=2)
        self.highest_score_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
        # Button to show highest man of the match awards by team
        self.mom_awards_button = tk.Button(main_frame, text="Highest Man of the Match Awards", command=self.show_mom_awards, width=30, height=2)
        self.mom_awards_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Button to show average first innings score by team
        self.avg_first_innings_button = tk.Button(main_frame, text="Average First Innings Score", command=self.show_avg_first_innings, width=30, height=2)
        self.avg_first_innings_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        
        # Button to show average second innings score by team
        self.avg_second_innings_button = tk.Button(main_frame, text="Average Second Innings Score", command=self.show_avg_second_innings, width=30, height=2)
        self.avg_second_innings_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # Button to show matches played at each venue
        self.venue_button = tk.Button(main_frame, text="Matches Played at Each Venue", command=self.show_venue_chart, width=30, height=2)
        self.venue_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Button to show the pie chart of overall performance of the teams
        self.team_win_percentage_pie_chart_button = tk.Button(main_frame, text="Team Win Percentage Pie Chart", command=self.team_win_percentage_pie_chart, width=30, height=2)
        self.team_win_percentage_pie_chart_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        # Button to show highest score in each match
        self.high_score_button = tk.Button(main_frame, text="Highest Score in Each Match", command=self.calculate_highest_score_each_match, width=30, height=2)
        self.high_score_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        # Label to display selected team info
        self.team_info_label = tk.Label(main_frame, text="", justify=tk.LEFT)
        self.team_info_label.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select IPL Data CSV File", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.update_teams()

    def update_teams(self):
        teams = pd.unique(self.data[['team1', 'team2']].values.ravel('K'))
        self.team_dropdown['values'] = list(teams)

    def show_team_stats(self):
        selected_team = self.team_var.get()
        if selected_team:
            team_wins = len(self.data[self.data['match_winner'] == selected_team])
            team_losses = len(self.data[(self.data['team1'] == selected_team) | (self.data['team2'] == selected_team)]) - team_wins
            total_matches = team_wins + team_losses
            win_percentage = (team_wins / total_matches) * 100 if total_matches > 0 else 0
            
            messagebox.showinfo("Team Stats",
                                f"{selected_team} Statistics:\n\n"
                                f"Number of Wins: {team_wins}\n"
                                f"Number of Losses: {team_losses}\n"
                                f"Win Percentage: {win_percentage:.2f}%")
        else:
            messagebox.showwarning("Select Team", "Please select a team from the dropdown.")

    def show_total_runs(self):
        selected_team = self.team_var.get()
        if selected_team:
            team_runs = self.data[(self.data['team1'] == selected_team)]['first_ings_score'].sum() + \
                        self.data[(self.data['team2'] == selected_team)]['second_ings_score'].sum()
            
            messagebox.showinfo("Total Runs",
                                f"{selected_team} has scored a total of {team_runs} runs.")
        else:
            messagebox.showwarning("Select Team", "Please select a team from the dropdown.")

    def show_highest_scores(self):
        selected_team = self.team_var.get()
        if selected_team:
            highest_first_ings_score = self.data[self.data['team1'] == selected_team]['first_ings_score'].max()
            highest_second_ings_score = self.data[self.data['team2'] == selected_team]['second_ings_score'].max()
            
            messagebox.showinfo("Highest Scores",
                                f"Highest Scores for {selected_team}:\n\n"
                                f"Highest First Innings Score: {highest_first_ings_score}\n"
                                f"Highest Second Innings Score: {highest_second_ings_score}")
        else:
            messagebox.showwarning("Select Team", "Please select a team from the dropdown.")

    def show_mom_awards(self):
        selected_team = self.team_var.get()
        if selected_team:
            team_mom_data = self.data[(self.data['team1'] == selected_team) | (self.data['team2'] == selected_team) & (self.data['match_winner']==selected_team)]
            mom_awards_count = team_mom_data['player_of_the_match'].value_counts()
            if not mom_awards_count.empty:
                max_awards_player = mom_awards_count.idxmax()
                max_awards_count = mom_awards_count.max()
                
                messagebox.showinfo("Man of the Match Awards",
                                    f"Most Man of the Match Awards for {selected_team}:\n\n"
                                    f"Player: {max_awards_player}\n"
                                    f"Awards: {max_awards_count}")
            else:
                messagebox.showinfo("Man of the Match Awards",
                                    f"No Man of the Match awards data available for {selected_team}.")
        else:
            messagebox.showwarning("Select Team", "Please select a team from the dropdown.")

    def show_avg_first_innings(self):
        selected_team = self.team_var.get()
        if selected_team:
            first_ings_scores = self.data[self.data['team1'] == selected_team]['first_ings_score']
            avg_first_ings_score = first_ings_scores.mean()
            messagebox.showinfo("Average First Innings Score",
                                f"Average First Innings Score for {selected_team}: {avg_first_ings_score:.2f}")
        else:
            messagebox.showwarning("Select Team", "Please select a team from the dropdown.")

    def show_avg_second_innings(self):
        selected_team = self.team_var.get()
        if selected_team:
            second_ings_scores = self.data[self.data['team2'] == selected_team]['second_ings_score']
            avg_second_ings_score = second_ings_scores.mean()
            messagebox.showinfo("Average Second Innings Score",
                                f"Average Second Innings Score for {selected_team}: {avg_second_ings_score:.2f}")
        else:
            messagebox.showwarning("Select Team", "Please select a team from the dropdown.")

    def show_venue_chart(self):
        selected_team = self.team_var.get()
        if selected_team:
            team_data = self.data[(self.data['team1'] == selected_team) | (self.data['team2'] == selected_team)]
            venue_counts = team_data['venue'].value_counts()
            venues = venue_counts.index.tolist()
            counts = venue_counts.values.tolist()

            plt.figure(figsize=(10, 6))
            plt.barh(venues, counts, color='skyblue')
            plt.xlabel('Number of Matches')
            plt.ylabel('Venue')
            plt.title(f'Matches Played at Each Venue by {selected_team}')
            plt.gca().invert_yaxis()  # Invert y-axis to show the highest count on top
            plt.show()
        else:
            messagebox.showwarning("Select Team", "Please select a team from the dropdown.")

    def team_win_percentage_pie_chart(self):
        if hasattr(self, 'data'):
            team_win_percentage = self.data['match_winner'].value_counts(normalize=True) * 100
            labels = team_win_percentage.index
            sizes = team_win_percentage.values
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title('Team Win Percentage')
            plt.show()
        else:
            messagebox.showwarning("No Data", "No Data Available. Please load the IPL Data CSV file first.")

    def calculate_highest_score_each_match(self):
        if hasattr(self, 'data'):
            ipl = self.data.groupby('match_id')[['first_ings_score', 'second_ings_score']].max()
            ipl['highscore'] = ipl[['first_ings_score', 'second_ings_score']].max(axis=1)
            plt.figure(figsize=(10, 6))
            plt.scatter(ipl.index, ipl['highscore'], color='green')
            plt.title('Highest Score in Each Match')
            plt.xlabel('Match Number')
            plt.ylabel('Highest Score')
            plt.grid(True)
            plt.show()
        else:
            messagebox.showwarning("No Data", "No Data Available. Please load the IPL Data CSV file first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = IPL_Data_Analytics_App(root)
    root.mainloop()
