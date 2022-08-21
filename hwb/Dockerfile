FROM python:3.9-alpine
# set work directory
WORKDIR /app/
# install dependencies
RUN pip install --user -U aiogram==2.21 rich==12.4.4 redis==4.3.4
ADD . .
ENTRYPOINT ["python", "app.py"]
