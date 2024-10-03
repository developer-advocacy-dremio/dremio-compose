from pyspark.sql import SparkSession

# Initialize SparkSession with Nessie, Iceberg, and S3 configuration
spark = (
    SparkSession.builder.appName("Nessie-Iceberg-PySpark")
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0,software.amazon.awssdk:bundle:2.24.8,software.amazon.awssdk:url-connection-client:2.24.8')
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.catalog.nessie", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.nessie.uri", "http://nessie:19120/iceberg/main/")
    .config("spark.sql.catalog.nessie.warehouse", "s3://my-bucket/")
    .config("spark.sql.catalog.nessie.type", "rest")
    .getOrCreate()
)

# Create a namespace in Nessie
spark.sql("CREATE NAMESPACE IF NOT EXISTS nessie.demo").show()

# Create a table in the `nessie.demo` namespace using Iceberg
spark.sql(
    """
    CREATE TABLE IF NOT EXISTS nessie.demo.sample_table (
        id BIGINT,
        name STRING
    ) USING iceberg
    """
).show()

# Insert data into the sample_table
spark.sql(
    """
    INSERT INTO nessie.demo.sample_table VALUES
    (1, 'Alice'),
    (2, 'Bob')
    """
).show()

# Query the data from the table
spark.sql("SELECT * FROM nessie.demo.sample_table").show()

# Stop the Spark session
spark.stop()