import math
import tkinter as tk
from tkinter import messagebox

# ----------------- COLORS & FONTS -----------------
BG_MAIN = "#f4f5f7"
CARD_BG = "#ffffff"
PRIMARY = "#0078D4"        #  Blue
PRIMARY_DARK = "#005a9e"
DANGER = "#d83b01"
TEXT_MAIN = "#222222"
TEXT_MUTED = "#666666"
TEXT_GREEN = "#107C10"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SECTION_TITLE = ("Segoe UI", 15, "bold")
FONT_INPUT = ("Segoe UI", 15)
FONT_BUTTON = ("Segoe UI", 15, "bold")
FONT_RESULT = ("Segoe UI", 15)
FONT_WARNING = ("Segoe UI", 16, "italic")
FONT_FOOTER = ("Segoe UI", 12, "italic")


# ----------------- BUTTON HOVER -----------------
def on_enter_button(event, hover_color):
    event.widget["bg"] = hover_color


def on_leave_button(event, normal_color):
    event.widget["bg"] = normal_color


# ----------------- CLEAR OUTPUTS -----------------
def clear_outputs():
    value_total_area.config(text="-")
    value_03m_locators.config(text="-", fg=TEXT_MAIN)
    value_3m_locators.config(text="-", fg=TEXT_MAIN)
    warning_label.config(text="", fg=DANGER)


# ----------------- RESET ALL -----------------
def reset_all():
    entry_L.delete(0, tk.END)
    entry_W.delete(0, tk.END)
    entry_locator_height.delete(0, tk.END)
    entry_tag_height.delete(0, tk.END)
    clear_outputs()


# ----------------- MAIN CALCULATION LOGIC -----------------
def calculate():
    try:
        L = float(entry_L.get())
        W = float(entry_W.get())
        locator_height = float(entry_locator_height.get())
        tag_height = float(entry_tag_height.get())

        warning_label.config(text="", fg=DANGER)

        # Rule 1 – Max locator height
        if locator_height > 10:
            messagebox.showwarning("HEIGHT WARNING", "Max installation height is 10 meters.")
            clear_outputs()
            return

        # Rule 2 – Locator must be above tag
        if locator_height <= tag_height:
            messagebox.showerror("INVALID HEIGHT", "Locator height must be greater than tag height.")
            clear_outputs()
            return

        # Base geometry
        H = locator_height - tag_height
        total_area = L * W
        single_locator_coverage = 3.14 * H * H  # π·H²

        value_total_area.config(text=f"{total_area:.2f} m²")

        # Rule 3 – Hard limit: Tag too high
        if tag_height > 0.67 * locator_height:
            value_03m_locators.config(text="N/A", fg=DANGER)
            value_3m_locators.config(text="N/A", fg=DANGER)
            warning_label.config(
                text="The number of locators cannot be calculated at this tag height.",
                fg=DANGER
            )
            return

        if single_locator_coverage <= 0:
            value_03m_locators.config(text="N/A", fg=DANGER)
            value_3m_locators.config(text="N/A", fg=DANGER)
            warning_label.config(text="Invalid coverage geometry.", fg=DANGER)
            return

        # Normal calculated locators (estimated)
        est_raw = total_area / single_locator_coverage
        est_03m = math.ceil(est_raw)      # New: 0.3 m accuracy locators
        est_3m = math.ceil(est_03m / 2)   # 3 m accuracy locators

        # Rule 4 – Minimum 2 locators
        min_warning = False
        if est_03m <= 2 or est_3m <= 2:
            est_03m = max(2, est_03m)
            est_3m = max(2, est_3m)
            min_warning = True

        # Apply UI updates
        value_03m_locators.config(
            text=str(est_03m),
            fg=DANGER if est_03m <= 2 else TEXT_GREEN
        )
        value_3m_locators.config(
            text=str(est_3m),
            fg=DANGER if est_3m <= 2 else TEXT_MAIN
        )

        # Rule 5 – Reliability warning (soft)
        warnings = []
        if tag_height > 0.52 * locator_height:
            warnings.append("Calculator may not provide reliable results at this tag height.")
        if min_warning:
            warnings.append("Minimum number of locators = 2")

        warning_label.config(text="  ".join(warnings), fg=DANGER if warnings else TEXT_MAIN)

    except ValueError:
        messagebox.showerror("INPUT ERROR", "Please enter valid numeric values.")
        clear_outputs()


# ----------------- BUILD MAIN UI -----------------
def build_main_ui(root):
    global entry_L, entry_W, entry_locator_height, entry_tag_height
    global value_total_area, value_03m_locators, value_3m_locators, warning_label

    root.title("RTLS Locators Calculator")
    root.geometry("560x520")
    root.configure(bg=BG_MAIN)

    container = tk.Frame(root, bg=BG_MAIN)
    container.pack(fill="both", expand=True, padx=20, pady=20)

    # Title: Calculator
    title_frame = tk.Frame(container, bg=BG_MAIN)
    title_frame.pack()

    tk.Label(
        title_frame, text="",
        font=("Segoe UI", 18, "bold"), fg=PRIMARY, bg=BG_MAIN
    ).pack(side="left")

    tk.Label(
        title_frame, text=" RTLS Locators Calculator",
        font=("Segoe UI", 18, "bold"), fg=TEXT_MAIN, bg=BG_MAIN
    ).pack(side="left")

    tk.Label(
        container,
        text="Estimate required RTLS locators based on room size and heights",
        font=("Segoe UI", 12), fg=TEXT_MUTED, bg=BG_MAIN
    ).pack(pady=(0, 15))

    # ---------- INPUT PANEL ----------
    input_card = tk.Frame(container, bg=CARD_BG)
    input_card.pack(fill="x")

    tk.Label(
        input_card, text="Inputs",
        font=FONT_SECTION_TITLE, fg=TEXT_MAIN, bg=CARD_BG
    ).pack(anchor="w", padx=15, pady=(10, 5))

    def add_input_row(text):
        row = tk.Frame(input_card, bg=CARD_BG)
        row.pack(fill="x", padx=15, pady=5)

        tk.Label(row, text=text, font=FONT_INPUT, fg=TEXT_MAIN, bg=CARD_BG).pack(side="left")
        entry = tk.Entry(row, width=10, font=FONT_INPUT, relief="flat")
        entry.configure(highlightbackground="#cccccc", highlightcolor=PRIMARY, highlightthickness=1)
        entry.pack(side="right")
        return entry

    entry_L = add_input_row("Room Length L (m):")
    entry_W = add_input_row("Room Width W (m):")
    entry_locator_height = add_input_row("Locator Height (m):")
    entry_tag_height = add_input_row("Tag Height (m):")

    # ---------- BUTTONS ----------
    btn_row = tk.Frame(container, bg=BG_MAIN)
    btn_row.pack(fill="x", pady=15)

    calc_btn = tk.Button(
        btn_row, text="Calculate", command=calculate,
        font=FONT_BUTTON, bg=PRIMARY, fg="white",
        relief="flat", padx=20, pady=5
    )
    calc_btn.pack(side="left", padx=(0, 10))
    calc_btn.bind("<Enter>", lambda e: on_enter_button(e, PRIMARY_DARK))
    calc_btn.bind("<Leave>", lambda e: on_leave_button(e, PRIMARY))

    reset_btn = tk.Button(
        btn_row, text="Reset", command=reset_all,
        font=FONT_BUTTON, bg="#cccccc", fg=TEXT_MAIN,
        relief="flat", padx=20, pady=5
    )
    reset_btn.pack(side="left")

    # ---------- RESULTS ----------
    results_card = tk.Frame(container, bg=CARD_BG)
    results_card.pack(fill="x", pady=10)

    tk.Label(
        results_card, text="Results",
        font=FONT_SECTION_TITLE, fg=TEXT_MAIN, bg=CARD_BG
    ).pack(anchor="w", padx=15, pady=(10, 5))

    def add_output_row(title):
        row = tk.Frame(results_card, bg=CARD_BG)
        row.pack(fill="x", padx=15, pady=5)
        tk.Label(row, text=title, font=FONT_RESULT, fg=TEXT_MAIN, bg=CARD_BG).pack(side="left")
        value = tk.Label(row, text="-", font=FONT_RESULT, fg=TEXT_MAIN, bg=CARD_BG)
        value.pack(side="right")
        return value

    value_total_area = add_output_row("Total Room Area (L × W):")
    value_03m_locators = add_output_row("0.3 meters Accuracy Locators (ceil):")
    value_3m_locators = add_output_row("3 meters Accuracy Locators (ceil):")

    warning_label = tk.Label(
        container, text="", font=FONT_WARNING,
        fg=DANGER, bg=BG_MAIN, wraplength=520, justify="center"
    )
    warning_label.pack(pady=5)

    # Footer
    tk.Label(
        container, text="RTLS Tools",
        font=FONT_FOOTER, fg=PRIMARY, bg=BG_MAIN
    ).pack(side="bottom", pady=(20, 0))

    clear_outputs()


# ----------------- SPLASH SCREEN -----------------
def show_splash_then_main():
    splash = tk.Toplevel()
    splash.overrideredirect(True)

    w, h = 360, 200
    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()
    x = (sw // 2) - (w // 2)
    y = (sh // 2) - (h // 2)

    splash.geometry(f"{w}x{h}+{x}+{y}")
    splash.configure(bg=BG_MAIN)

    tk.Label(
        splash, text="",
        font=("Segoe UI", 26, "bold"), fg=PRIMARY, bg=BG_MAIN
    ).pack(pady=(40, 0))

    tk.Label(
        splash, text="RTLS Locators Calculator",
        font=("Segoe UI", 14), fg=TEXT_MUTED, bg=BG_MAIN
    ).pack()

    tk.Label(
        splash, text="Loading...",
        font=("Segoe UI", 10, "italic"), fg=TEXT_MUTED, bg=BG_MAIN
    ).pack(pady=15)

    def start():
        splash.destroy()
        root.deiconify()
        build_main_ui(root)

    root.withdraw()
    root.after(2000, start)


# ----------------- APP ENTRY -----------------
root = tk.Tk()
show_splash_then_main()
root.mainloop()
