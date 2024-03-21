from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime, timedelta

# https://registry.astronomer.io/providers/postgres/modules/postgresoperator
# https://registry.astronomer.io/providers/apache-airflow/modules/pythonoperator
class CustomPostgresOperator(PostgresOperator):

    template_fields = ('sql', 'parameters',)

    def execute(self, context):
        return 0


def _extract(partner_name):
    print(partner_name)

with DAG("301_templating", description="Templating in both variables and files. Checkout Render tab ofr each task.",
        start_date=datetime(2021, 1, 1),
        schedule_interval='@daily',
         dagrun_timeout=timedelta(minutes=10),
         tags=['data_science', 'customer'],
         catchup=False
         ) as dag:

         extract = PythonOperator(
             task_id="extract",
             python_callable=_extract,
             op_args=["{{ var.json.my_dag_partner.name }}"]
         )

         fetching_data = CustomPostgresOperator(
             task_id="fetching_data",
             sql="sql/301_my_request.sql",   # template_ext https://github.com/apache/airflow/blob/main/airflow/providers/postgres/operators/postgres.py#L46
             parameters={
                 'next_ds': '{{ next_ds }}',
                 'prev_ds': '{{ prev_ds }}',
                 'partner_name': '{{ var.json.my_dag_partner.name }}'
             }
         )
