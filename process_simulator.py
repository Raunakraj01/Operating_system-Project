import tkinter as tk
from tkinter import ttk
from collections import deque

class Process:
    def __init__(self, pid, burst):
        self.pid = pid
        self.burst = burst
        self.remaining = burst
        self.state = "New"

class Simulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Management Simulator")

        self.processes = []
        self.ready_queue = deque()
        self.current = None
        self.time_quantum = 2
        self.counter = 0
        self.running = False
        self.gantt = []

        self.create_ui()

    def create_ui(self):
        # Title
        tk.Label(self.root, text="Process Management Simulator",
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Input Frame
        frame = tk.LabelFrame(self.root, text="Add Process", padx=10, pady=10)
        frame.pack(pady=5)

        tk.Label(frame, text="PID").grid(row=0, column=0)
        self.pid_entry = tk.Entry(frame)
        self.pid_entry.grid(row=0, column=1)

        tk.Label(frame, text="Burst Time").grid(row=1, column=0)
        self.burst_entry = tk.Entry(frame)
        self.burst_entry.grid(row=1, column=1)

        tk.Button(frame, text="Add Process", command=self.add_process).grid(row=2, columnspan=2, pady=5)

        # Table
        self.tree = ttk.Treeview(self.root, columns=("PID", "Burst", "Remaining", "State"), show="headings")
        for col in ("PID", "Burst", "Remaining", "State"):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        # Colors
        self.tree.tag_configure("Running", background="lightgreen")
        self.tree.tag_configure("Ready", background="lightyellow")
        self.tree.tag_configure("Terminated", background="lightcoral")

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Next Step", command=self.next_step).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Start", command=self.start_auto).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Stop", command=self.stop_auto).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset).grid(row=0, column=3, padx=5)

        # Status
        self.status_label = tk.Label(self.root, text="Status: Idle", font=("Arial", 12))
        self.status_label.pack(pady=5)

        # Gantt Chart Display
        self.gantt_label = tk.Label(self.root, text="Gantt Chart: ", font=("Arial", 10))
        self.gantt_label.pack(pady=5)

    def add_process(self):
        pid = self.pid_entry.get()
        burst = int(self.burst_entry.get())

        p = Process(pid, burst)
        p.state = "Ready"

        self.processes.append(p)
        self.ready_queue.append(p)

        self.update_table()

    def next_step(self):
        if self.current is None and self.ready_queue:
            self.current = self.ready_queue.popleft()
            self.current.state = "Running"
            self.counter = 0

        if self.current:
            self.current.remaining -= 1
            self.counter += 1
            self.gantt.append(self.current.pid)

            if self.current.remaining == 0:
                self.current.state = "Terminated"
                self.current = None
            elif self.counter == self.time_quantum:
                self.current.state = "Ready"
                self.ready_queue.append(self.current)
                self.current = None

        self.update_table()
        self.update_status()

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in self.processes:
            self.tree.insert("", "end",
                             values=(p.pid, p.burst, p.remaining, p.state),
                             tags=(p.state,))

    def update_status(self):
        running = self.current.pid if self.current else "None"
        queue = [p.pid for p in self.ready_queue]

        self.status_label.config(text=f"Running: {running} | Ready Queue: {queue}")
        self.gantt_label.config(text="Gantt Chart: " + " → ".join(self.gantt))

    def start_auto(self):
        self.running = True
        self.run_auto()

    def run_auto(self):
        if self.running:
            self.next_step()
            self.root.after(1000, self.run_auto)

    def stop_auto(self):
        self.running = False

    def reset(self):
        self.processes.clear()
        self.ready_queue.clear()
        self.current = None
        self.gantt.clear()
        self.running = False
        self.update_table()
        self.update_status()

# Run App
root = tk.Tk()
app = Simulator(root)
root.mainloop()