FROM python:3.9.14

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Now copy in our code, and run it
COPY . /app

RUN python ./scripts/PreRun.py

RUN echo 'alias pmmm="python manage.py makemigrations"' >> ~/.bashrc
RUN echo 'alias pmm="python manage.py migrate"' >> ~/.bashrc
RUN echo 'alias pmf="python manage.py flush"' >> ~/.bashrc

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]