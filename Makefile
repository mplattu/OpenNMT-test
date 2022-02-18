.PHONY: test

clean:
	rm -fR OpenNMT-test

get-data-ccmatrix:
	-mkdir -p data/ccmatrix/
	if { [ ! -f data/ccmatrix/fi.txt ] || [ ! -f data/ccmatrix/sv.txt ]; } then \
		wget -O data/ccmatrix/moses.zip https://object.pouta.csc.fi/OPUS-CCMatrix/v1/moses/fi-sv.txt.zip; \
		cd data/ccmatrix; \
		unzip moses.zip CCMatrix.fi-sv.fi >fi.txt; \
		unzip moses.zip CCMatrix.fi-sv.sv >sv.txt; \
		rm *.zip; \
	fi

get-data-finlex:
	-mkdir -p data/finlex/
	if { [ ! -f data/finlex/fi.txt ] || [ ! -f data/finlex/sv.txt ]; } then \
		wget -O data/finlex/moses.zip https://object.pouta.csc.fi/OPUS-Finlex/v2018/moses/fi-sv.txt.zip; \
		cd data/finlex; \
		unzip -p moses.zip Finlex.fi-sv.fi >fi.txt; \
		unzip -p moses.zip Finlex.fi-sv.sv >sv.txt; \
		rm *.zip; \
	fi

get-data-wikimatrix:
	-mkdir -p data/wikimatrix/
	if { [ ! -f data/wikimatrix/fi.txt ] || [ ! -f data/wikimatrix/sv.txt ]; } then \
		wget -O data/wikimatrix/moses.zip https://object.pouta.csc.fi/OPUS-WikiMatrix/v1/moses/fi-sv.txt.zip; \
		cd data/wikimatrix; \
		unzip -p moses.zip WikiMatrix.fi-sv.fi >fi.txt; \
		unzip -p moses.zip WikiMatrix.fi-sv.sv >sv.txt; \
		rm *.zip; \
	fi

get-data: get-data-ccmatrix get-data-finlex get-data-wikimatrix

install:
	virtualenv -p python3 data
	( \
		. data/bin/activate; \
		pip3 install OpenNMT-py; \
	)

prepare-data:
	-rm data/src-val.txt data/tgt-val.txt
	python3 prepare-data.py

vocabulary:
	-rm data/run/meb.vocab.src
	-rm data/run/meb.vocab.tgt

	cp config/meb.yaml data/
	( \
		. data/bin/activate; \
		cd data; \
		onmt_build_vocab -config meb.yaml -n_sample -1; \
	)

train:
	cp config/meb.yaml data/
	-rm data/run/model_step_*.pt
	( \
		. data/bin/activate; \
		cd data; \
		onmt_train -config meb.yaml; \
	)

test:
	( \
		. data/bin/activate; \
		cd data; \
		onmt_translate -model run/model_step_100000.pt -src ../test/sample-fi.txt -output ./translated-test.txt -gpu 0 -verbose; \
		echo "Samples:" >test-report.txt; \
		echo "--------" >>test-report.txt; \
		cat ../test/sample-fi.txt >>test-report.txt; \
		echo "" >>test-report.txt; \
		echo "Expected:" >>test-report.txt; \
		echo "---------" >>test-report.txt; \
		cat ../test/sample-sv.txt >>test-report.txt; \
		echo "" >>test-report.txt; \
		echo "Observed:" >>test-report.txt; \
		echo "---------" >>test-report.txt; \
		cat translated-test.txt >>test-report.txt; \
		rm translated-test.txt; \
	)
