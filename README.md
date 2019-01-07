Energostat
==========
 

Небольшой инструмент, который переводит показания счетчиков из html в xml 80020.


Ограничения
-----------

Атрибут летнего времени (daylightsavingtime) всегда установлен в летнее время, 
в связи с федеральным законом "Об исчислении времени" от 03.06.2011 N 107-ФЗ.


Формат XML макета 80020
-----------------------

Взято из случайного документа в интернете.

1.  Элемент message является корневым элементом. Потомками элемента _message_ являются элементы _comment_, _datetime_, _sender_, _area_. В документе допускается наличие только одного корневого элемента _message_.
2.  Атрибут class элемента _message_ является обязательным и  содержит данные о типе электронного документа. Значение атрибута class должно быть равно 80020.
3.  Атрибут version корневого элемента _message_ является обязательным и содержит данные о версии формата. Данный документ определяет версию документа 2.
4.  Атрибут number элемента _message_ является обязательным и  содержит порядковый номер сообщения. (Номера сообщений присваиваются отправителем, начинаются с 1 и увеличиваются на 1 с каждым новым сообщением). Совпадает с номером документа в  пункте 4.1.3.
5.  Элемент  _datetime_ является потомком корневого элемента _message_.В документе допускается наличие только одного элемента _datetime_.Элемент _datetime_ содержит информацию о времени создания документа. Потомками элемента _datetime_ являются элементы _timestamp_, _day_, _daylightsavingtime_.
6.  Элемент _timestamp_ является потомком элемента _datetime_.Содержимым элемента _timestamp_ является дата и время формирования данного документа в формате “ГГГГММДДччммсс”, где: ГГГГ – год, ММ – порядковый номер месяца, ДД – день, чч – час, мм – минуты, сс – секунды.
7.  Элемент _daylightsavingtime_ является обязательным и содержит 1 если используется летнее время, 0, если используется зимнее время, и 2, если документ сформирован для суток, в которые осуществлялся перевод часов с зимнего на летнее время и обратно.  Значение элемента _daylightsavingtime_ применяется ко всем значениям времени в данном документе.
8.  Элемент _day_ является обязательным и  содержит дату, определяющую операционный период, за который предоставляется информация, в формате ГГГГММДД где: ГГГГ – год, ММ – порядковый номер месяца, ДД – день. В случае предоставления информации за операционный период месяц, поле день (ДД) принимает значение 00.
9.  Элемент _sender_ является потомком корневого элемента _message_.В документе допускается наличие только одного элемента _sender_. Элемент _sender_ описывает организацию, предоставляющую информацию. Потомками элемента _sender_ являются элементы _inn_,_name_.
10. Элемент  _inn_ является обязательным и содержит ИНН организации, предоставляющей информацию.
11. Элемент  _name_ элемента _sender_ содержит название организации, предоставляющей информацию. Длина названия до 250 символов.
12. Элемент _area_ содержит информацию о результатах измерений по точкам измерения, точкам учета и датчикам ТИ одной организации субъекта ОРЭ (Если субъект ОРЭ представляет на рынке несколько организаций, то каждой организации в документе должно соответствовать своя секция  _area_.). Потомками элемента _area_ могут являться элементы _inn_, _name_, _measuringpoint_, _accountpoint_, _deliverypoint_, _deliverygroup_.
13. Элемент  _inn_ является обязательным и содержит ИНН организации субъекта ОРЭ.
14. Элемент _name_ является обязательным и содержит название организации субъекта ОРЭ. Длина названия до 250 символов.
15. Элемент _measuringpoint_ содержит сведения о точке измерения и результатах измерения по ней. Атрибутами элемента _measuringpoint_ являются code, name. Потомками элемента _measuringpoint_ являются элементы _measuringchannel_.
    содержимым атрибута name элемента _measuringpoint_ является наименование данной точки измерения. Длина наименования до 250 символов.
    атрибут code элемента _measuringpoint_ содержит уникальный код, присвоенный НП «АТС» данной точке измерения.
16. Элемент _accountpoint_ содержит сведения о точке учета и результатах измерения по ней. Атрибутами элемента _accountpoint_ являются code и name. Потомками элемента _accountpoint_ являются элементы _measuringchannel_.
    содержимым атрибута name является наименование данной точки учета. Длина наименования до 250 символов.
    атрибут code содержит уникальный код, присвоенный НП «АТС» точке учета.
17. Элемент _deliverypoint_ содержит сведения о точке поставки и результатах измерения в ней. Атрибутами элемента _deliverypoint_ являются code и name. Потомками элемента _deliverypoint_ являются элементы _measuringchannel_.
    содержимым атрибута name является наименование данной точки поставки. Длина наименования до 250 символов.
    атрибут code содержит уникальный код, присвоенный НП «АТС» точке поставки.
18. Элемент _deliverygroup_ содержит сведения о группе точек поставки и результатах измерения в ней. Атрибутами элемента _deliverypoint_ являются code и name. Потомками элемента _deliverygroup_ являются элементы _measuringchannel_.
    содержимым атрибута name является наименование данной группе точек поставки. Длина наименования до 250 символов.
    атрибут code содержит уникальный код, присвоенный НП «АТС» группе точек поставки.
19. Элемент _measuringchannel_ содержит информацию результатах измерений по точкам учета, точкам измерений, точкам поставки и группам точек поставки. Потомками элемента _measuringchannel_ являются элементы _period_.
    атрибут code элемента _measuringchannel_ содержит код измерительного канала, присвоенный НП «АТС» данному измерительному каналу ИС. В коде измерительного канала содержится информация о направлении передачи электроэнергии и типе измерительного канала.
    атрибут desc содержит описание измерительного канала ИС.
20. Элемент _period_ содержит временной диапазон вычисления и значения измерительных каналов точки учета и точки измерения. Потомками элемента _period_ являются элемент _value_. В зависимости от интервала измерений в элементах _measuringchannel_ должно присутствовать определенное количество элементов _period_. То есть для точки измерения с интервалом измерения 30 минут должно быть 48 элементов период, с интервалом измерения 15 минут - 96. Несовпадение числа элементов _period_ считается ошибкой формата и является основанием в отказе приема файла целиком. В сутки, когда осуществляется переход с зимнего на летнее время число периодов должно оставаться неизменным, а в сутки, когда осуществляется переход с летнего на зимнее время, число периодов должно быть увеличено с учетом появления лишнего часа. При этом элемент _daylightsavingtime_ (п4.2.7) принимает значение 2, а у периодов, относящиеся к летнему времени, устанавливается атрибут “summer” равный 1. 
21. Атрибуты _start_ и _end_ элемента _period_ являются обязательными и содержат дату и время начала и конца измерения соответственно, в формате “ччмм”, где: чч – часы, мм - минуты. Последний интервал в операционных сутках записывается в виде start=время начала периода, end=0000.
22. Содержимым элемента _value_ является значение результата измерения. Атрибутами элемента _value_ являются status, errofmeasuring, exstendedstatus, param1, param2, param3.
    содержимое атрибута status элемента _value_ показывает статус передаваемой информации. Статус 0 означает, что передаваемая информация имеет статус коммерческой. В этом случае атрибут статус может отсутствовать. Значение поля status 1 означает, что данную информацию нельзя использовать в коммерческих расчетах.
    Содержимое атрибута errofmeasuring элемента _value_ содержит абсолютную погрешность результатов измерений. Обязательность передачи атрибута определяется Актом соответствия АИСС техническим требованиям  ОРЭ.
    Атрибуты param1, param2, param3 содержат дополнительную информацию, содержание которой определяется значением атрибута extendedstatus.
    Атрибут extendedstatus содержит расширенный статус передаваемой информации. В частности, в случае замещения результатов измерений в точке измерения на значение результатов измерений в группе точек измерений (в случае включения присоединения через обходной выключатель),  значение атрибута exstendedstatus равно 1114, а значение атрибута param1 принимает значение равное коду, присвоенному НП «АТС» группе точек измерений.

Look, feel, be happy :-)
