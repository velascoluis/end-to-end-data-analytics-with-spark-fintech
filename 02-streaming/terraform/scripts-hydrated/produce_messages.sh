#!/bin/sh
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
for i in {0..100000}
do
        bool_arr[0]="false"
        bool_arr[1]="true"
        rand=$[$RANDOM % ${#bool_arr[@]}]
        echo '{"key":'$i'}&{"timestamp" :"'$(date)'" ,"name" : "bitcoin_transaction", "is_coinbase": "'${bool_arr[$rand]}'", "tx_value":"'$i'"}' |    /usr/lib/kafka/bin/kafka-console-producer.sh --broker-list kafka-cluster-w-0:9092 --topic transactions --property "parse.key=true" --property "key.separator=&"  
        sleep 1
done









    

