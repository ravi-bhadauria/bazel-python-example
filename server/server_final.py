"""The Python implementation of the GRPC server."""

from concurrent import futures
import logging

import grpc

import sorting_service_pb2
import sorting_service_pb2_grpc

from grpc_reflection.v1alpha import reflection
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

from py_grpc_prometheus.prometheus_server_interceptor import PromServerInterceptor
from prometheus_client import start_http_server

import socket
import random


def get_container_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return str(s.getsockname()[0])


class SortingService(sorting_service_pb2_grpc.SortingServiceServicer):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        super(SortingService, self).__init__()

    def execute(
        self, request: sorting_service_pb2.SortingRequest, context: grpc.ServicerContext
    ) -> sorting_service_pb2.SortingResponse:
        self.logger.info("Received: {}".format(request))
        unsortedArray = list(range(request.arrsize))
        random.shuffle(unsortedArray)
        self.logger.info("unsorted: {}".format(unsortedArray))
        sortedArray = sorted(unsortedArray)
        self.logger.info("sorted: {}".format(sortedArray))
        return sorting_service_pb2.SortingResponse(
            ip=get_container_ip(), unsortedArray=unsortedArray, sortedArray=sortedArray
        )


def serve():
    logger = logging.getLogger(__name__)
    try:
        logging.info("Starting SortingService")
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
            interceptors=(
                PromServerInterceptor(
                    legacy=True,
                    enable_handling_time_histogram=True,
                    skip_exceptions=True,
                ),
            ),
        )
        sorting_service_pb2_grpc.add_SortingServiceServicer_to_server(
            SortingService(), server
        )

        # Reflection service block
        # Add services to reflection
        SERVICE_NAMES = (
            sorting_service_pb2.DESCRIPTOR.services_by_name["SortingService"].full_name,
            health.SERVICE_NAME,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, server)

        # Health checks block
        # Create a health check servicer. We use the non-blocking implementation
        # to avoid thread starvation.
        health_servicer = health.HealthServicer(
            experimental_non_blocking=True,
            experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=16),
        )
        # Mark all services as healthy.
        health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
        for service in SERVICE_NAMES:
            health_servicer.set(service, health_pb2.HealthCheckResponse.SERVING)

        server.add_insecure_port("[::]:50051")
        server.start()
        # Start an end point to expose metrics.
        start_http_server(8080)
        logger.info(
            "Started py-grpc-prometheus SortingService, grpc at localhost:50051, "
            "metrics at http://localhost:8080"
        )

        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.error("\rShutting down server\r")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)-15s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%y %H:%M:%S",
    )
    serve()
