# Starting Redis
redis-server

# Erase all Redis Data in memory (testing only)
# $ redis-cli FLUSHALL

# Start DynamoDB
cd ..
cd ..
cd ..
cd ..
cd dynamodb_local_latest
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

# Initialize the Polls table & create a default poll
cd ..
cd Projects/Project3/api/bin
python3 initPolls.py