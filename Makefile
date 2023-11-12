build:
	@docker-compose build

serve:
	@docker-compose up -d

test:
	@python3 src/main.py src/samples/sars-cov-2.fasta

install:
	@pip3 install -r src/requirements.txt

clean:
	@rm -rf src/midi/* src/uploads/*