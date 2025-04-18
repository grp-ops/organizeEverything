# A GRP UTILITY
# Convert contents of a PDF to markdown format for Obsidian / Notion.
# Prints very sick skull while converting the file.

import threading
import time
import PyPDF2
import argparse

def draw_ascii_art(stop_event):
    ascii_art = r'''
                                              ++++++++                                              
                                         ++++++++++++++++++                                         
                                     ++++++++++++++++++++++++++                                     
                                   ++++++++++++++++++++++++++++++                                   
                                 ++++++++++++++++++++++++++++++++++                                 
                               ++++++++++++++++++++++++++++++++++++++                               
                              ++++++++++++++++++++++++++++++++++++++++                              
                              ++++++++++++++++++++++++++++++++++++++++                              
                             ++++++++++++++++++++++++++++++++++++++++++                             
                             ++++++++++++++++++++++++++++++++++++++++++                             
                             ++++++++++++++++++++++++++++++++++++++++++                             
                             +++    ++++++++++++++++++++++++++++    +++                             
                             ++++       ++++++++++++++++++++       ++++                             
                              +++          ++++++++++++++          +++                              
                              ++++             ++++++             ++++                              
                              ++++++++++     ++++++++++     ++++++++++                              
                              ++++++++++++++++++++++++++++++++++++++++                              
                             +++++++++++++++++++ ++ +++++++++++++++++++                             
                              +++++++++++++++++  ++  +++++++++++++++++                              
                               ++++++++++++++++ ++++ ++++++++++++++++                               
                                      ++++++++++++++++++++++++                                      
                                      ++++++++++++++++++++++++                                      
                                       ++++++++++++++++++++++                                       
                                       +++++ ++++  ++++ +++++                                       
                                       +++++ ++++  ++++ +++++                                       
                                       +++++ ++++  ++++ +++++                                       
                                       +++++ ++++  ++++ +++++                                       
                                       +++++ ++++  ++++ +++++                                       
                                       +++++ ++++  ++++ +++++                                       
                                       +++++ ++++  ++++ +++++                                       
                                       +++++ ++++  ++++ +++++                                       
                                       +++++ ++++  ++++ +++++                                       
                                       +++++ ++++  ++++ +++++                                               
    '''
    lines = ascii_art.strip('\n').splitlines()
    
    for line in lines:
        if stop_event.is_set():
            break
        print(line)
        time.sleep(0.5)

def convert_pdf_to_markdown(pdf_path, md_path, stop_event):
    # Convert PDF to Markdown file. 
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            with open(md_path, 'w', encoding='utf-8') as md_file:
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    md_file.write(f"# Page {i + 1}\n\n")
                    if text:
                        md_file.write(text)
                    else:
                        md_file.write("_No text detected on this page._")
                    md_file.write("\n\n")
        print(f"\n File converted. Markdown file saved to {md_path}")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
    finally:
        stop_event.set()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown"
    )
    parser.add_argument("pdf", help="Path to PDF file.")
    parser.add_argument("md", help="Path to the output markdown file.")
    args = parser.parse_args()

    
    stop_event = threading.Event()

    art_thread = threading.Thread(target=draw_ascii_art, args=(stop_event,))
    art_thread.start()

    # Run PDF conversion in main thread.
    convert_pdf_to_markdown(args.pdf, args.md, stop_event)
  
    art_thread.join()
