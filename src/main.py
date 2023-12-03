import asyncio
import functools
from time import perf_counter

import aioboto3
import boto3


AMOUNT_OF_CALLS = 100  # The ammount of calls to make to list_buckets
TIMES_TO_RUN_PERFORMANCE_TEST = 3


def synchronous_example() -> float:
    """Tests the performance of the boto3 client used synchronously."""
    client = boto3.client("s3")
    start_time = perf_counter()
    for _ in range(AMOUNT_OF_CALLS):
        client.list_buckets()
    end_time = perf_counter()
    return end_time - start_time


async def async_aiboto3_example():
    session = aioboto3.Session()
    async with session.client("s3") as s3:
        start_time = perf_counter()
        await asyncio.gather(*[s3.list_buckets() for _ in range(AMOUNT_OF_CALLS)])
        end_time = perf_counter()
        return end_time - start_time


async def async_boto3_example() -> float:
    client = boto3.client("s3")
    loop = asyncio.get_running_loop()

    start_time = perf_counter()
    await asyncio.gather(
        *[
            loop.run_in_executor(None, functools.partial(client.list_buckets))
            for _ in range(AMOUNT_OF_CALLS)
        ]
    )
    end_time = perf_counter()
    return end_time - start_time


def main():
    """Entry point of the application."""
    sync_elapsed_time_total = 0
    async_boto3_elapsed_time_total = 0
    async_aiboto3_elapsed_time_total = 0

    for i in range(TIMES_TO_RUN_PERFORMANCE_TEST):
        elapsed_time = synchronous_example()
        sync_elapsed_time_total += elapsed_time
        print(f"synchronous elapsed time for run {i}: {elapsed_time} seconds")

    for i in range(TIMES_TO_RUN_PERFORMANCE_TEST):
        elapsed_time = asyncio.run(async_boto3_example())
        async_boto3_elapsed_time_total += elapsed_time
        print(f"async boto3 elapsed time for run {i}: {elapsed_time} seconds")

    for i in range(TIMES_TO_RUN_PERFORMANCE_TEST):
        elapsed_time = asyncio.run(async_aiboto3_example())
        async_aiboto3_elapsed_time_total += elapsed_time
        print(f"async aioboto3 elapsed time for run {i}: {elapsed_time} seconds")

    print(
        f"Average synchronous elapsed time: {sync_elapsed_time_total / TIMES_TO_RUN_PERFORMANCE_TEST} seconds"
    )
    print(
        f"Average async boto3 elapsed time: {async_boto3_elapsed_time_total / TIMES_TO_RUN_PERFORMANCE_TEST} seconds"
    )
    print(
        f"Average async aioboto3 elapsed time: {async_aiboto3_elapsed_time_total / TIMES_TO_RUN_PERFORMANCE_TEST} seconds"
    )


if __name__ == "__main__":
    main()
