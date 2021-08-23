from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import pytest
import pytz
from freezegun import freeze_time

from app.models.alerts import Alerts
from app.render import all_view_paths


def get_local_route_from_template_path(template_path):
    local_route = '/alerts/' + Path(template_path).stem
    if local_route != '/alerts/index':
        return local_route
    else:  # index page is mapped to root of /alerts directory
        return '/alerts'


local_routes_except_alerts = [
    get_local_route_from_template_path(template_path)
    for template_path in all_view_paths]


def test_local_links_lead_to_existing_routes_in_pages_with_no_alerts(client_get):
    for route in local_routes_except_alerts:
        html = client_get(route)
        local_links = html.select("a[href^='/alerts']")

        for link in local_links:
            path = urlparse(link['href']).path
            assert path in local_routes_except_alerts


@pytest.mark.parametrize("alert_timings", [
    {  # current alert
        "starts_at": datetime(2021, 4, 21, 11, 25, tzinfo=pytz.utc),
        "approved_at": datetime(2021, 4, 21, 11, 30, tzinfo=pytz.utc),
        "cancelled_at": datetime(2021, 4, 21, 12, 30, tzinfo=pytz.utc)
    },
    {  # past alert
        "starts_at": datetime(2021, 4, 20, 11, 25, tzinfo=pytz.utc),
        "approved_at": datetime(2021, 4, 20, 11, 30, tzinfo=pytz.utc),
        "cancelled_at": datetime(2021, 4, 20, 12, 30, tzinfo=pytz.utc)
    }
])
@freeze_time(datetime(2021, 4, 21, 11, 30, tzinfo=pytz.utc))
def test_local_links_lead_to_existing_routes_in_pages_with_alerts(
    client_get,
    alert_dict,
    alert_timings,
    mocker
):
    # fake an alert existing in the routes and data
    local_routes = local_routes_except_alerts + ['/alerts/21-Apr-2021']
    alert_dict['identifier'] = '21-Apr-2021'

    alert_dict.update(alert_timings)
    alerts_data = Alerts([alert_dict])

    mocker.patch('app.models.alerts.Alerts.load', return_value=alerts_data)

    for route in local_routes:
        html = client_get(route)
        local_links = html.select("a[href^='/alerts']")

        for link in local_links:
            path = urlparse(link['href']).path
            assert path in local_routes


@pytest.mark.parametrize('route', local_routes_except_alerts)
def test_links_have_correct_class_attribute(client_get, alert_dict, route):
    html = client_get(route)

    for link in html.select('main a'):
        assert 'govuk-link' in link['class']
