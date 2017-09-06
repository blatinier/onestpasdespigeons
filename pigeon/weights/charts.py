import collections
from datetime import datetime, timedelta
from django.db.models.functions import ExtractWeek
from django.db.models import Count
from django.utils import timezone
from django.utils.translation import ugettext as _
from jchart import Chart
from jchart.config import DataSet, Legend, Axes, Tooltips
from weights.models import Measure


class ContribBarChart(Chart):
    chart_type = 'bar'
    legend = Legend(display=False)
    tooltips = Tooltips()
    scales = {
        'xAxes': [Axes(display=False,
                       position='bottom')]
    }
    options = {
        'maintainAspectRatio': False
    }
    def get_labels(self, user, **kwargs):
        return [_('week') + ' %s' % i for i in range(1, 53)]

    def get_datasets(self, user, **kwargs):
        now = datetime.now()
        a_year_ago = timezone.make_aware(now - timedelta(days=365))
        measures_by_week = (Measure.objects
                            .filter(user=user)
                            .filter(created_at__gt=a_year_ago)
                            .annotate(week=ExtractWeek('created_at'))
                            .values('week')
                            .annotate(Count('user')))
        current_week = int(now.strftime('%V'))
        data = [0] * 52
        for m in measures_by_week:
            data[m['week'] - 1] = m['user__count']
        data = collections.deque(data)
        data.rotate(52 - current_week)
        data = list(data)
        return [DataSet(label=_("# Measures"),
                        backgroundColor="#FF5A5F",
                        borderColor="#FF5A5F",
                        data=data)]

