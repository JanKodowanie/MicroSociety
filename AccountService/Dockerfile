FROM python:3.9

WORKDIR /app
COPY . ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN aerich upgrade

CMD ["./wait_for_it.sh", "rabbit:15672","-t", "30", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]