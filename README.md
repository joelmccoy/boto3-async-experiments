# boto3-async-experiments
Experiments/performance testing with boto3 and async.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Performance Test
The performance tests use the s3 ListBuckets call.  The test will run the call 100 times and then run the test 3 times.  The results will be printed to the console.

You can modify the `src/main.py` file to change the number of times to run each test and the number of times to run the s3 ListBuckets call.

```bash
python3 src/main.py
```

## Results
Sample of results on my local machine (Apple M2 Pro with 16GB RAM)

100 runs of the s3 ListBuckets call and 3 runs of the test
```
synchronous elapsed time for run 0: 7.94390033298987 seconds
synchronous elapsed time for run 1: 7.485672875016462 seconds
synchronous elapsed time for run 2: 7.424951791006606 seconds
async boto3 elapsed time for run 0: 0.8219816250202712 seconds
async boto3 elapsed time for run 1: 0.8033592499850783 seconds
async boto3 elapsed time for run 2: 0.8520164999936242 seconds
async aioboto3 elapsed time for run 0: 1.4005139590008184 seconds
async aioboto3 elapsed time for run 1: 1.4623616670141928 seconds
async aioboto3 elapsed time for run 2: 1.4225388749910053 seconds
Average synchronous elapsed time: 7.6181749996709796 seconds
Average async boto3 elapsed time: 0.8257857916663246 seconds
Average async aioboto3 elapsed time: 1.4284715003353388 seconds
```

## Conclusion
* The async boto3 option is faster than the synchrous boto3 option (about 9x faster).  
* The async aioboto3 option is still faster than the synchronous boto3 option (about 5.3x faster).

When running a large number of boto3 calls that can be run concurrently, it is worth using the async boto3 option to speed up the execution time.