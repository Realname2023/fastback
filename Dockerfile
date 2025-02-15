FROM python:3.10-alpine
WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt && chmod 755 .
COPY . .
EXPOSE 8000
ENV TZ Asia/Almaty
CMD ["python3", "-u", "main.py"]