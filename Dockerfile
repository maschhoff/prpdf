# syntax=docker/dockerfile:1
FROM knex666/prpdf:latest
WORKDIR /source
ENV FLASK_APP=prpdf.py
ENV FLASK_RUN_HOST=0.0.0.0
#RUN apk add --no-cache gcc musl-dev linux-headers
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
#EXPOSE 5000
COPY /prpdf /source
CMD ["flask", "run"]
