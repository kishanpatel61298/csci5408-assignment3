from pyspark import SparkContext
import json
import re
sc = SparkContext("local", "wordcount")

flu=0;
snow=0;
emergency=0;

for i in range(30):
    text_file = sc.textFile("Tweets"+str(i)+".txt")
    counts = text_file.flatMap(lambda line: line.split(" ")) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)
    flu += counts.filter(lambda flu : 'flu' in flu).collect()
    snow += counts.filter(lambda snow : 'snow' in snow).collect()
    emergency += counts.filter(lambda emerg : 'emergency' in emerg).collect()

print(flu)
print(snow)
print(emergency)

