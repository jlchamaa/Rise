if [ $# -eq 3 ]
then
request="127.0.0.1:5000/apply?r="$1"&g="$2"&b="$3"&s=1"
curl --silent -H POST $request &
fi
if [ $# -eq 1 ]
then
request="127.0.0.1:5000/apply?r="$1"&g="$1"&b="$1"&s=1"
curl --silent -H POST $request &
fi
