build:
	@docker-compose build --no-cache

serve:
	@docker-compose up -d

stop:
	@docker-compose down

restart:
	@docker-compose down && docker-compose up -d

test:
	@python3 main.py samples/sars-cov-2.fasta

install:
	@pip3 install -r requirements.txt

clean:
	@rm -rf midi/* uploads/* mp3/* json/*