import csv
import matplotlib.pyplot as plt
import os


class Metrics:
    def __init__(self, player_count: int):
        self.player_count = player_count
        self.wins = [0 for _ in range(player_count)]
        self.chips_history = [[] for _ in range(player_count)]

    def record_hand(self, player_index: int, chips: float, win: bool):
        # Record the player's chip total after a hand and whether that hand was a win
        if player_index < 0 or player_index >= self.player_count:
            return
        self.chips_history[player_index].append(chips)
        if win:
            self.wins[player_index] += 1

    def win_percentage(self, player_index: int) -> float:
        plays = len(self.chips_history[player_index])
        if plays == 0:
            return 0.0
        return (self.wins[player_index] / plays) * 100.0

    def save_csv(self, filename: str = "metrics_chips.csv"):
        # Save per-hand chips history as columns per player
        max_len = max((len(h) for h in self.chips_history), default=0)
        header = [f"player_{i}_chips" for i in range(self.player_count)]
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for i in range(max_len):
                row = []
                for p in range(self.player_count):
                    if i < len(self.chips_history[p]):
                        row.append(self.chips_history[p][i])
                    else:
                        row.append("")
                writer.writerow(row)

    def save_summary(self, filename: str = "metrics_summary.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["player", "hands_played", "wins", "win_pct"])
            for i in range(self.player_count):
                hands = len(self.chips_history[i])
                wins = self.wins[i]
                pct = self.win_percentage(i)
                writer.writerow([f"player_{i}", hands, wins, f"{pct:.2f}"])

    def print_summary(self):
        for i in range(self.player_count):
            hands = len(self.chips_history[i])
            wins = self.wins[i]
            pct = self.win_percentage(i)
            print(f"Player {i}: hands={hands}, wins={wins}, win_pct={pct:.2f}%")

    def plot_chips(self, output: str = "metrics_chips.png", show: bool = False):
        """Plot chip totals over hands for each player using matplotlib.

        Saves the figure to `output`. If `show` is True, calls `plt.show()`.
        """
        plt.figure(figsize=(10, 6))
        for i, history in enumerate(self.chips_history):
            if not history:
                continue
            x = list(range(1, len(history) + 1))
            plt.plot(x, history, marker='o', label=f"Player {i}")

        plt.xlabel("Hand Number")
        plt.ylabel("Chips")
        plt.title("Player chips over time")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        # Ensure output dir exists
        out_dir = os.path.dirname(output)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        plt.savefig(output)
        if show:
            plt.show()
        plt.close()
