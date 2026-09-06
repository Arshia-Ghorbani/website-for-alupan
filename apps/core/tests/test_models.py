import pytest
from django.utils import timezone

from apps.core.models import SiteSettings


@pytest.mark.django_db
def test_site_settings_is_a_singleton():
    first = SiteSettings.load()
    second = SiteSettings.load()
    assert first.pk == second.pk == 1
    assert SiteSettings.objects.count() == 1


@pytest.mark.django_db
def test_publishable_sets_published_at_on_publish():
    from apps.systems.models import System, SystemCategory

    category = SystemCategory.objects.create(name="Facade", slug="facade")
    system = System.objects.create(
        category=category, name="AP-70TB", slug="ap-70tb",
        status=System.Status.PUBLISHED,
    )
    assert system.published_at is not None
    assert system.published_at <= timezone.now()
    assert system.is_live is True
    assert System.objects.published().count() == 1
