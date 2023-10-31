
#FROM fishtownanalytics/dbt:1.0.0
FROM ghcr.io/dbt-labs/dbt-bigquery:1.6.6
ENV DBT_PROFILES_DIR=/demo/profile/
COPY profiles.yml /demo/profile/
COPY keyfile.json /demo
COPY dbt_run.sh /demo
COPY dbt /demo

#USER root
#RUN chown -R dbt_user /dbt
#USER dbt_user

RUN chmod +x /demo/dbt_run.sh
WORKDIR /demo
RUN /demo/dbt_run.sh deps
ENTRYPOINT []
