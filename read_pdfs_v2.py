import os
from pdfminer.high_level import extract_text

# 対象ディレクトリ
target_dir = "../野洲のおっさん2026"
output_file = "pdf_contents_v2.txt"

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
            # pdfminerを使ってテキスト抽出
            text = extract_text(pdf_path)
            
            if text:
                out_f.write(text)
            else:
                out_f.write("(No text extracted)")
            out_f.write("\n\n")
                
        except Exception as e:
            out_f.write(f"Error reading file: {e}\n")

print(f"Done! Contents saved to {output_file}")

