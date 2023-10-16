start:
	@python3 main.py samples/sars-cov-2.fasta

install:
	@pip3 install -r requirements.txt

clean:
	@rm -rf midi/*