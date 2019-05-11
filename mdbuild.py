

from io import StringIO
from os import listdir
from os.path import isfile, join, dirname
from shutil import copyfile
import panflute as pf
import yaml, sys, re, hashlib, json, os, traceback, urllib.parse
from util import *

class md_builder:
    def __init__(self, filename, output_dir, plugins={}):
        self.OK = False
        self.ID = ''
        self.node = {}
        self.filename = filename
        self.output_dir = output_dir
        self.plugins = plugins
        with open(filename,"rb") as f:
            doc = pf.convert_text(f.read().decode(),standalone=True)
        doc = doc.walk(self.extract_metadata)
        self.doc = pf.convert_text(doc, input_format='panflute',output_format='html').encode('utf-8')
        self.OK = True

    def extract_metadata(self, elem, doc):
        if (isinstance(elem, pf.Code) or isinstance(elem, pf.CodeBlock)):
            print(elem.classes)
            if 'info' in elem.classes:
                print("info")
                data,new_edges = parse_config(elem.text)
                if not 'name' in data:
                    sys.stderr.write("WARNING: 'name' required in info\n")
                    return []
                self.node = {x:data[x] for x in data}
                self.node['edges'] = {'has':{}, 'is':{}}
                edges = self.node['edges']
                self.ID = get_id(self.node['name'])
                add_edges(new_edges, edges)
                return []
            else:
                for p in self.plugins:
                    if p in elem.classes:
                        inner_doc = pf.convert_text(elem.text,standalone=True)
                        inner_doc = inner_doc.walk(self.extract_metadata)
                        inner_doc = pf.convert_text(inner_doc, input_format='panflute',output_format='html')
                        return pf.RawBlock("""<script type="category/plugin" lang="{}">\n{}\n</script>""".format(p,inner_doc),format="html")
                    
        elif isinstance(elem, pf.Link) or isinstance(elem, pf.Image):
            new_url = get_file(self.ID, self.filename, elem.url, self.output_dir)
            print("URL",elem.url)
            if new_url:
                elem.url = new_url
            elif elem.url[:5] == "node:":
                target = urllib.parse.unquote(elem.url[5:])
                print("LINK",target)
                return pf.RawInline("""<script type="category/plugin" lang="link">{}:{}</script>""".format(get_id(target),target),format="html")
            elif elem.url[:6] == "query:":
                q = urllib.parse.unquote(elem.url[6:])
                print("QUERY",q)
                return pf.RawInline("""<script type="category/plugin" lang="query">{}</script>""".format(q),format="html")
        elif isinstance(elem, pf.Math):
            print("MATH",elem.text)
            return pf.Str("$"+elem.text+"$")

if __name__ == "__main__":
    import docopt
    args = docopt.docopt("""Usage: mdbuild.py <input_file> <output_dir>""")
    md_builder(args['<output_dir>'])
    
