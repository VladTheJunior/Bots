# /bin/sh
while true
do
echo "$(date '+%d.%m.%Y %H:%M:%S') :: Запуск VK бота"
python3 VK.py
echo "$(date '+%d.%m.%Y %H:%M:%S') :: Перезапуск VK бота через 5 секунд"
sleep 5
done
