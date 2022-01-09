#!/bin/sh
python ./cmd/update.py run \
  && pip install -r ./requirements.txt \
  && echo ------------------------------------------------------------------ \
  && python ./cmd/update.py success \
  && echo ------------------------------------------------------------------