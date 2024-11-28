import os
from pathlib import Path
import pickle
from progress.bar import Bar
from progress.spinner import PieSpinner
from cltk import NLP
from cltk.dependency.processes import LatinStanzaProcess
from cltk.data.fetch import FetchCorpus

corpus_downloader = FetchCorpus(language="lat")
corpus_downloader.import_corpus('lat_text_latin_library', suppress_banner=True)
cltk_nlp = NLP(language="lat")
cltk_nlp.pipeline.processes[1]
cltk_nlp.pipeline.processes[1] = LatinStanzaProcess

file_count = 0
for file_path in Path(os.path.join(os.path.expanduser('~'), 'cltk_data', 'lat', 'text', 'lat_text_latin_library')).rglob('*.txt'):
    file_count = file_count + 1
data = []
with Bar('analyzing texts', max=file_count) as progress:
    print('\n')
    for file_path in Path(os.path.join(os.path.expanduser('~'), 'cltk_data', 'lat', 'text', 'lat_text_latin_library')).rglob('*.txt'):
        with open(file_path, 'r') as file:
            cltk_doc = cltk_nlp.analyze(text=file.read())
            data.append(cltk_doc)
        progress.next()

with PieSpinner('serializing data...') as progress:
    open('data', 'w').close()
    data_file = open(Path('data'), 'ab')
    pickle.dump(data, data_file)
    data_file.close()
    progress.next()
