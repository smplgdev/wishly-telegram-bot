echo "Recreate image wishly_bot"
docker build -t wishly_bot .

echo "Delete old wishly container"
docker stop wishly && docker rm wishly

echo "Create new wishly container"
docker run -d --name wishly --network botnet wishly_bot

echo "Script executed successfully"
