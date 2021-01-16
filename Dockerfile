FROM python:3.9
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "run.py"]
