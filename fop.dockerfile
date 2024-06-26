FROM python:3.11-bullseye
ENV DEBIAN_FRONTEND noninteractive


RUN echo "net.ipv6.conf.all.disable_ipv6=1" >> /etc/sysctl.conf && \
    echo "net.ipv6.conf.default.disable_ipv6=1" >> /etc/sysctl.conf && \
    echo "net.ipv6.conf.lo.disable_ipv6=1" >> /etc/sysctl.conf && \
    echo "net.ipv6.conf.tun0.disable_ipv6=1" >> /etc/sysctl.conf




RUN apt-get update && apt-get install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    iputils-ping \
    iproute2 \
    traceroute \
    nano \
    openvpn \
    ca-certificates \
    net-tools

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install ./google-chrome-stable_current_amd64.deb
RUN curl -fSsL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor | tee /usr/share/keyrings/google-chrome.gpg >> /dev/null
RUN echo deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y nano google-chrome-stable


WORKDIR /app
RUN mkdir static templates
COPY ./templates/index.html ./templates/index.html
COPY ./requirements.txt /app/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt 
COPY temp_cred.txt /app
RUN chmod 777 /app/temp_cred.txt
COPY fop-startup.sh /app/
RUN chmod 777 /app/fop-startup.sh


COPY ./app_fop.py /app/

#CMD ["/bin/sh", "-c", "python ./app_fop.py"]
#CMD ["/bin/sh", "-c", "sleep infinity"]
CMD ["/bin/sh", "-c", "/app/fop-startup.sh"]
