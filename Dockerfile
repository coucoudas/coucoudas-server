FROM python:3.9

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]