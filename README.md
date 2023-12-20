# Sound of DNA
![Screenshot of the system](/static/img/screenshot.png)

Prototype software implementing an algorithm to sonify genetic data in FASTA format. It's part of my graduation final project for the Computer Engineering course.
You can find audio examples produced by the algorithm [here](https://github.com/ofabiobraga/sound-of-dna/tree/main/examples).

## Dependencies
- Docker

### Get Started
Run this command to build project locally. It will create Docker containers and all prerequisites will be installed.

```bash
make build
```

After that, the project is ready to be served and exposed on top of FastAPI. Just run the command below.
```bash
make serve
```

It can now be accessed from any web browser on the URL http://localhost:8000.

If you need to stop server, just run the command below.
```bash
make stop
```

To remove files generated by the sonification algorithm, you can clean it running 
```bash
make clean
```
