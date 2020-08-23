#!/usr/bin/env python
from flobin.flo_s3 import S3Base
from flobin.flo_ssm import SSMBase
from flobin.flo_util import parse_ddl_from_dict
from json import loads
from pyspark.sql.functions import udf, lit, struct
from pyspark.sql.types import FloatType, IntegerType
from pyspark import SparkConf
from pyspark.sql import SparkSession
from uuid import uuid4
from yaml import safe_load

import findspark
import logging


def personas():
    """Run personas segmentation job and update fs_insights.personas."""
    def cluster_calc(row):
        cols = df_cols or []
        clust = 0
        dist = float('inf')
        for centroid in centroid_dict['centroids']:
            ctrd_clust = centroid['cluster']
            coords = [centroid[c.lower()[:-len(scaled_column_affix)]]
                      for c in cols if c.lower() not in ['evt_user_id', 'evt_site_id']]
            dist_test = sum([(float(a_i) - float(b_i)) ** 2 for a_i, b_i in zip(row, coords)])
            dist_test = dist_test ** 0.5
            if dist_test < dist:
                dist = dist_test
                clust = int(ctrd_clust)
        return clust

    def scale_fn(array, max_, min_):
        """Min-max scale every column in for loop."""
        array, max_, min_ = map(float, (array, max_, min_))
        if max_ != 0:
            return (array - min_) / (max_ - min_)
        else:
            return 0.0

    findspark.init()
    logger = logging.getLogger('airflow.task')
    schema = 'fs_insights'
    table = 'personas'
    scaled_column_affix = '_scaled'
    s3, ssm = S3Base(), SSMBase()
    bucket = s3.bucket
    table_yaml = s3.client.get_object(Bucket=bucket, Key='jobs/segmentation/table_definitions.yaml')['Body'].read().decode('utf-8')
    table_yaml = safe_load(table_yaml)[schema][table]
    table_meta = {schema: {table: table_yaml}}
    ddl_str = parse_ddl_from_dict(table_meta)
    sql_str = s3.client.get_object(Bucket=bucket, Key='jobs/segmentation/personas_initial_query.sql')['Body'].read().decode('utf-8')
    minmax_dict = loads(s3.client.get_object(Bucket=bucket, Key='jobs/segmentation/minmax_dict.json')['Body'].read().decode('utf-8'))
    centroid_dict = loads(s3.client.get_object(Bucket=bucket, Key='jobs/segmentation/centroid_dict.json')['Body'].read().decode('utf-8'))
    scale_udf = udf(scale_fn, FloatType())
    cluster_udf = udf(cluster_calc, IntegerType())
    sf_args = ssm.get_snowflake_creds()
    s_conf = SparkConf()
    app_uuid = uuid4()
    s_conf.setAppName(f"{schema}-{table}-{app_uuid}")
    s_session = SparkSession.builder.config(conf=s_conf).getOrCreate()
    run_query = s_session._sc._gateway.jvm.net.snowflake.spark.snowflake.Utils.runQuery
    run_query(sf_args, f"CREATE SCHEMA IF NOT EXISTS {schema}")
    run_query(sf_args, ddl_str)

    logger.warning('Reading from Snowflake...')
    df = s_session.read \
        .format('net.snowflake.spark.snowflake') \
        .options(**sf_args) \
        .option('query', sql_str) \
        .load()

    logger.warning('Generating output...')
    df = df.na.fill(0)
    for c, scale in minmax_dict['minmax'].items():
        s_col = '{0}{1}'.format(c, scaled_column_affix).lower()
        df = df.withColumn(
            s_col,
            scale_udf(
                c,
                lit(scale[0]),
                lit(scale[1])
            )
        )
        df = df.drop(c)
    df_cols = df.columns

    pred = df.withColumn(
        'cluster',
        cluster_udf(
            struct([df[c] for c in df_cols if c.lower() not in ['evt_user_id', 'evt_site_id']]),
        )
    )
    pred = pred.select('evt_user_id', 'evt_site_id', 'cluster')
    logger.warning('Writing to Snowflake...')
    pred.write \
        .format('snowflake') \
        .mode('overwrite') \
        .options(**sf_args) \
        .option('dbtable', '{0}.{1}'.format(schema, table)) \
        .save()


if __name__ == '__main__':
    personas()
