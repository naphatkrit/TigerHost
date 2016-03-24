FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /docs
WORKDIR /docs
COPY requirements.txt /docs/
RUN pip install -r requirements.txt
COPY . /docs/
RUN make html
VOLUME /docs/_build/html
