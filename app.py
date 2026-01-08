import streamlit as st

# --- Core Logic ---
def analyze_dna(raw_data):
    lines = raw_data.splitlines()
    dna_lines = [line for line in lines if not line.strip().startswith(">")]
    clean_dna = "".join(dna_lines).replace(" ", "").upper()

    if not clean_dna:
        return None, "No valid DNA sequence found."
    if not all(base in "ATGC" for base in clean_dna):
        return None, "Sequence contains non-DNA characters."



    g_count = clean_dna.count('G')
    c_count = clean_dna.count('C')
    gc_percent = ((g_count + c_count) / len(clean_dna)) * 100
    
    return {
        "length": len(clean_dna),
        "gc_count": g_count + c_count,
        "gc_percent": gc_percent,
        "sequence": clean_dna
    }

# --- Streamlit UI ---
st.set_page_config(page_title="DNA GC Analyzer", page_icon="🧬")

st.title("🧬 Advanced DNA GC Analyzer")
st.markdown("Paste your sequence below or upload a FASTA file to calculate GC content.")

# File Uploader
uploaded_file = st.file_uploader("Upload a FASTA file", type=["fasta", "fa", "txt"])
input_text = ""

if uploaded_file is not None:
    input_text = uploaded_file.read().decode("utf-8")
else:
    input_text = st.text_area("Paste DNA Sequence here:", height=200)

if st.button("Analyze Sequence"):
    if input_text:
        data, error = None, None
        try:
            results = analyze_dna(input_text)
            if isinstance(results, dict):
                # Display Results in nice metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Length", results["length"])
                col2.metric("G+C Bases", results["gc_count"])
                col3.metric("GC Percentage", f"{results['gc_percent']:.2f}%")
                
                # Show a progress bar for visual impact
                st.progress(results["gc_percent"] / 100)
                
                # Download button
                report = f"GC Analysis Report\nLength: {results['length']}\nGC%: {results['gc_percent']:.2f}%"
                st.download_button("💾 Download Report", report, file_name="gc_report.txt")
            else:
                st.error(results)
        except Exception as e:
            st.error(f"Error processing sequence: {e}")
    else:
        st.warning("Please enter a sequence first.")
        