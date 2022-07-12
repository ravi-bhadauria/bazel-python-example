"""The Python implementation of the GRPC server."""

from concurrent import futures
import logging

import grpc

import sorting_service_pb2
import sorting_service_pb2_grpc


class SortingService(sorting_service_pb2_grpc.SortingServiceServicer):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        super(SortingService, self).__init__()

    def execute(
        self, request: sorting_service_pb2.SortingRequest, context: grpc.ServicerContext
    ) -> sorting_service_pb2.SortingResponse:
        self.logger.info("Received: {}".format(request))
        return sorting_service_pb2.SortingResponse(
            ip=None, unsortedArray=[], sortedArray=[]
        )


def serve():
    logger = logging.getLogger(__name__)
    try:
        logging.info("Starting SortingService")
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
        )
        sorting_service_pb2_grpc.add_SortingServiceServicer_to_server(
            SortingService(), server
        )
        server.add_insecure_port("[::]:50051")
        server.start()

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
