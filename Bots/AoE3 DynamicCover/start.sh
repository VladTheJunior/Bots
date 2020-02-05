# /bin/sh
while true
do
echo "$(date '+%d.%m.%Y %H:%M:%S') :: Запуск DynamicCover"
python3 DynamicCover.py
echo "$(date '+%d.%m.%Y %H:%M:%S') :: Перезапуск DynamicCover через 5 секунд"
sleep 5
done
