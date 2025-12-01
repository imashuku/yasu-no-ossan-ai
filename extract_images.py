import os
import fitz  # PyMuPDF

# 対象PDFディレクトリ
pdf_dir = "../野洲のおっさん2026"
output_dir = "extracted_images"

# 出力ディレクトリ作成
os.makedirs(output_dir, exist_ok=True)

# PDFファイルを取得
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

image_count = 0

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    print(f"Processing: {pdf_file}")
    
    try:
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images(full=True)
            
            for img_index, img in enumerate(images):
                xref = img[0]
                
                try:
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # ファイル名を作成
                    image_filename = f"{pdf_file.replace('.pdf', '')}_page{page_num+1}_img{img_index+1}.{image_ext}"
                    image_path = os.path.join(output_dir, image_filename)
                    
                    # 保存
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    image_count += 1
                    print(f"  ✅ Saved: {image_filename}")
                    
                except Exception as e:
                    print(f"  ⚠️ Could not extract image: {e}")
        
        doc.close()
        
    except Exception as e:
        print(f"  ❌ Error processing {pdf_file}: {e}")

print(f"\n🎉 完了！ {image_count} 枚の画像を {output_dir}/ に保存しました。")

