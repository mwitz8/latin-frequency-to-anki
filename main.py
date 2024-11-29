import os
from pathlib import Path
import pickle
from progress.bar import Bar
from progress.spinner import PieSpinner
from cltk import NLP
from cltk.dependency.processes import LatinStanzaProcess
from cltk.data.fetch import FetchCorpus

cltk_nlp = NLP(language="lat", suppress_banner=True)
cltk_nlp.pipeline.processes[1]
cltk_nlp.pipeline.processes[1] = LatinStanzaProcess

def serialize_cltk_doc(cltk_doc, file_path: Path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file = open(file_path, 'wb')
    pickle.dump(cltk_doc, file)
    file.close()

text_count = 0
corpus_path = Path(os.getcwd(), 'data', 'latin', 'text', 'historical')
for text_path_str in corpus_path.rglob('*.txt'):
    text_count = text_count + 1
with Bar('analyzing texts', max=text_count) as progress:
    for text_path_str in corpus_path.rglob('*.txt'):
        with open(text_path_str, 'r') as text:
            text_path = Path(text_path_str)
            data_path = Path(*(list(text_path.parts)[:text_path.parts.index('historical')+1] + ['cltk_data'] + list(text_path.parts[text_path.parts.index('historical')+1:]))).with_suffix('.cltk')
            if not data_path.exists():
                cltk_doc = cltk_nlp.analyze(text=text.read())
                serialize_cltk_doc(cltk_doc, data_path)
        progress.next()
