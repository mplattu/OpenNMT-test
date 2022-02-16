# OpenNMT-test

## Before Starting

If you are working on a fresh installation install these first:
 * `apt install git make python3-pip python3-virtualenv`
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
