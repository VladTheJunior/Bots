# /bin/sh
while true
do
echo "$(date '+%d.%m.%Y %H:%M:%S') :: Запуск Discord бота"
python3 bot.py
echo "$(date '+%d.%m.%Y %H:%M:%S') :: Перезапуск Discord бота через 30 секунд"
sleep 30
done
