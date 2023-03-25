from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.mobile import APIGatewayEndpoint
from diagrams.onprem.aggregator import Fluentd

with Diagram("Braze integration", show=True):

    with Cluster("Central account"):
        sns_in = SNS("SNS IN")
        sns_out = SNS("SNS OUT")

    with Cluster("Notification Service"):
        sqs = SQS("FIFO")

        sqs_dld = SQS("DLQ")

        with Cluster("Processing"):
            lambdas = [
                LambdaFunction("LAMBDA")
            ]

    braze = Fluentd("Braze")


    with Cluster("PostMaster"):
        api = APIGatewayEndpoint("API")


    sns_in >> sqs >> lambdas
    sqs_dld << Edge(color="red", label="Error") << lambdas
    lambdas >> Edge(label="Batch") >> braze

    braze >> Edge(label="Webhook") >> api
    api >>Edge(label="canvas_entry_properties.callback") >> sns_out
