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
    return f'''<body><div class="content" id="content">'''

def gen_p(text):
    return f'''<p id="page">{text}</p>'''

def gen_pagenum(pagenum):
    return f'''<div id="pagenum"><p>{pagenum}</p></div>'''

def gen_tail():
    return f'''</div></body></html>'''


def load_pdf_from_url(URL):

    def remove_newlines(raw_text):
        return " ".join(raw_text.split("\n"))
                
    req = urllib.request.Request(URL, headers={'User-Agent' : "Magic Browser"})
    remote_file = urllib.request.urlopen(req).read()
    remote_file_bytes = io.BytesIO(remote_file)
    pdfdoc = PyPDF2.PdfReader(remote_file_bytes)

    output_html = ""
    output_html += gen_head("PDF VIEWER")
    output_html += gen_header()
    for i in range(len(pdfdoc.pages)):
        output_html += gen_p(remove_newlines(pdfdoc.pages[i].extract_text()))
        output_html += gen_pagenum(str(i))
    output_html += gen_tail()

    with open("index.html", "w") as html_out:
        html_out.write(output_html)

pdf_url = input("Input pdf url\n")
load_pdf_from_url(pdf_url)
