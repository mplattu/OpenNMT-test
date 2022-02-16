.PHONY: test

clean:
	rm -fR OpenNMT-test

get-data:
	-mkdir -p data/finlex/
	if [ ! -f data/finlex/fi.txt || ! -f data/finlex/sv.txt]; then wget -O data/finlex/moses.zip https://object.pouta.csc.fi/OPUS-Finlex/v2018/moses/fi-sv.txt.zip; cd data/finlex; unzip moses.zip; mv Finlex.fi-sv.fi fi.txt; mv Finlex.fi-sv.sv sv.txt; rm *.zip *.xml; fi

install:
	virtualenv -p python3 data
	( \
		. data/bin/activate; \
		pip3 install OpenNMT-py; \
	)

prepare-data:
	python3 prepare-data.py

vocabulary:
	cp config/finlex.yaml data/
	( \
		. data/bin/activate; \
		cd data; \
		onmt_build_vocab -config finlex.yaml -n_sample 10000; \
	)

train:
	cp config/finlex.yaml data/
	( \
		. data/bin/activate; \
		cd data; \
		onmt_train -config finlex.yaml; \
	)

test:
	( \
		. data/bin/activate; \
		cd data; \
		onmt_translate -model finlex/run/model_step_1000.pt -src ../test/sample-fi.txt -output ./translated-test.txt -gpu 0 -verbose; \
		echo "Samples:" >test-report.txt; \
		echo "--------" >>test-report.txt; \
		cat ../test/sample-fi.txt >>test-report.txt; \
		echo "Expected:" >>test-report.txt; \
		echo "---------" >>test-report.txt; \
		cat ../test/sample-sv.txt >>test-report.txt; \
		echo "Observed:" >>test-report.txt; \
		echo "---------" >>test-report.txt; \
		cat translated-test.txt >>test-report.txt; \
		rm translated-test.txt; \
	)	

