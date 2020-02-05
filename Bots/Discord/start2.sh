# /bin/sh
while true
do
echo "$(date '+%d.%m.%Y %H:%M:%S') :: Запуск Discord Event бота"
python3 event.py
echo "$(date '+%d.%m.%Y %H:%M:%S') :: Перезапуск Discord бота через 30 секунд"
sleep 30
done
