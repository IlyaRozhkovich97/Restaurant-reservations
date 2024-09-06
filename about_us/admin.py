from django.contrib import admin
from .models import RestaurantHistory, MissionAndValues, TeamMember

# Регистрация моделей в административной панели Django

admin.site.register(RestaurantHistory)
"""
Регистрация модели RestaurantHistory в административной панели Django.
Модель RestaurantHistory будет доступна для управления через админ-панель, где можно 
просматривать, редактировать и удалять записи о истории ресторана.
"""

admin.site.register(MissionAndValues)
"""
Регистрация модели MissionAndValues в административной панели Django.
Модель MissionAndValues будет доступна для управления через админ-панель, где можно 
просматривать, редактировать и удалять записи о миссии и ценностях ресторана.
"""

admin.site.register(TeamMember)
"""
Регистрация модели TeamMember в административной панели Django.
Модель TeamMember будет доступна для управления через админ-панель, где можно 
просматривать, редактировать и удалять записи о членах команды ресторана.
"""