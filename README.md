# Database_Project


-   ### API
   
	-  	 The API gets data from (https://allsportsapi.com/).
	    


    ### Kafka Producer (Topic: Football_live)
    
	
	-   The data from the API stream is pushed to Kafka (Producer.py) under topic: Football_live


## How to run the code

	    
-   #### Start Zookeeper
    

		 docker run --name myzookeeper --restart always -p 2181:2181 zookeeper
    

  

-   #### Start Kafka
    

		docker run --name mykafkaserver --link myzookeeper:zookeeper -p 9092:9092 apache/kafka
    

  

-   #### Create football_live Topic
    

		   docker exec -it mykafkaserver /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic football_live
    

  

-   #### Create football_live_clean Topic
    

		 docker exec -it mykafkaserver /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic football_live_clean
    

  

-  #### Push Data From API Stream to Kafka Topic: football_live
    
        (pip install kafka-python-ng requests)
		python Producer.py
        
    

  

-   #### Structure and Validate Data, Push To MongoDB and Kafka Topic football_live_clean
    

		  EN COURS
    

  

-  #### View football_live Topic
    

		docker exec -it mykafkaserver /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic football_live --from-beginning
    

  

-   #### View football_live_clean Topic
    

		docker exec -it mykafkaserver /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic football_live_clean --from-beginning
    

