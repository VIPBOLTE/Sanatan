# Use Python 3.8 slim image
FROM python:3.8.5-slim-buster

# Set environment variables
ENV PIP_NO_CACHE_DIR 1

# Fix apt sources if needed
RUN sed -i.bak 's/us-west-2\.ec2\.//' /etc/apt/sources.list

# Installing Required System Packages
RUN apt update && apt upgrade -y && \
    apt install --no-install-recommends -y \
    debian-keyring \
    debian-archive-keyring \
    bash \
    bzip2 \
    curl \
    figlet \
    git \
    util-linux \
    libffi-dev \
    libjpeg-dev \
    libjpeg62-turbo-dev \
    libwebp-dev \
    linux-headers-amd64 \
    musl-dev \
    musl \
    neofetch \
    php-pgsql \
    python3-lxml \
    postgresql \
    postgresql-client \
    python3-psycopg2 \
    libpq-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libxslt1-dev \
    python3-pip \
    python3-requests \
    python3-sqlalchemy \
    python3-tz \
    python3-aiohttp \
    openssl \
    pv \
    jq \
    wget \
    python3-dev \
    libreadline-dev \
    libyaml-dev \
    gcc \
    sqlite3 \
    libsqlite3-dev \
    sudo \
    zlib1g \
    ffmpeg \
    libssl-dev \
    libgconf-2-4 \
    libxi6 \
    xvfb \
    unzip \
    libopus0 \
    libopus-dev \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* /tmp/*

# Upgrade pip and setuptools to latest version
RUN pip3 install --upgrade pip setuptools

# Copy your application files into the Docker container
COPY . /root/utahimebot-
WORKDIR /root/utahimebot-

# Install Python dependencies from the requirements.txt file
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh

# Set the PATH environment variable
ENV PATH="/home/bot/bin:$PATH"

# Expose the necessary port
EXPOSE 5000

# Define the command to run your bot
CMD ["/root/entrypoint.sh"]
