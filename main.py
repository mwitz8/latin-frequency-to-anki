import os
from pathlib import Path
import pickle
from progress.bar import Bar
from progress.spinner import PieSpinner
from cltk import NLP
from cltk.dependency.processes import LatinStanzaProcess
from cltk.data.fetch import FetchCorpus

corpus_downloader = FetchCorpus(language="lat")
corpus_downloader.import_corpus('lat_text_latin_library')
cltk_nlp = NLP(language="lat", suppress_banner=True)
cltk_nlp.pipeline.processes[1]
cltk_nlp.pipeline.processes[1] = LatinStanzaProcess

def serialize_cltk_doc(cltk_doc, file_path: Path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file = open(file_path, 'wb')
    pickle.dump(cltk_doc, file)
    file.close()

file_count = 0
for file_path in Path(os.path.expanduser('~'), 'cltk_data', 'lat', 'text', 'lat_text_latin_library').rglob('*.txt'):
    file_count = file_count + 1
with Bar('analyzing texts', max=file_count) as progress:
    print('\n')
    for file_path_str in Path(os.path.expanduser('~'), 'cltk_data', 'lat', 'text', 'lat_text_latin_library').rglob('*.txt'):
        with open(file_path_str, 'r') as file:
            file_path = Path(file_path_str)
            new_file_path = Path(os.getcwd(), 'data', 'cltk_docs', *list(file_path.parts)[list(file_path.parts).index('lat'):]).with_suffix('.cltk')
            if not new_file_path.exists():
                cltk_doc = cltk_nlp.analyze(text=file.read())
                serialize_cltk_doc(cltk_doc, new_file_path)
        progress.next()
