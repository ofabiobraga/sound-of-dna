start:
	@python3 main.py samples/cannabis-sativa-amalgavirus.fasta

install:
	@pip3 install -r requirements.txt

clean:
	@rm -rf midi/*