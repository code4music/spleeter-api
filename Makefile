PHONY: install-conda
install-conda:
	wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
	bash ~/miniconda.sh -b
	rm ~/miniconda.sh
	source $(HOME)/miniconda3/bin/activate
	conda install -y -c conda-forge ffmpeg libsndfile

PHONY: run
run:
	python3 main.py

PHONY: download-music-demo
download-music-demo:
	wget https://github.com/deezer/spleeter/raw/master/audio_example.mp3

PHONY: spleeter
spleeter:
	spleeter separate -p spleeter:2stems -o output audio_example.mp3

