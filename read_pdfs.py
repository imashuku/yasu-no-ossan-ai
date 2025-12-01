import os
from pypdf import PdfReader

# 対象ディレクトリ
target_dir = "../野洲のおっさん2026"
output_file = "pdf_contents.txt"

# ディレクトリ内のPDFファイルを取得
pdf_files = [f for f in os.listdir(target_dir) if f.endswith('.pdf')]
pdf_files.sort()

with open(output_file, 'w', encoding='utf-8') as out_f:
    for pdf_file in pdf_files:
        pdf_path = os.path.join(target_dir, pdf_file)
        print(f"Reading: {pdf_file}...")
        
        out_f.write(f"\n{'='*50}\n")
        out_f.write(f"FILE: {pdf_file}\n")
        out_f.write(f"{'='*50}\n\n")
        
        try:
            reader = PdfReader(pdf_path)
            number_of_pages = len(reader.pages)
            
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                out_f.write(f"--- Page {i+1}/{number_of_pages} ---\n")
                if text:
                    out_f.write(text)
                else:
                    out_f.write("(No text found on this page)")
                out_f.write("\n\n")
                
        except Exception as e:
            out_f.write(f"Error reading file: {e}\n")

print(f"Done! Contents saved to {output_file}")

