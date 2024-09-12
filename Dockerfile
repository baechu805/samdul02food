FROM python:3.11

WORKDIR /code

COPY src/samdul16food/main.py /code/

RUN pip install --no-cache-dir --upgrade git+https://github.com/baechu805/samdul02food.git

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]FROM 
