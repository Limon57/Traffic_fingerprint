import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parents[3]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import tkinter as tk
from tkinter import filedialog, messagebox

from PCAP_Traffic.src.model.predict import predict_website

BG         = "#0f1117"
CARD       = "#1a1d27"
ACCENT     = "#4f8ef7"
ACCENT_HOV = "#6ba3ff"
BTN_BG     = "#252836"
BTN_HOV    = "#2e3246"
TEXT       = "#e8eaf6"
MUTED      = "#7b82a0"
SUCCESS    = "#4caf89"
BAR_TRACK  = "#252836"


class PcapPredictorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PCAP Website Predictor")
        self.root.geometry("760x570")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.selected_file: str = ""
        self._build_ui()


    def _build_ui(self) -> None:

        header = tk.Frame(self.root, bg=CARD, pady=20)
        header.pack(fill="x")

        tk.Label(
            header,
            text="PCAP Website Predictor",
            font=("Segoe UI", 20, "bold"),
            bg=CARD, fg=TEXT,
        ).pack()
        tk.Label(
            header,
            text="Select a capture file and classify the website traffic",
            font=("Segoe UI", 9),
            bg=CARD, fg=MUTED,
        ).pack(pady=(4, 0))


        tk.Frame(self.root, height=2, bg=ACCENT).pack(fill="x")


        body = tk.Frame(self.root, bg=BG, padx=30, pady=22)
        body.pack(fill="both", expand=True)


        file_card = tk.Frame(body, bg=CARD, padx=16, pady=14)
        file_card.pack(fill="x", pady=(0, 16))

        tk.Label(
            file_card,
            text="CAPTURE FILE",
            font=("Segoe UI", 7, "bold"),
            bg=CARD, fg=MUTED,
        ).pack(anchor="w")

        file_row = tk.Frame(file_card, bg=CARD)
        file_row.pack(fill="x", pady=(6, 0))

        self.file_label = tk.Label(
            file_row,
            text="No file selected…",
            font=("Segoe UI", 10),
            bg="#11141f", fg=MUTED,
            anchor="w", padx=12, pady=8,
            relief="flat",
        )
        self.file_label.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self._make_btn(file_row, "Browse", self.browse_file, width=10).pack(side="right")


        self._make_btn(
            body, "Predict Website", self.run_prediction,
            width=22, accent=True,
        ).pack(pady=(0, 20))


        result_card = tk.Frame(body, bg=CARD, padx=16, pady=14)
        result_card.pack(fill="both", expand=True)

        tk.Label(
            result_card,
            text="RESULT",
            font=("Segoe UI", 7, "bold"),
            bg=CARD, fg=MUTED,
        ).pack(anchor="w")

        self.result_label = tk.Label(
            result_card,
            text="—",
            font=("Segoe UI", 18, "bold"),
            bg=CARD, fg=TEXT, pady=4,
        )
        self.result_label.pack(anchor="w")

        tk.Label(
            result_card,
            text="CONFIDENCE BREAKDOWN",
            font=("Segoe UI", 7, "bold"),
            bg=CARD, fg=MUTED,
        ).pack(anchor="w", pady=(12, 6))


        scroll_outer = tk.Frame(result_card, bg=CARD)
        scroll_outer.pack(fill="both", expand=True)

        self._canvas = tk.Canvas(
            scroll_outer, bg=CARD, highlightthickness=0, bd=0
        )
        scrollbar = tk.Scrollbar(
            scroll_outer, orient="vertical",
            command=self._canvas.yview,
            bg=BTN_BG, troughcolor=BAR_TRACK,
            activebackground=ACCENT, relief="flat", bd=0,
        )
        self._canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self.bars_frame = tk.Frame(self._canvas, bg=CARD)
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self.bars_frame, anchor="nw"
        )


        self.bars_frame.bind(
            "<Configure>",
            lambda _e: self._canvas.configure(
                scrollregion=self._canvas.bbox("all")
            ),
        )
        self._canvas.bind(
            "<Configure>",
            lambda e: self._canvas.itemconfig(self._canvas_window, width=e.width),
        )

        self._canvas.bind_all("<MouseWheel>",
            lambda e: self._canvas.yview_scroll(-1 * (e.delta // 120), "units")
        )



    def _make_btn(self, parent, text, command, width=12, accent=False):

        normal = ACCENT   if accent else BTN_BG
        hover  = ACCENT_HOV if accent else BTN_HOV

        btn = tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=normal, fg="#ffffff",
            padx=16, pady=8,
            cursor="hand2",
            width=width,
            relief="flat",
        )
        btn.bind("<Button-1>", lambda _e: command())
        btn.bind("<Enter>",    lambda _e: btn.config(bg=hover))
        btn.bind("<Leave>",    lambda _e: btn.config(bg=normal))
        return btn

    def _add_bar(self, label: str, prob: float) -> None:

        BAR_W = 370

        row = tk.Frame(self.bars_frame, bg=CARD)
        row.pack(fill="x", pady=4)

        tk.Label(
            row,
            text=label,
            font=("Segoe UI", 9),
            bg=CARD, fg=TEXT,
            width=13, anchor="w",
        ).pack(side="left")

        track = tk.Frame(row, bg=BAR_TRACK, height=12, width=BAR_W)
        track.pack(side="left", padx=(8, 10))
        track.pack_propagate(False)

        fill_w = max(int(BAR_W * prob), 2)
        tk.Frame(track, bg=ACCENT, width=fill_w).place(x=0, y=0, relheight=1)

        tk.Label(
            row,
            text=f"{prob:.1%}",
            font=("Segoe UI", 9, "bold"),
            bg=CARD, fg=MUTED,
            width=6, anchor="e",
        ).pack(side="left")



    def browse_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select a PCAP file",
            filetypes=[("PCAP files", "*.pcap"), ("All files", "*.*")],
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=Path(file_path).name, fg=TEXT)

    def run_prediction(self) -> None:
        if not self.selected_file:
            messagebox.showwarning("No File", "Please select a PCAP file first.")
            return

        result = predict_website(self.selected_file)

        if not result["success"]:
            messagebox.showerror("Prediction Error", result["error"])
            return

        self.result_label.config(text=result["prediction"], fg=SUCCESS)


        for widget in self.bars_frame.winfo_children():
            widget.destroy()

        sorted_scores = sorted(
            result["confidence_scores"].items(),
            key=lambda item: item[1],
            reverse=True,
        )
        for cls, prob in sorted_scores:
            self._add_bar(cls, prob)


def main() -> None:
    root = tk.Tk()
    PcapPredictorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

