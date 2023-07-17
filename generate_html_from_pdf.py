from PyPDF2 import PdfReader
import tempfile
import urllib.request
import PyPDF2
import io
import termux.termux as pixel

def gen_head(title): 
    return f'''<html><head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="../include/main.css"/>
    </head>'''

def gen_header():
    return f'''
    <body>
    <div class="content" id="content">

    '''

def gen_p(text):
    return f'''<p id="page">
    {text}
    </p>'''

def gen_pagenum(pagenum):
    return f'''<div id="pagenum"><p>
    {pagenum}
    </p></div>'''

def gen_tail():
    return f'''
    </div>
    </body>
    </html>
    '''


def load_pdf_from_url(URL):

    def extract_page(raw_text, strategy, full_page=False):
        #remove newlines
        if strategy == "flowing_stream":
            if not full_page:
                return " ".join(raw_text.split("\n")[1:-1])
            else:
                return " ".join(raw_text.split("\n"))

        #replace newlines
        if strategy == "strip_header_and_footer_simple":
            return "\n".join(raw_text.split("\n")[1:-1])
        if strategy == "block_set":
            stripped_page = extract_page(raw_text, "flowing_stream", full_page)
            words = stripped_page.split(" ")
            char_count = 0
            text_stream = "\n"
            desired_max_width = 40
            for word in words:
                #print("word=", word, "word len=", len(word), "char_count_before=", char_count)
                if char_count + len(word) > desired_max_width: 
                    text_stream += "\n" + word
                    char_count = len(word)
                else:
                    text_stream += " " + word
                    char_count += len(word)
            return text_stream
                
    req = urllib.request.Request(URL, headers={'User-Agent' : "Magic Browser"})
    remote_file = urllib.request.urlopen(req).read()
    remote_file_bytes = io.BytesIO(remote_file)
    pdfdoc = PyPDF2.PdfReader(remote_file_bytes)
    sep_delim = "="*30

    output_html = ""
    output_html += gen_head("PDF VIEWER")
    output_html += gen_header()
    for i in range(len(pdfdoc.pages)):
        output_html += gen_p(extract_page(pdfdoc.pages[i].extract_text(), "block_set", full_page=True))
        output_html += gen_pagenum(str(i))
    output_html += gen_tail()

    with open("index.html", "w") as html_out:
        html_out.write(output_html)

pdf_url = input("Input pdf url\n")
load_pdf_from_url(pdf_url)
