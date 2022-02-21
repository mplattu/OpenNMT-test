# OpenNMT-test

## Before Starting

If you are working on a fresh installation install these first:
 * `apt install git make python3-pip python3-virtualenv python3-pdfminer`
 * Nvidia CUDA: https://developer.nvidia.com/cuda-zone (Do not use the packaged version `nvidia-cuda-framework` as it is outdated)

## Manual Process

1. Download datasets: `make get-data`
 * https://opus.nlpl.eu/
 * Select `fi (Finnish)` and `sv (Swedish)`
 * Finlex data, version `moses`

1. Process datasets: `make prepare-data`
 * Creates training and validation data files to `data/finlex/`
 * `src-train.txt`
 * `src-val.txt`
 * `tgt-train.txt`
 * `tgt-val.txt`

1. Install OpenNMT-py: `make install`
 * Creates a virtualenv `data` and installs OpenNMT-py

1. Create vocabulary: `make vocabulary`
 * Creates vocabulary files using `onmt_build_vocab` based on `config/finlex.yaml`

1. Train the model: `make train`
  * Makes training using `onmt_train` based on `config/finlex.yaml`

## Adding a new dataset

1. Create a download rule to `Makefile`. See `get-data-*` for an example.
1. Add new dataset to `prepare-data.py`
1. Add new dataset to `config/meb.yaml`
1. Run your new `make get-data-rule`
1. `make prepare-data`
1. `make vocabulary`
1. `make train`

## MEB Dataset

MEB dataset (`training-material/meb/`) was created as follows:
1. Downloaded PDF document and named Finnish and Swedish versions accordingly.
   Filenames after this step: `1-fi.pdf`, `1-sv.pdf`, `2-fi.pdf`, `2-sv.pdf`,
   `...`
1. Executing `meb-pdf-to-text.py` which extracts text from PDF files, removes
   unwanted characters and tries to format one sentence into single line.
   Filenames after this step: `1-fi.raw-txt`, `1-sv.raw-txt`, `2-fi.raw-txt`,
   `2-sv.raw-txt`, `...`
1. Going throw the raw text files and making sure the lines in the Finnish and
   Swedish have the same meaning. This is manual work and most time-consuming part
   of the process. Filenames after this step: `1-fi.txt`, `1-sv.txt`, `2-fi.txt`,
   `2-sv.txt`, `...`
