from django.views.generic import TemplateView
from about_us.models import RestaurantHistory, MissionAndValues, TeamMember


class RestaurantPageView(TemplateView):
    """
    Представление для отображения страницы о ресторане.

    Данное представление используется для отображения информации о ресторане,
    включая его историю, миссию и ценности, а также команду.

    Атрибуты:
        template_name (str): Путь к шаблону, используемому для отображения страницы.

    Методы:
        get_context_data(**kwargs): Метод для получения контекста данных,
        передаваемых в шаблон.

    Контекст:
        - history (RestaurantHistory): История ресторана. Включает информацию о
          ресторане, которая была отмечена как опубликованная.
        - mission_and_values (MissionAndValues): Миссия и ценности ресторана.
          Включает информацию, которая была отмечена как опубликованная.
        - team_members (QuerySet[TeamMember]): Список всех членов команды ресторана.
    """
    template_name = 'about_us/about_use.html'

    def get_context_data(self, **kwargs):
        """
        Метод для получения контекста данных, передаваемых в шаблон.

        Получает следующие данные:
        - history: История ресторана, отфильтрованная по признаку опубликованности.
        - mission_and_values: Миссия и ценности ресторана, отфильтрованные по
          признаку опубликованности.
        - team_members: Список всех членов команды ресторана.

        Параметры:
            **kwargs: Дополнительные аргументы, передаваемые методу.

        Возвращает:
            dict: Словарь с контекстом данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['history'] = RestaurantHistory.objects.filter(is_published=True).first()
        context['mission_and_values'] = MissionAndValues.objects.filter(is_published=True).first()
        context['team_members'] = TeamMember.objects.all()
        return context
