# Starting from OpenJDK
FROM openjdk:8u292-jdk

# Some build args defined in the docker-compose.yaml file
ARG DEPS_SRC
ARG HEXTRACT_SRC

# Use as environment variables
ENV DEPS_SRC=$DEPS_SRC
ENV HEXTRACT_SRC=$HEXTRACT_SRC

# Install dependencies
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | tee /etc/apt/sources.list.d/sbt.list && \
    echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | tee /etc/apt/sources.list.d/sbt_old.list && \
    curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add && \
    apt-get update && \
    apt-get install -y git wget python3 python3-pip scala sbt && \
    apt-get clean -y

# Install Grobid
WORKDIR $DEPS_SRC
RUN wget https://github.com/kermitt2/grobid/archive/0.6.2.zip && \
    unzip 0.6.2.zip && cd grobid-0.6.2 &&  \
    ./gradlew clean install && \
    echo "./gradlew run > grobid.out 2>&1" > grobid_startup.sh

# Install PDFFigures
RUN git clone https://github.com/jcpassy/pdffigures2 && \
    cd pdffigures2 && \
    sbt compile

# Install HaptipediaExtractor
COPY . $HEXTRACT_SRC
WORKDIR $HEXTRACT_SRC
RUN python3 -m pip install -U pip && \
    python3 -m pip install -r requirements.txt

# Start GROBID service
# ENTRYPOINT ["/tini" "-s" "--"]
# CMD ["cd $DEPS_SRC/grobid-0.6.2 && . ./grobid_startup.sh"]
SHELL ["/bin/bash", "-c"]
#CMD bash
ENTRYPOINT source docker-entrypoint.sh && bash
#CMD cd /work/src/grobid-0.6.2 && . ./grobid_startup.sh
