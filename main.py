import tkinter as tk
from tkinter import messagebox, filedialog

def analyze_logic(raw_data):
    """Core logic to process DNA and return results."""
    # Split lines and ignore the FASTA header (starts with >)
    lines = raw_data.splitlines()
    dna_lines = [line for line in lines if not line.strip().startswith(">")]
    clean_dna = "".join(dna_lines).replace(" ", "").upper()

    if not clean_dna:
        return None, "No valid DNA sequence found."

    if not all(base in "ATGC" for base in clean_dna):
        return None, "Sequence contains non-DNA characters."

    g_count = clean_dna.count('G')
    c_count = clean_dna.count('C')
    total_gc = g_count + c_count
    total_len = len(clean_dna)
    gc_percent = (total_gc / total_len) * 100

    results = (
        f"Sequence Length: {total_len}\n"
        f"Total G+C Bases: {total_gc}\n"
        f"GC Percentage: {gc_percent:.2f}%"
    )
    return clean_dna, results

def run_analysis():
    raw_input = dna_text.get("1.0", tk.END)
    dna, report = analyze_logic(raw_input)
    
    if dna is None:
        messagebox.showerror("Error", report)
    else:
        result_label.config(text=report)
        global current_save_data
        current_save_data = f"Analysis Report:\n{report}\n\nFull Sequence:\n{dna}"

def load_fasta():
    file_path = filedialog.askopenfilename(
        filetypes=[("FASTA files", "*.fasta *.fa"), ("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            dna_text.delete("1.0", tk.END)
            dna_text.insert("1.0", content)
        run_analysis() # Automatically analyze after loading

def save_results():
    if 'current_save_data' not in globals():
        messagebox.showwarning("No Data", "Analyze something first!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as file:
            file.write(current_save_data)
        messagebox.showinfo("Saved", "Analysis saved successfully!")

# --- UI Setup ---
root = tk.Tk()
root.title("Advanced DNA GC Analyzer")
root.geometry("600x650")
root.configure(bg="#f4f7f6")

# Header and Text Area
tk.Label(root, text="Add your DNA sequence or Load FASTA:", font=("Arial", 12, "bold"), bg="#f4f7f6").pack(pady=15)
dna_text = tk.Text(root, width=65, height=15, font=("Courier", 10), relief="solid", borderwidth=1)
dna_text.pack(padx=20)

# Buttons Container
btn_frame = tk.Frame(root, bg="#f4f7f6")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="📁 Load FASTA", command=load_fasta, width=12).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="🧬 Analyze", command=run_analysis, bg="#4CAF50", fg="black", width=12, font=("Arial", 9, "bold")).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="🗑️ Clear", command=lambda: [dna_text.delete("1.0", tk.END), result_label.config(text="")], width=12).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="💾 Save", command=save_results, width=12).grid(row=0, column=3, padx=5)

# Result Output
result_label = tk.Label(root, text="", font=("Arial", 11, "bold"), bg="#f4f7f6", justify="left")
result_label.pack(pady=10)

root.mainloop()